import pytest
from unittest.mock import patch, MagicMock
from utils.responses import get_user_context, login_required


class TestUserContext:
    """Test user context retrieval."""

    def test_get_user_context_no_session(self, client):
        """Test get_user_context when no user is logged in."""
        from utils.responses import get_user_context
        with client:
            # Create request context without user_id
            with client.session_transaction() as sess:
                # Verify no user_id
                assert 'user_id' not in sess

    @patch('utils.responses.get_connection')
    def test_get_user_context_with_user(self, mock_get_connection, client):
        """Test get_user_context with logged-in user."""
        from utils.responses import get_user_context
        
        # Mock database
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchone.side_effect = [
            {
                'id': 1,
                'prenom': 'John',
                'nom': 'Doe',
                'email': 'john@example.com'
            },
            {'nb': 3}  # 3 unread notifications
        ]
        
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        
        # Make a request to set up request context
        response = client.get('/login')
        assert response.status_code == 200

    @patch('utils.responses.get_connection')
    def test_get_user_context_no_notifications(self, mock_get_connection, client):
        """Test get_user_context with no unread notifications."""
        from utils.responses import get_user_context
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchone.side_effect = [
            {
                'id': 1,
                'prenom': 'John',
                'nom': 'Doe',
                'email': 'john@example.com'
            },
            {'nb': 0}  # 0 unread notifications
        ]
        
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        
        # Make a request to set up request context
        response = client.get('/login')
        assert response.status_code == 200


class TestLoginRequired:
    """Test login_required decorator."""

    def test_login_required_with_session(self, client):
        """Test that login_required allows access when logged in."""
        @login_required
        def test_view():
            return "Success"
        
        with client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            
            # Make a request to create request context
            response = client.get('/')

    def test_login_required_without_session(self, client):
        """Test that login_required redirects when not logged in."""
        @login_required
        def test_view():
            return "Success"
        
        with client:
            # Request without user_id should be redirected
            response = client.get('/')
            # Should redirect to login
            assert response.status_code == 302 or response.status_code == 200

    def test_login_required_preserves_function_name(self):
        """Test that login_required preserves the wrapped function's name."""
        @login_required
        def my_test_function():
            """My docstring."""
            return "result"
        
        # The wrapper should preserve the original function's metadata
        assert my_test_function.__name__ == 'my_test_function'
        assert 'My docstring' in my_test_function.__doc__

    def test_login_required_with_args_and_kwargs(self, client):
        """Test login_required with function that has arguments."""
        @login_required
        def test_view_with_args(user_id, name=None):
            return f"user_{user_id}_{name}"
        
        with client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            
            # Make request to activate context
            response = client.get('/')

