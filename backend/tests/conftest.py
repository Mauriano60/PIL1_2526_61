import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import warnings
from config.settings import Config

# Config explicite avant l'import de create_app (qui déclenche app = create_app())
Config.RATELIMIT_STORAGE_URI = "memory://"

from app import create_app


TEMPLATE_FILES = {
    'auth/login.html': '''<!DOCTYPE html>
<html><head><title>Login</title></head><body>
    <h1>Login</h1>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    <form method="POST">
        <input type="email" name="email" required>
        <input type="password" name="password" required>
        <button type="submit">Login</button>
    </form>
</body></html>''',

    'auth/register.html': '''<!DOCTYPE html>
<html><head><title>Register</title></head><body>
    <h1>Register</h1>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    <form method="POST">
        <input type="text" name="prenom" required>
        <input type="text" name="nom" required>
        <input type="email" name="email" required>
        <input type="tel" name="telephone" required>
        <input type="password" name="password" required>
        <select name="id_filiere" required>
            <option value="">Select Filiere</option>
            {% for filiere in filieres %}<option value="{{ filiere.id }}">{{ filiere.nom }}</option>{% endfor %}
        </select>
        <select name="id_niveau" required>
            <option value="">Select Niveau</option>
            {% for niveau in niveaux %}<option value="{{ niveau.id }}">{{ niveau.nom }}</option>{% endfor %}
        </select>
        <button type="submit">Register</button>
    </form>
</body></html>''',

    'auth/email_envoye.html': '<h1>Email envoy\u00e9</h1><a href="/login">Retour</a>',

    'dashboard/index.html': '''<!DOCTYPE html>
<html><head><title>Dashboard</title></head><body>
    <h1>Dashboard</h1>
    <p>Welcome to your dashboard</p>
</body></html>''',

    'matching/index.html': '''<!DOCTYPE html>
<html><head><title>Matching</title></head><body>
    <h1>Matching</h1>
    {% for mentor in mentors %}<div>{{ mentor.prenom }} {{ mentor.nom }} - Score: {{ mentor.score_compatibilite }}%</div>{% endfor %}
    {% if matchs_en_attente %}<h2>En attente</h2>{% endif %}
    {% if matchs_acceptes %}<h2>Accept\u00e9s</h2>{% endif %}
</body></html>''',

    'mentorat/offres.html': '<h1>Offres</h1>{% for offre in offres %}<div>{{ offre.matiere }}</div>{% endfor %}',
    'mentorat/creer-offre.html': '<h1>Cr\u00e9er offre</h1>{% if error %}<p>{{ error }}</p>{% endif %}',
    'mentorat/demandes.html': '<h1>Demandes</h1>{% for demande in demandes %}<div>{{ demande.matiere }}</div>{% endfor %}',
    'mentorat/creer-demande.html': '<h1>Cr\u00e9er demande</h1>{% if error %}<p>{{ error }}</p>{% endif %}',
    'conversations/index.html': '<h1>Conversations</h1>{% if error %}<p>{{ error }}</p>{% endif %}',
    'notifications/index.html': '<h1>Notifications</h1>{% for n in notifications %}<div>{{ n.message }}</div>{% endfor %}',
    'references/index.html': '<h1>R\u00e9f\u00e9rences</h1>',
    'mentore/dashboard.html': '<h1>Dashboard Mentor\u00e9</h1>',
    'errors/403.html': '<h1>403</h1>',
    'forgot_password.html': '<h1>Mot de passe oubli\u00e9</h1><form method="POST"><input type="email" name="email"><button type="submit">Envoyer</button></form>',
    'reset_password.html': '<h1>R\u00e9initialiser</h1><form method="POST"><input type="password" name="mot_de_passe"><input type="password" name="confirm_mot_de_passe"><button type="submit">R\u00e9initialiser</button></form>',
    'profil/public.html': '<h1>Profil</h1>{% if profil_user %}<p>{{ profil_user.prenom }}</p>{% endif %}',

    'settings/profil_matieres.html': '<h1>Comp\u00e9tences</h1><form method="POST"><button type="submit">Save</button></form>',
    'settings/preferences.html': '<h1>Pr\u00e9f\u00e9rences</h1><form method="POST"><button type="submit">Save</button></form>',
    'settings/confidentialite.html': '<h1>Confidentialit\u00e9</h1><form method="POST"><button type="submit">Save</button></form>',
    'settings/supprimer-compte.html': '<h1>Supprimer compte</h1><form method="POST"><button type="submit">Supprimer</button></form>',
}


@pytest.fixture(scope="session", autouse=True)
def create_temp_templates():
    template_dir = Path(__file__).parent / "templates"

    for rel_path, content in TEMPLATE_FILES.items():
        filepath = template_dir / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)

    yield

    if template_dir.exists():
        import shutil
        shutil.rmtree(template_dir)


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    app.config['RATELIMIT_ENABLED'] = False

    template_folder = Path(__file__).parent / 'templates'
    app.template_folder = str(template_folder)

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield app
