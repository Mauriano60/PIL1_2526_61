# CHABI AYEDOUN Yoéla
from flask import Blueprint, flash, redirect, render_template, request, url_for
import secrets
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import bcrypt  
from db.database import fetch_one, execute 
from config.settings import Config

email_bp = Blueprint('email_bp', __name__)

# SMTP CONFIG
SMTP_SERVER = Config.MAIL_SERVER
SMTP_PORT = Config.MAIL_PORT
SMTP_USER = Config.MAIL_USERNAME      
SMTP_PASSWORD = Config.MAIL_PASSWORD


def send_reset_email(to_email: str, reset_link: str):
    msg = EmailMessage()
    msg["Subject"] = "Réinitialisation de votre mot de passe"
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    msg.set_content(
        f"Bonjour,\n\n"
        f"Cliquez ici pour réinitialiser :\n{reset_link}\n\n"
        f"Lien valide 1 heure."
    )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)


@email_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()

        # Utilisation directe de ta fonction fetch_one
        user = fetch_one("SELECT id, email FROM utilisateurs WHERE email=%s", (email,))

        if user:
            token = secrets.token_urlsafe(32)
            expires = datetime.now() + timedelta(hours=1)

            # Utilisation directe de ta fonction execute (qui gère le commit)
            execute(
                "UPDATE utilisateurs SET reset_token=%s, reset_expire=%s WHERE id=%s",
                (token, expires, user["id"])
            )

            reset_link = url_for("email_bp.reset_password", token=token, _external=True)
            send_reset_email(user["email"], reset_link)

        flash("Un email de réinitialisation vous a été envoyé.", "success")
        return redirect(url_for("auth.login"))

    return render_template("forgot_password.html")


@email_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    
    user = fetch_one(
        "SELECT id FROM utilisateurs WHERE reset_token=%s AND reset_expire > NOW()",
        (token,)
    )

    if not user:
        flash("Lien invalide ou expiré.", "error")
        return redirect(url_for("email_bp.forgot_password"))

    if request.method == "POST":
        password = request.form.get("mot_de_passe", "")
        confirm = request.form.get("confirm_mot_de_passe", "")

        if password != confirm:
            flash("Mots de passe différents.", "error")
            return redirect(url_for("email_bp.reset_password", token=token))

        # Hachage sécurisé
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Mise à jour et nettoyage du token en une seule fois
        execute(
            "UPDATE utilisateurs SET mot_de_passe=%s, reset_token=NULL, reset_expire=NULL WHERE id=%s",
            (hashed_password, user["id"])
        )

        flash("Mot de passe mis à jour.", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", token=token)