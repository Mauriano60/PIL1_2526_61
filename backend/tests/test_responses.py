import pytest
from unittest.mock import patch, MagicMock
from flask import session, url_for
from utils.responses import get_user_context
from utils.decorators import login_required


class TestUserContext:
    """Test user context retrieval."""

    def test_get_user_context_no_session(self, client):
        """Test get_user_context when no user is logged in."""
        # On force un contexte de requête vide
        with client.application.test_request_context():
            context = get_user_context()
            # Si pas de session, le contexte doit retourner un dictionnaire vide
            assert context == {}

    # CORRECTION : On patche get_db de utils.responses au lieu de get_connection
    @patch('utils.responses.get_db')
    def test_get_user_context_with_user(self, mock_get_db, client):
        """Test get_user_context with logged-in user."""
        
        # Mock de la structure contextuelle de PyMySQL (with get_db() as conn -> with conn.cursor() as cursor)
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        mock_get_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Simuler les retours successifs pour : 1. L'utilisateur, 2. Le COUNT des notifs
        mock_cursor.fetchone.side_effect = [
            {
                'id': 1,
                'prenom': 'John',
                'nom': 'Doe',
                'email': 'john@example.com'
            },
            {'nb': 3}  # 3 notifications non lues
        ]
        
        # On exécute dans un contexte de requête avec une session active
        with client.application.test_request_context():
            session['user_id'] = 1
            context = get_user_context()
            
            assert context['user']['prenom'] == 'John'
            assert context['nb_notifs'] == 3

    @patch('utils.responses.get_db')
    def test_get_user_context_no_notifications(self, mock_get_db, client):
        """Test get_user_context with no unread notifications."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        mock_get_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        mock_cursor.fetchone.side_effect = [
            {
                'id': 1,
                'prenom': 'John',
                'nom': 'Doe',
                'email': 'john@example.com'
            },
            {'nb': 0}  # 0 notification
        ]
        
        with client.application.test_request_context():
            session['user_id'] = 1
            context = get_user_context()
            
            assert context['user']['nom'] == 'Doe'
            assert context['nb_notifs'] == 0


class TestLoginRequired:
    """Test login_required decorator."""

    def test_login_required_with_session(self, client):
        """Test that login_required allows access when logged in."""
        @login_required
        def dummy_view():
            return "Success"
        
        # On simule un utilisateur connecté en session
        with client.application.test_request_context():
            session['user_id'] = 1
            # La fonction doit s'exécuter normalement et retourner sa valeur
            result = dummy_view()
            assert result == "Success"

    def test_login_required_without_session(self, client):
        """Test that login_required redirects when not logged in."""
        @login_required
        def dummy_view():
            return "Success"

        with client.application.test_request_context():
            response = dummy_view()
            assert response.status_code == 302
            assert '/login' in response.headers['Location']

    def test_login_required_preserves_function_name(self):
        """Test that login_required preserves the wrapped function's name."""
        @login_required
        def my_test_function():
            """My docstring."""
            return "result"
        
        # Vérification des métadonnées (crucial pour le routing Flask)
        assert my_test_function.__name__ == 'my_test_function'
        assert 'My docstring' in my_test_function.__doc__

    def test_login_required_with_args_and_kwargs(self, client):
        """Test login_required with function that has arguments."""
        @login_required
        def test_view_with_args(user_id, name=None):
            return f"user_{user_id}_{name}"
        
        with client.application.test_request_context():
            session['user_id'] = 1
            result = test_view_with_args(42, name="Yoela")
            assert result == "user_42_Yoela"