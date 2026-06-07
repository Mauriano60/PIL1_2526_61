from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for

mail = Mail()

def generate_token(email):
    """Génère un token unique lié à l'email"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirmation')

def verify_token(token, expiration=3600):
    """Vérifie le token et retourne l'email s'il est valide"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirmation', max_age=expiration)
        return email
    except Exception:
        return None

def envoyer_email_confirmation(email, prenom):
    """Envoie un email de confirmation à l'utilisateur"""
    token = generate_token(email)
    lien = url_for('auth.confirmer_email', token=token, _external=True)

    msg = Message(
        subject="Confirmez votre adresse email - IFRI_MentorLink",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    msg.body = f"""
Bonjour {prenom},

Merci de vous être inscrit sur IFRI_MentorLink !

Cliquez sur le lien ci-dessous pour confirmer votre adresse email :
{lien}

Ce lien expire dans 1 heure.

Si vous n'avez pas créé de compte, ignorez cet email.

L'équipe IFRI_MentorLink
    """
    mail.send(msg)