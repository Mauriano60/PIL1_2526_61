# CHABI AYEDOUN Yoéla
import pytest
from unittest.mock import patch, MagicMock
from flask import session

class TestUserDashboard:
    """Tests fonctionnels pour le tableau de bord utilisateur."""

        # CORRECTION : On patche la source directe dans utils.responses
    @patch('routes.users.fetch_one')
    @patch('routes.users.fetch_all')
    @patch('utils.responses.get_user_context') # On patche la source absolue
    def test_dashboard_access_authenticated(self, mock_get_context, mock_fetch_all, mock_fetch_one, client):
        """Vérifie que le dashboard charge les données correctement si l'utilisateur est connecté."""
        
        # On force également le mock dans le namespace local des routes au cas où
        import routes.users
        routes.users.get_user_context = mock_get_context
        
        # Configuration de la valeur de retour du mock
        mock_get_context.return_value = {
            'user': {'id': 1, 'prenom': 'Yoéla', 'nom': 'CHABI', 'id_filiere': 1},
            'nb_notifs': 0
        }
        
        mock_fetch_one.return_value = {'id_filiere': 1}
        mock_fetch_all.side_effect = [[], [], []] # Mock pour les 3 requêtes SQL du dashboard

        with client.session_transaction() as sess:
            sess['user_id'] = 1

        response = client.get('/dashboard')
        assert response.status_code == 200
    def test_dashboard_redirects_anonymous(self, client):
        """Vérifie que le dashboard redirige un utilisateur non connecté."""
        response = client.get('/dashboard')
        assert response.status_code == 302
        assert '/login' in response.headers['Location']


class TestUserProfile:
    """Tests fonctionnels pour la page de profil."""

    @patch('routes.users.fetch_one')
    @patch('routes.users.fetch_all')
    def test_profile_not_found(self, mock_fetch_all, mock_fetch_one, client):
        """Vérifie qu'une erreur 404 est renvoyée si l'utilisateur ciblé n'existe pas ou est inactif."""
        mock_fetch_one.return_value = None # Utilisateur introuvable
        
        with client.session_transaction() as sess:
            sess['user_id'] = 1 # Connecté

        response = client.get('/profil/999') # ID inexistant
        assert response.status_code == 404
        assert b"Utilisateur introuvable" in response.data