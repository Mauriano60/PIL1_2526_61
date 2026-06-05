import pytest
import sys
import os
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app


@pytest.fixture(scope="session", autouse=True)
def create_temp_templates():
    """Create temporary templates for testing."""
    test_dir = Path(__file__).parent
    template_dir = test_dir / "templates"
    
    # Create template directories
    (template_dir / "auth").mkdir(parents=True, exist_ok=True)
    (template_dir / "dashboard").mkdir(parents=True, exist_ok=True)
    
    # Create login template
    login_html = template_dir / "auth" / "login.html"
    login_html.write_text("""<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    {% if error %}
    <p class="error">{{ error }}</p>
    {% endif %}
    <form method="POST">
        <input type="email" name="email" required>
        <input type="password" name="password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>""")
    
    # Create register template
    register_html = template_dir / "auth" / "register.html"
    register_html.write_text("""<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    {% if error %}
    <p class="error">{{ error }}</p>
    {% endif %}
    <form method="POST">
        <input type="text" name="prenom" required>
        <input type="text" name="nom" required>
        <input type="email" name="email" required>
        <input type="tel" name="telephone" required>
        <input type="password" name="password" required>
        <select name="id_filiere" required>
            <option value="">Select Filiere</option>
            {% for filiere in filieres %}
            <option value="{{ filiere.id }}">{{ filiere.nom }}</option>
            {% endfor %}
        </select>
        <select name="id_niveau" required>
            <option value="">Select Niveau</option>
            {% for niveau in niveaux %}
            <option value="{{ niveau.id }}">{{ niveau.nom }}</option>
            {% endfor %}
        </select>
        <button type="submit">Register</button>
    </form>
</body>
</html>""")
    
    # Create dashboard template
    dashboard_html = template_dir / "dashboard" / "index.html"
    dashboard_html.write_text("""<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body>
    <h1>Dashboard</h1>
    <p>Welcome to your dashboard</p>
</body>
</html>""")
    
    yield
    
    # Cleanup: remove temporary templates
    if template_dir.exists():
        shutil.rmtree(template_dir)


@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    # Configure template folder for tests
    template_folder = Path(__file__).parent / 'templates'
    app.template_folder = str(template_folder)
    
    return app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a CLI runner for testing CLI commands."""
    return app.test_cli_runner()


@pytest.fixture
def app_context(app):
    """Create an application context for testing."""
    with app.app_context():
        yield app


