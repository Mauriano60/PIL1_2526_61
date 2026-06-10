import os
from dotenv import load_dotenv

# On charge le fichier .env caché au tout début
load_dotenv()

class Config:
    # On récupère les valeurs depuis le .env de manière sécurisée
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY", "une_cle_de_secours_super_securisee")
    # Le os.getenv renvoie du texte, on le convertit en booléen pour DEBUG
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    # Configuration email — paramètres techniques non sensibles
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # Identifiants sensibles récupérés depuis .env
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # Mode local — pas d'envoi SMTP, l'email est affiché dans la console
    MAIL_SUPPRESS_SEND = True
    MAIL_DEBUG = True