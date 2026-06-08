# CHABI AYEDOUN Yoéla
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

    # CORRECTION : On patche les fonctions globales db.database importées ou utilisées dans auth
    @patch('routes.auth.fetch_one')
    def test_login_successful(self, mock_fetch_one, client):
        """Test successful login."""
        import bcrypt
        password = "TestPassword123"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # On simule directement le retour de fetch_one de manière propre
        mock_fetch_one.return_value = {
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
        
        assert response.status_code == 200

    @patch('routes.auth.bcrypt.checkpw')
    @patch('routes.auth.fetch_one')
    def test_login_with_invalid_credentials(self, mock_fetch_one, mock_checkpw, client):
        """Test login with invalid credentials."""
        # fetch_one renvoie None si l'utilisateur n'est pas trouvé en BDD
        mock_fetch_one.return_value = None
        
        response = client.post('/login', data={
            'email': 'notfound@example.com',
            'password': 'AnyPassword123'
        })
        
        assert response.status_code == 200
        assert len(response.data) > 0

    @patch('routes.auth.bcrypt.checkpw')
    @patch('routes.auth.fetch_one')
    def test_login_with_wrong_password(self, mock_fetch_one, mock_checkpw, client):
        """Test login with wrong password."""
        import bcrypt
        hashed = bcrypt.hashpw("CorrectPassword123".encode('utf-8'), bcrypt.gensalt())
        
        mock_fetch_one.return_value = {
            'id': 1,
            'email': 'test@example.com',
            'mot_de_passe': hashed.decode('utf-8'),
            'prenom': 'John',
            'nom': 'Doe',
            'est_actif': 1
        }
        
        # Le mot de passe ne correspond pas -> checkpw doit renvoyer False
        mock_checkpw.return_value = False
        
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'WrongPassword123'
        })
        
        assert response.status_code == 200
        assert len(response.data) > 0

    @patch('routes.auth.fetch_all')
    def test_register_page_loads(self, mock_fetch_all, client):
        """Test that register page loads successfully."""
        # On simule les appels successifs de fetch_all pour charger les filières et les niveaux
        mock_fetch_all.side_effect = [
            [{'id': 1, 'nom': 'Informatique'}],  # Pour les filières
            [{'id': 1, 'nom': 'L1'}]              # Pour les niveaux d'études
        ]
        
        response = client.get('/register')
        assert response.status_code == 200
        assert b'register' in response.data.lower()

    @patch('routes.auth.execute')
    @patch('routes.auth.fetch_all')
    @patch('routes.auth.fetch_one') # Ajoute fetch_one si ton code vérifie si l'email existe déjà
    def test_register_successful(self, mock_fetch_one, mock_fetch_all, mock_execute, client):
        """Test successful registration."""
        # 1. Aucun utilisateur existant avec cet email
        mock_fetch_one.return_value = None 
    
        # 2. Chargement des filières et niveaux pour le formulaire
        mock_fetch_all.side_effect = [
            [{'id': 1, 'nom': 'Informatique'}],
            [{'id': 1, 'nom': 'L1'}]
        ]
    
        # 3. L'exécution de l'INSERT renvoie l'ID généré
        mock_execute.return_value = 1
    
        response = client.post('/register', data={
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'jean@example.com',
            'telephone': '123456789',
            'password': 'TestPassword123',
            'id_filiere': '1',
            'id_niveau': '1'
        }, follow_redirects=True)
    
        # Vérifie que la page finale se charge bien (200) ou qu'on est redirigé vers le login
        assert response.status_code == 200

    @patch('routes.auth.execute')
    @patch('routes.auth.fetch_all')
    def test_register_duplicate_email(self, mock_fetch_all, mock_execute, client):
        """Test registration with duplicate email."""
        mock_fetch_all.side_effect = [
            [{'id': 1, 'nom': 'Informatique'}],
            [{'id': 1, 'nom': 'L1'}]
        ]
        
        # On simule la levée d'exception de la contrainte UNIQUE d'email de MySQL
        mock_execute.side_effect = Exception("Email already used")
        
        response = client.post('/register', data={
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'duplicate@example.com',
            'telephone': '123456789',
            'password': 'TestPassword123',
            'id_filiere': '1',
            'id_niveau': '1'
        })
        
        assert response.status_code in [200, 302]

    def test_logout(self, client):
        """Test logout functionality."""
        with client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['prenom'] = 'John'
                sess['nom'] = 'Doe'
            
            response = client.get('/logout', follow_redirects=True)
            
            with client.session_transaction() as sess:
                assert 'user_id' not in sess
            
            assert response.status_code == 200


class TestAuthSecurity:
    """Test authentication security features."""

    def test_session_isolation(self, client):
        """Test that sessions are isolated between requests."""
        with client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['data'] = 'sensitive'
            
            with client.session_transaction() as sess:
                assert sess.get('user_id') == 1
            
            with client.session_transaction() as sess:
                sess.clear()

    def test_password_hashing(self):
        """Test that passwords are properly hashed."""
        import bcrypt
        from utils.validators import valider_mot_de_passe
        
        password = "SecurePassword123"
        valid, msg = valider_mot_de_passe(password)
        assert valid is True
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        assert hashed.decode('utf-8') != password
        assert bcrypt.checkpw(password.encode('utf-8'), hashed)