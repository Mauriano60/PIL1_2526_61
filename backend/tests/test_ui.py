import pytest
from unittest.mock import patch, MagicMock


class TestAuthUI:
    """Tests UI pour les pages d'authentification."""

    def test_login_page_has_form(self, client):
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data or b'Connexion' in response.data
        assert b'email' in response.data or b'Email' in response.data
        assert b'mot de passe' in response.data or b'password' in response.data

    def test_register_page_has_form(self, client):
        with patch('routes.auth.fetch_all') as mock_fetch_all:
            mock_fetch_all.side_effect = [
                [{'id': 1, 'nom': 'Informatique'}],
                [{'id': 1, 'nom': 'Licence 1'}],
            ]
            response = client.get('/register')
        assert response.status_code == 200
        assert b'Inscription' in response.data or b'Register' in response.data

    def test_email_envoye_page(self, client):
        response = client.get('/email-envoye')
        assert response.status_code == 200

    def test_forgot_password_page(self, client):
        response = client.get('/forgot-password')
        assert response.status_code == 200
        assert b'mot de passe' in response.data or b'email' in response.data

    def test_reset_password_page_invalid_token(self, client):
        with patch('routes.email.fetch_one') as mock_fetch_one:
            mock_fetch_one.return_value = None
            response = client.get('/reset-password/invalid-token', follow_redirects=True)
        assert response.status_code == 200

    def test_login_shows_error_on_failure(self, client):
        with patch('routes.auth.fetch_one') as mock_fetch_one:
            mock_fetch_one.return_value = None
            response = client.post('/login', data={
                'email': 'wrong@test.com',
                'password': 'wrong'
            })
        assert response.status_code == 200
        assert b'incorrect' in response.data or b'Email' in response.data

    def test_index_redirects_to_login(self, client):
        response = client.get('/')
        assert response.status_code == 302
        assert '/login' in response.headers['Location']


class TestProtectedRoutesUI:
    """Tests UI pour les routes protégées (redirection anonyme)."""

    def test_dashboard_redirects_anonymous(self, client):
        response = client.get('/dashboard')
        assert response.status_code == 302
        assert '/login' in response.headers['Location']

    def test_profil_redirects_anonymous(self, client):
        response = client.get('/profil/1')
        assert response.status_code == 302

    def test_matching_redirects_anonymous(self, client):
        response = client.get('/matching')
        assert response.status_code == 302

    def test_offres_redirects_anonymous(self, client):
        response = client.get('/offres')
        assert response.status_code == 302

    def test_creer_offre_redirects_anonymous(self, client):
        response = client.get('/offres/creer')
        assert response.status_code == 302

    def test_demandes_redirects_anonymous(self, client):
        response = client.get('/demandes')
        assert response.status_code == 302

    def test_creer_demande_redirects_anonymous(self, client):
        response = client.get('/demandes/creer')
        assert response.status_code == 302

    def test_conversations_redirects_anonymous(self, client):
        response = client.get('/conversations')
        assert response.status_code == 302

    def test_notifications_redirects_anonymous(self, client):
        response = client.get('/notifications')
        assert response.status_code == 302

    def test_references_redirects_anonymous(self, client):
        response = client.get('/references')
        assert response.status_code == 302

    def test_settings_profil_redirects_anonymous(self, client):
        response = client.get('/settings/profil')
        assert response.status_code == 302

    def test_settings_preferences_redirects_anonymous(self, client):
        response = client.get('/settings/preferences')
        assert response.status_code == 302

    def test_settings_confidentialite_redirects_anonymous(self, client):
        response = client.get('/settings/confidentialite')
        assert response.status_code == 302

    def test_settings_supprimer_compte_redirects_anonymous(self, client):
        response = client.get('/settings/supprimer-compte')
        assert response.status_code == 302


