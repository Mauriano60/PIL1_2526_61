from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mentorlink_secret_2024'
    app.config['DEBUG'] = True

    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.matching import matching_bp
    from routes.conversations import conversations_bp
    from routes.notifications import notifications_bp
    from routes.offres import offres_bp
    from routes.demandes import demandes_bp
    from routes.parametres import settings_bp
    from routes.references import references_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(conversations_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(offres_bp)
    app.register_blueprint(demandes_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(references_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)