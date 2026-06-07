from functools import wraps
import secrets
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

from flask import flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "votre_email@gmail.com"
SMTP_PASSWORD = "mot_de_passe_application"


def send_reset_email(to_email: str, reset_link: str):
    """Envoie un email avec le lien de réinitialisation."""
    msg = EmailMessage()
    msg["Subject"] = "Réinitialisation de votre mot de passe"
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    msg.set_content(
        f"Bonjour,\n\n"
        f"Vous avez demandé la réinitialisation de votre mot de passe.\n"
        f"Cliquez sur le lien ci-dessous pour définir un nouveau mot de passe :\n\n"
        f"{reset_link}\n\n"
        f"Ce lien est valable pendant 1 heure.\n"
    )

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Erreur d'envoi : {e}")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()

        user = fetch_one(
            "SELECT id, email FROM utilisateurs WHERE email=%s",
            (email,)
        )

        if user:
            token = secrets.token_urlsafe(32)
            expires = datetime.now() + timedelta(hours=1)

            execute(
                "UPDATE utilisateurs SET reset_token=%s, reset_expires=%s WHERE id=%s",
                (token, expires, user["id"])
            )

            reset_link = url_for(
                "reset_password",
                token=token,
                _external=True
            )

            send_reset_email(user["email"], reset_link)

        flash(
            "Si cette adresse existe, un lien de réinitialisation a été envoyé.",
            "info"
        )
        return redirect(url_for("login"))

    return render_template("forgot_password.html")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    user = fetch_one(
        """
        SELECT id
        FROM utilisateurs
        WHERE reset_token=%s
        AND reset_expires > NOW()
        """,
        (token,)
    )

    if not user:
        flash("Lien invalide ou expiré.", "error")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":

        password = request.form.get("mot_de_passe", "")
        confirm = request.form.get("confirm_mot_de_passe", "")

        if len(password) < 6:
            flash(
                "Le mot de passe doit contenir au moins 6 caractères.",
                "error"
            )
            return redirect(
                url_for("reset_password", token=token)
            )

        if password != confirm:
            flash(
                "Les mots de passe ne correspondent pas.",
                "error"
            )
            return redirect(
                url_for("reset_password", token=token)
            )

        execute(
            """
            UPDATE utilisateurs
            SET mot_de_passe=%s,
                reset_token=NULL,
                reset_expires=NULL
            WHERE id=%s
            """,
            (generate_password_hash(password), user["id"])
        )

        flash(
            "Mot de passe réinitialisé avec succès.",
            "success"
        )
        return redirect(url_for("login"))

    return render_template(
        "reset_password.html",
        token=token
    )