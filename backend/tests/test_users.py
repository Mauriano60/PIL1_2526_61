import pytest
from unittest.mock import patch, MagicMock
from flask import session

class TestUserDashboard:
    """Tests fonctionnels pour le tableau de bord utilisateur."""

    @patch('routes.users.fetch_one')
    @patch('routes.users.fetch_all')
    @patch('utils.responses.get_user_context')
    def test_dashboard_access_authenticated(self, mock_get_context, mock_fetch_all, mock_fetch_one, client):
        """Vérifie que le dashboard charge les données correctement si l'utilisateur est connecté."""
        import routes.users
        routes.users.get_user_context = mock_get_context

        mock_get_context.return_value = {
            'user': {'id': 1, 'prenom': 'Yoéla', 'nom': 'CHABI', 'id_filiere': 1},
            'nb_notifs': 0
        }

        # 5 appels à fetch_one dans le dashboard
        mock_fetch_one.side_effect = [
            {'id_filiere': 1},       # user_info
            {'total': 5},             # nb_offres_filiere
            {'total': 3},             # nb_demandes_profil
            {'total': 2},             # nb_correspondances
            {'total': 1},             # nb_messages_non_lus
        ]
        mock_fetch_all.side_effect = [[], [], []]  

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
    
    @patch('routes.matching.fetch_all')
    @patch('routes.matching.obtenir_suggestions_matching')
    def test_matching_view_success(self, mock_suggestions, mock_fetch_all, client):
        """Vérifie que la page de matching charge sans encombre avec le nouveau système."""
        mock_suggestions.return_value = []
        mock_fetch_all.return_value = [] # Renvoie une liste vide pour simuler aucun historique

        with client.session_transaction() as sess:
            sess['user_id'] = 1

        response = client.get('/matching')
        assert response.status_code == 200