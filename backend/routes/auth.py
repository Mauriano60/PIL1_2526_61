from flask import Blueprint, render_template, request, redirect, url_for, session
from db.database import get_connection
from utils.validators import valider_inscription
from services.mail_service import envoyer_email_confirmation, verify_token
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
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateurs WHERE email = %s AND est_actif = 1", (email,))
            user = cursor.fetchone()
            if user and bcrypt.checkpw(password.encode('utf-8'), user['mot_de_passe'].encode('utf-8')):
                # Vérifier si l'email a été confirmé
                if not user['email_verifie']:
                    error = "Veuillez confirmer votre adresse email avant de vous connecter"
                else:
                    session['user_id'] = user['id']
                    session['prenom'] = user['prenom']
                    session['nom'] = user['nom']
                    return redirect(url_for('users.dashboard'))
            else:
                error = "Email ou mot de passe incorrect"
        except Exception as e:
            error = f"Erreur lors de la connexion: {str(e)}"
        finally:
            if conn:
                conn.close()
    return render_template('auth/login.html', error=error)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    filieres = []
    niveaux = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM filieres_etudes")
        filieres = cursor.fetchall()
        cursor.execute("SELECT * FROM niveaux_etudes")
        niveaux = cursor.fetchall()
    except Exception as e:
        error = f"Erreur lors du chargement des filières et niveaux: {str(e)}"
    finally:
        if conn:
            conn.close()

    if request.method == 'POST':
        erreurs = valider_inscription(request.form)
        if erreurs:
            error = " | ".join(erreurs)
        else:
            conn = None
            try:
                prenom = request.form['prenom']
                nom = request.form['nom']
                email = request.form['email']
                telephone = request.form['telephone']
                password = request.form['password']
                id_filiere = request.form['id_filiere']
                id_niveau = request.form['id_niveau']
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO utilisateurs (email, telephone, mot_de_passe, prenom, nom, id_filiere, id_niveau)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (email, telephone, hashed.decode('utf-8'), prenom, nom, id_filiere, id_niveau))
                user_id = cursor.lastrowid
                cursor.execute("INSERT INTO parametres (utilisateur_id) VALUES (%s)", (user_id,))
                conn.commit()

                # Envoyer l'email de confirmation
                envoyer_email_confirmation(email, prenom)

                return redirect(url_for('auth.email_envoye'))
            except Exception as e:
                error = "Email ou téléphone déjà utilisé"
            finally:
                if conn:
                    conn.close()

    return render_template('auth/register.html', error=error, filieres=filieres, niveaux=niveaux)

@auth_bp.route('/email-envoye')
def email_envoye():
    return render_template('auth/email_envoye.html')

@auth_bp.route('/confirmer-email/<token>')
def confirmer_email(token):
    # Vérifier le token
    email = verify_token(token)
    if not email:
        return "Lien invalide ou expiré. Veuillez vous réinscrire.", 400
    # CHABI AYEDOUN Yoéla

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE utilisateurs SET email_verifie = 1
            WHERE email = %s
        """, (email,))
        conn.commit()
        return redirect(url_for('auth.login'))
    except Exception as e:
        return f"Erreur : {str(e)}", 500
    finally:
        if conn:
            conn.close()

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))