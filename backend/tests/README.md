# MentorLink Backend Tests

Cette suite de tests couvre les fonctionnalités principales du backend MentorLink.

## 📋 Structure des tests

### `test_validators.py`
Tests unitaires pour les fonctions de validation:
- **TestEmailValidation**: Validation des adresses email
- **TestPhoneValidation**: Validation des numéros de téléphone
- **TestPasswordValidation**: Validation des mots de passe
- **TestRegistrationValidation**: Validation complète du formulaire d'inscription

### `test_auth_routes.py`
Tests d'intégration pour les routes d'authentification:
- **TestAuthRoutes**: Tests des endpoints de login/register/logout
- **TestAuthSecurity**: Tests de sécurité (hachage de mot de passe, isolation de sessions)

### `test_responses.py`
Tests pour les utilitaires de réponse:
- **TestUserContext**: Tests de récupération du contexte utilisateur
- **TestLoginRequired**: Tests du décorateur `login_required`

## 🚀 Installation des dépendances

```bash
pip install -r requirements.txt
```

## ▶️ Exécution des tests

### Tous les tests
```bash
pytest tests/
# ou
python run_tests.py
```

### Tests spécifiques
```bash
# Validators uniquement
pytest tests/test_validators.py
python run_tests.py --validators

# Auth uniquement
pytest tests/test_auth_routes.py
python run_tests.py --auth

# Responses uniquement
pytest tests/test_responses.py
python run_tests.py --responses
```

### Avec rapport de couverture
```bash
pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
# ou
python run_tests.py --coverage
```

### Mode détaillé
```bash
pytest tests/ -v -s
```

### Arrêter au premier échec
```bash
pytest tests/ -x
```

## 📊 Rapport de couverture

Après avoir exécuté les tests avec `--coverage`, consultez:
- Terminal: résumé dans le terminal
- HTML: `htmlcov/index.html`

## 🧪 Écrire de nouveaux tests

### Structure d'un test
```python
class TestFeatureName:
    """Description de ce qui est testé."""
    
    def test_specific_case(self, client):
        """Description du cas de test."""
        # Arrange: Préparer les données
        # Act: Exécuter le code
        # Assert: Vérifier les résultats
        assert result == expected
```

### Fixtures disponibles (conftest.py)
- `app`: L'application Flask
- `client`: Client de test Flask
- `runner`: CLI runner
- `app_context`: Contexte d'application

### Exemple avec mock
```python
from unittest.mock import patch, MagicMock

@patch('module.function')
def test_with_mock(self, mock_func, client):
    mock_func.return_value = {"data": "mocked"}
    # ... test code
```

## ✅ Checklist avant commit

- [ ] Tous les tests passent: `pytest tests/`
- [ ] Couverture de code acceptable: `pytest --cov=.`
- [ ] Pas d'avertissements: `pytest tests/ -W error::Warning`
- [ ] Code valide: `python -m py_compile backend/**/*.py`

## 🔗 Ressources

- [Documentation pytest](https://docs.pytest.org/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Flask Testing](https://flask.palletsprojects.com/testing/)

## 📝 Notes

- Les tests utilisent des mocks pour éviter les dépendances à la base de données
- Les fixtures définies dans `conftest.py` sont automatiquement disponibles
- Les tests sont isolés et peuvent être exécutés dans n'importe quel ordre
