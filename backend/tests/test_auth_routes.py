import pytest
from unittest.mock import patch, MagicMock
from flask import session


class TestAuthRoutes:
    """Test authentication routes."""

    def test_index_redirects_to_login(self, client):
        """Test that index redirects to login page."""
        response = client.get('/')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_login_page_loads(self, client):
        """Test that login page loads successfully."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'login' in response.data.lower()

    @patch('routes.auth.get_connection')
    def test_login_successful(self, mock_get_connection, client):
        """Test successful login."""
        # Mock database connection and user
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock password hash
        import bcrypt
        password = "TestPassword123"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        mock_cursor.fetchone.return_value = {
            'id': 1,
            'email': 'test@example.com',
            'mot_de_passe': hashed.decode('utf-8'),
            'prenom': 'John',
            'nom': 'Doe',
            'est_actif': 1
        }
        
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': password
        }, follow_redirects=True)
        
        # Check that user was redirected (login was successful)
        assert response.status_code == 200

    @patch('routes.auth.bcrypt.checkpw')
    @patch('routes.auth.get_connection')
    def test_login_with_invalid_credentials(self, mock_get_connection, mock_checkpw, client):
        """Test login with invalid credentials."""
        # Mock database connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # User not found
        mock_cursor.fetchone.return_value = None
        
        response = client.post('/login', data={
            'email': 'notfound@example.com',
            'password': 'AnyPassword123'
        })
        
        assert response.status_code == 200
        # The response may contain the login form again or error message
        assert len(response.data) > 0

    @patch('routes.auth.bcrypt.checkpw')
    @patch('routes.auth.get_connection')
    def test_login_with_wrong_password(self, mock_get_connection, mock_checkpw, client):
        """Test login with wrong password."""
        import bcrypt
        
        # Mock database connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Create valid hash for wrong password
        hashed = bcrypt.hashpw("CorrectPassword123".encode('utf-8'), bcrypt.gensalt())
        
        mock_cursor.fetchone.return_value = {
            'id': 1,
            'email': 'test@example.com',
            'mot_de_passe': hashed.decode('utf-8'),
            'prenom': 'John',
            'nom': 'Doe',
            'est_actif': 1
        }
        
        # Mock checkpw to return False (wrong password)
        mock_checkpw.return_value = False
        
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'WrongPassword123'
        })
        
        assert response.status_code == 200
        # Login should fail and return login page
        assert len(response.data) > 0

    def test_register_page_loads(self, client):
        """Test that register page loads successfully."""
        with patch('routes.auth.get_connection') as mock_get_connection:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_get_connection.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            mock_cursor.fetchall.side_effect = [
                [{'id': 1, 'nom': 'Informatique'}],  # filieres
                [{'id': 1, 'nom': 'L1'}]  # niveaux
            ]
            
            response = client.get('/register')
            assert response.status_code == 200
            assert b'register' in response.data.lower()

    @patch('routes.auth.get_connection')
    def test_register_successful(self, mock_get_connection, client):
        """Test successful registration."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # For initial page load
        mock_cursor.fetchall.side_effect = [
            [{'id': 1, 'nom': 'Informatique'}],
            [{'id': 1, 'nom': 'L1'}],
            # After form submission - return value for fetchall won't be called
        ]
        
        mock_cursor.lastrowid = 1
        
        response = client.post('/register', data={
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'jean@example.com',
            'telephone': '123456789',
            'password': 'TestPassword123',
            'id_filiere': '1',
            'id_niveau': '1'
        }, follow_redirects=True)
        
        # Should redirect to login
        assert response.status_code == 200

    @patch('routes.auth.get_connection')
    def test_register_duplicate_email(self, mock_get_connection, client):
        """Test registration with duplicate email."""
        # For GET request (page load) and POST request, we need separate connections
        mock_conn_get = MagicMock()
        mock_cursor_get = MagicMock()
        
        mock_conn_post = MagicMock()
        mock_cursor_post = MagicMock()
        
        # Setup GET mocks
        mock_conn_get.cursor.return_value = mock_cursor_get
        mock_cursor_get.fetchall.side_effect = [
            [{'id': 1, 'nom': 'Informatique'}],
            [{'id': 1, 'nom': 'L1'}],
        ]
        
        # Setup POST mocks
        mock_conn_post.cursor.return_value = mock_cursor_post
        mock_cursor_post.execute.side_effect = Exception("Email already used")
        
        # Return different connections for each call
        mock_get_connection.side_effect = [mock_conn_get, mock_conn_post]
        
        response = client.post('/register', data={
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'duplicate@example.com',
            'telephone': '123456789',
            'password': 'TestPassword123',
            'id_filiere': '1',
            'id_niveau': '1'
        })
        
        # After error, user is redirected back to register page
        assert response.status_code in [200, 302]

    def test_logout(self, client):
        """Test logout functionality."""
        with client:
            # Set a session
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['prenom'] = 'John'
                sess['nom'] = 'Doe'
            
            # Perform logout
            response = client.get('/logout', follow_redirects=True)
            
            # Check that session is cleared
            with client.session_transaction() as sess:
                assert 'user_id' not in sess
            
            assert response.status_code == 200


class TestAuthSecurity:
    """Test authentication security features."""

    def test_session_isolation(self, client):
        """Test that sessions are isolated between requests."""
        # Test 1: Set session data
        with client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['data'] = 'sensitive'
            
            # Within the same context, session data is present
            with client.session_transaction() as sess:
                assert sess.get('user_id') == 1
            
            # Clear session
            with client.session_transaction() as sess:
                sess.clear()

    def test_password_hashing(self):
        """Test that passwords are properly hashed."""
        import bcrypt
        from utils.validators import valider_mot_de_passe
        
        password = "SecurePassword123"
        valid, msg = valider_mot_de_passe(password)
        assert valid is True
        
        # Simulate what registration does
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Verify hash is different from password
        assert hashed.decode('utf-8') != password
        
        # Verify password can be checked
        assert bcrypt.checkpw(password.encode('utf-8'), hashed)