class TestAuthenticatedUI:
    """Tests UI pour les pages protégées (authentifié simulé)."""

    def test_dashboard_page_loads(self, client):
        with patch('routes.users.fetch_one') as mock_fetch_one:
            mock_fetch_one.side_effect = [
                {'id_filiere': 1},
                {'total': 5},
                {'total': 3},
                {'total': 2},
                {'total': 1},
            ]
            with patch('routes.users.fetch_all') as mock_fetch_all:
                mock_fetch_all.return_value = []
                with patch('utils.responses.get_user_context') as mock_ctx:
                    mock_ctx.return_value = {'user': None, 'nb_notifs': 0}
                    with client.session_transaction() as sess:
                        sess['user_id'] = 1
                    response = client.get('/dashboard')
        assert response.status_code == 200

    def test_matching_page_loads(self, client):
        with patch('routes.matching.obtenir_suggestions_matching') as mock_sug:
            mock_sug.return_value = []
            with patch('routes.matching.fetch_all') as mock_fa:
                mock_fa.return_value = []
                with client.session_transaction() as sess:
                    sess['user_id'] = 1
                response = client.get('/matching')
        assert response.status_code == 200

    def test_offres_page_loads(self, client):
        with patch('routes.offres.fetch_all') as mock_fa:
            mock_fa.return_value = []
            with patch('routes.offres.obtenir_suggestions_matching') as mock_sug:
                mock_sug.return_value = []
                with client.session_transaction() as sess:
                    sess['user_id'] = 1
                response = client.get('/offres')
        assert response.status_code == 200

    def test_creer_offre_page_loads(self, client):
        with patch('routes.offres.fetch_all') as mock_fa:
            mock_fa.return_value = [{'id': 1, 'nom': 'Maths'}]
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/offres/creer')
        assert response.status_code == 200

    def test_demandes_page_loads(self, client):
        with patch('routes.demandes.fetch_all') as mock_fa:
            mock_fa.return_value = []
            with patch('routes.demandes.obtenir_suggestions_matching') as mock_sug:
                mock_sug.return_value = []
                with client.session_transaction() as sess:
                    sess['user_id'] = 1
                response = client.get('/demandes')
        assert response.status_code == 200

    def test_creer_demande_page_loads(self, client):
        with patch('routes.demandes.fetch_all') as mock_fa:
            mock_fa.return_value = [{'id': 1, 'nom': 'Maths'}]
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/demandes/creer')
        assert response.status_code == 200

    def test_conversations_page_loads(self, client):
        with patch('routes.conversations.fetch_all') as mock_fa:
            mock_fa.return_value = []
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/conversations')
        assert response.status_code == 200

    def test_notifications_page_loads(self, client):
        with patch('routes.notifications.fetch_all') as mock_fa:
            mock_fa.return_value = []
            with patch('routes.notifications.execute') as mock_ex:
                mock_ex.return_value = None
                with client.session_transaction() as sess:
                    sess['user_id'] = 1
                response = client.get('/notifications')
        assert response.status_code == 200

    def test_references_page_loads(self, client):
        with patch('routes.references.fetch_all') as mock_fa:
            mock_fa.side_effect = [
                [{'id': 1, 'nom': 'Maths'}],
                [{'id': 1, 'nom': 'Info'}],
                [{'id': 1, 'nom': 'L1'}],
            ]
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/references')
        assert response.status_code == 200

    def test_settings_profil_page_loads(self, client):
        with patch('routes.parametres.fetch_all') as mock_fa:
            mock_fa.return_value = [{'id': 1, 'nom': 'Maths'}]
            with patch('routes.parametres.fetch_one') as mock_fo:
                mock_fo.side_effect = [
                    {'matiere_id': 1},
                    {'matiere_id': 2},
                ]
                with client.session_transaction() as sess:
                    sess['user_id'] = 1
                response = client.get('/settings/profil')
        assert response.status_code == 200

    def test_settings_preferences_page_loads(self, client):
        with patch('routes.parametres.fetch_one') as mock_fo:
            mock_fo.return_value = {'email_notification': 1, 'push_notification': 0}
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/settings/preferences')
        assert response.status_code == 200

    def test_settings_confidentialite_page_loads(self, client):
        with patch('routes.parametres.fetch_one') as mock_fo:
            mock_fo.return_value = {'visibilite_profil': 'public', 'email_notification': 1}
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/settings/confidentialite')
        assert response.status_code == 200

    def test_settings_supprimer_compte_page_loads(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        response = client.get('/settings/supprimer-compte')
        assert response.status_code == 200

    def test_profil_not_found(self, client):
        with patch('routes.users.fetch_one') as mock_fo:
            mock_fo.return_value = None
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/profil/999')
        assert response.status_code == 404

    def test_conversation_403_forbidden(self, client):
        with patch('routes.conversations.fetch_one') as mock_fo:
            mock_fo.return_value = None
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/conversations/999')
        assert response.status_code == 403


