from flask import Blueprint, render_template, request, redirect, url_for, session
from db.database import get_connection
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateurs WHERE email = %s AND est_actif = 1", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['mot_de_passe'].encode('utf-8')):
            session['user_id'] = user['id']
            session['prenom'] = user['prenom']
            session['nom'] = user['nom']
            return redirect(url_for('users.dashboard'))
        else:
            error = "Email ou mot de passe incorrect"

    return render_template('auth/login.html', error=error)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        email = request.form['email']
        telephone = request.form['telephone']
        password = request.form['password']
        id_filiere = request.form['id_filiere']
        id_niveau = request.form['id_niveau']

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO utilisateurs (email, telephone, mot_de_passe, prenom, nom, id_filiere, id_niveau)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (email, telephone, hashed.decode('utf-8'), prenom, nom, id_filiere, id_niveau))
            user_id = cursor.lastrowid

            cursor.execute("INSERT INTO parametres (utilisateur_id) VALUES (%s)", (user_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('auth.login'))
        except Exception as e:
            error = "Email ou téléphone déjà utilisé"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM filieres_etudes")
    filieres = cursor.fetchall()
    cursor.execute("SELECT * FROM niveaux_etudes")
    niveaux = cursor.fetchall()
    conn.close()

    return render_template('auth/register.html', error=error, filieres=filieres, niveaux=niveaux)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))