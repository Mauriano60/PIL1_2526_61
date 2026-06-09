import pytest
from utils.validators import (
    valider_email,
    valider_telephone,
    valider_mot_de_passe,
    valider_inscription
)


class TestEmailValidation:
    """Test email validation function."""

    def test_valid_email_simple(self):
        """Test simple valid email."""
        assert valider_email("user@example.com") is True

    def test_valid_email_with_dot(self):
        """Test valid email with dot in local part."""
        assert valider_email("john.doe@example.com") is True

    def test_valid_email_with_hyphen(self):
        """Test valid email with hyphen."""
        assert valider_email("user-name@example.co.uk") is True

    def test_invalid_email_no_at(self):
        """Test email without @ symbol."""
        assert valider_email("userexample.com") is False

    def test_invalid_email_no_domain(self):
        """Test email without domain."""
        assert valider_email("user@") is False

    def test_invalid_email_no_extension(self):
        """Test email without extension."""
        assert valider_email("user@example") is False

    def test_invalid_email_spaces(self):
        """Test email with spaces."""
        assert valider_email("user @example.com") is False

    def test_invalid_email_empty(self):
        """Test empty email."""
        assert valider_email("") is False


class TestPhoneValidation:
    """Test phone validation function."""

    def test_valid_phone_8_digits(self):
        """Test valid phone with 8 digits."""
        assert valider_telephone("12345678") is True

    def test_valid_phone_9_digits(self):
        """Test valid phone with 9 digits."""
        assert valider_telephone("123456789") is True

    def test_valid_phone_10_digits(self):
        """Test valid phone with 10 digits."""
        assert valider_telephone("1234567890") is True

    def test_invalid_phone_too_short(self):
        """Test phone with less than 8 digits."""
        assert valider_telephone("1234567") is False

    def test_invalid_phone_with_letters(self):
        """Test phone with letters."""
        assert valider_telephone("1234567a") is False

    def test_invalid_phone_with_spaces(self):
        """Test phone with spaces."""
        assert valider_telephone("123 456 789") is False

    def test_invalid_phone_empty(self):
        """Test empty phone."""
        assert valider_telephone("") is False

    def test_invalid_phone_special_chars(self):
        """Test phone with special characters."""
        assert valider_telephone("123-456-789") is False


class TestPasswordValidation:
    """Test password validation function."""

    def test_valid_password(self):
        """Test valid password with all requirements."""
        valid, msg = valider_mot_de_passe("Password123")
        assert valid is True
        assert msg is None

    def test_invalid_password_too_short(self):
        """Test password shorter than 8 characters."""
        valid, msg = valider_mot_de_passe("Pass12")
        assert valid is False
        assert "8 caractère" in msg.lower()

    def test_invalid_password_no_uppercase(self):
        """Test password without uppercase letter."""
        valid, msg = valider_mot_de_passe("password123")
        assert valid is False
        assert "majuscule" in msg.lower()

    def test_invalid_password_no_digit(self):
        """Test password without digit."""
        valid, msg = valider_mot_de_passe("Password")
        assert valid is False
        assert "chiffre" in msg.lower()

    def test_valid_password_exact_8_chars(self):
        """Test valid password with exactly 8 characters."""
        valid, msg = valider_mot_de_passe("Passwor1")
        assert valid is True

    def test_valid_password_long(self):
        """Test valid password that is very long."""
        valid, msg = valider_mot_de_passe("VeryLongPassword1234567890")
        assert valid is True


class TestRegistrationValidation:
    """Test full registration validation."""

    def test_valid_registration_form(self):
        """Test valid registration form."""
        form = {
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'jean@example.com',
            'telephone': '123456789',
            'password': 'Password123',
            'id_filiere': '1',
            'id_niveau': '1'
        }
        erreurs = valider_inscription(form)
        assert len(erreurs) == 0

    def test_missing_first_name(self):
        """Test registration with missing first name."""
        form = {
            'prenom': '',
            'nom': 'Dupont',
            'email': 'jean@example.com',
            'telephone': '123456789',
            'password': 'Password123',
            'id_filiere': '1',
            'id_niveau': '1'
        }
        erreurs = valider_inscription(form)
        assert any('prénom' in e.lower() for e in erreurs)

    def test_missing_last_name(self):
        """Test registration with missing last name."""
        form = {
            'prenom': 'Jean',
            'nom': '',
            'email': 'jean@example.com',
            'telephone': '123456789',
            'password': 'Password123',
            'id_filiere': '1',
            'id_niveau': '1'
        }
        erreurs = valider_inscription(form)
        assert any('nom' in e.lower() for e in erreurs)

    def test_invalid_email_in_registration(self):
        """Test registration with invalid email."""
        form = {
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'invalid-email',
            'telephone': '123456789',
            'password': 'Password123',
            'id_filiere': '1',
            'id_niveau': '1'
        }
        erreurs = valider_inscription(form)
        assert any('email' in e.lower() for e in erreurs)

    def test_invalid_phone_in_registration(self):
        """Test registration with invalid phone."""
        form = {
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'jean@example.com',
            'telephone': '12345',
            'password': 'Password123',
            'id_filiere': '1',
            'id_niveau': '1'
        }
        erreurs = valider_inscription(form)
        assert any('téléphone' in e.lower() for e in erreurs)

    def test_weak_password_in_registration(self):
        """Test registration with weak password."""
        form = {
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'jean@example.com',
            'telephone': '123456789',
            'password': 'weak',
            'id_filiere': '1',
            'id_niveau': '1'
        }
        erreurs = valider_inscription(form)
        assert len(erreurs) > 0

    def test_missing_filiere(self):
        """Test registration with missing filiere."""
        form = {
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'jean@example.com',
            'telephone': '123456789',
            'password': 'Password123',
            'id_filiere': '',
            'id_niveau': '1'
        }
        erreurs = valider_inscription(form)
        assert any('filière' in e.lower() for e in erreurs)

    def test_missing_niveau(self):
        """Test registration with missing niveau."""
        form = {
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'jean@example.com',
            'telephone': '123456789',
            'password': 'Password123',
            'id_filiere': '1',
            'id_niveau': ''
        }
        erreurs = valider_inscription(form)
        assert any('niveau' in e.lower() for e in erreurs)