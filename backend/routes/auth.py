# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, request, redirect, url_for, session
# CORRECTION : On importe les fonctions réelles de ton database.py
from db.database import fetch_one, fetch_all, execute
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
        
        try:
            # Utilisation de fetch_one (gère automatiquement la connexion et la fermeture)
            user = fetch_one("SELECT * FROM utilisateurs WHERE email = %s AND est_actif = 1", (email,))
            
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
            
    return render_template('auth/login.html', error=error)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    
    # Chargement dynamique des filières et niveaux avec fetch_all
    try:
        filieres = fetch_all("SELECT * FROM filieres_etudes")
        niveaux = fetch_all("SELECT * FROM niveaux_etudes")
    except Exception as e:
        filieres = []
        niveaux = []
        error = f"Erreur lors du chargement des filières et niveaux: {str(e)}"

    if request.method == 'POST':
        erreurs = valider_inscription(request.form)
        if erreurs:
            error = " | ".join(erreurs)
        else:
            try:
                prenom = request.form['prenom']
                nom = request.form['nom']
                email = request.form['email']
                telephone = request.form['telephone']
                password = request.form['password']
                id_filiere = request.form['id_filiere']
                id_niveau = request.form['id_niveau']
                
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                # Insertion de l'utilisateur avec execute (renvoie directement le lastrowid)
                user_id = execute("""
                    INSERT INTO utilisateurs (email, telephone, mot_de_passe, prenom, nom, id_filiere, id_niveau)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (email, telephone, hashed.decode('utf-8'), prenom, nom, id_filiere, id_niveau))
                
                # Insertion des paramètres initiaux
                execute("INSERT INTO parametres (utilisateur_id) VALUES (%s)", (user_id,))

                # Envoyer l'email de confirmation
                envoyer_email_confirmation(email, prenom)

                return redirect(url_for('auth.email_envoye'))
            except Exception:
                error = "Email ou téléphone déjà utilisé"

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
    
    try:
        # Mise à jour du statut de l'étudiant
        execute("""
            UPDATE utilisateurs SET email_verifie = 1
            WHERE email = %s
        """, (email,))
        return redirect(url_for('auth.login'))
    except Exception as e:
        return f"Erreur : {str(e)}", 500

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))