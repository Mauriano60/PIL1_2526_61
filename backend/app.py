from flask import Flask,session
from config.settings import Config
from services.mail_service import mail
from flask_socketio import SocketIO, join_room
from extensions import limiter

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    
    # Charger toute la config depuis settings.py (qui lit le .env)
    app.config.from_object(Config)
    app.config['SERVER_NAME'] = '127.0.0.1:5000'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'
    
    
    mail.init_app(app)

    limiter.init_app(app)

    from utils.csrf import generer_token_csrf

    @app.context_processor
    def inject_csrf():
        return dict(csrf_token=generer_token_csrf)

    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.matching import matching_bp
    from routes.conversations import conversations_bp
    from routes.notifications import notifications_bp
    from routes.offres import offres_bp
    from routes.demandes import demandes_bp
    from routes.parametres import settings_bp
    from routes.references import references_bp
    from routes.email import email_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(conversations_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(offres_bp)
    app.register_blueprint(demandes_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(references_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(dashboard_bp)

    return app

app = create_app()

socketio.init_app(app)

@socketio.on('connect')
def handle_connect():
    if 'user_id' in session:
        utilisateur_id = session['user_id']
        join_room(f"user_{utilisateur_id}")
        print(f"L'utilisateur {utilisateur_id} a rejoint son canal de notification en temps réel.")

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)