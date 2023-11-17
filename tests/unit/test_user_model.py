import pytest
from project.models import User


def test_valid_user_creation():
    user = User("test@example.com", "Abcd1234!")
    assert user.email == "test@example.com"
    assert user.is_password_correct("Abcd1234!")
    assert user._is_valid_password("Abcd1234!")


def test_invalid_email():
    with pytest.raises(ValueError, match="Invalid email address."):
        User("invalid_email", "Abcd1234!")


def test_invalid_password_length():
    with pytest.raises(ValueError, match="Invalid password. It must have one special character, only ASCII characters, at least one number, at least one uppercase and one lowercase character, and a length between 8 and 20."):
        User("test@example.com", "Short1!")


def test_invalid_password_no_special_char():
    with pytest.raises(ValueError, match="Invalid password. It must have one special character, only ASCII characters, at least one number, at least one uppercase and one lowercase character, and a length between 8 and 20."):
        User("test@example.com", "Abcd1234")


def test_invalid_password_no_number():
    with pytest.raises(ValueError, match="Invalid password. It must have one special character, only ASCII characters, at least one number, at least one uppercase and one lowercase character, and a length between 8 and 20."):
        User("test@example.com", "AbcdEfgh!")


def test_invalid_password_no_lowercase_char():
    with pytest.raises(ValueError, match="Invalid password. It must have one special character, only ASCII characters, at least one number, at least one uppercase and one lowercase character, and a length between 8 and 20."):
        User("test@example.com", "ABCD1234!")


def test_invalid_password_no_uppercase_char():
    with pytest.raises(ValueError, match="Invalid password. It must have one special character, only ASCII characters, at least one number, at least one uppercase and one lowercase character, and a length between 8 and 20."):
        User("test@example.com", "abcd1234!")


def test_invalid_password_only_digits():
    with pytest.raises(ValueError, match="Invalid password. It must have one special character, only ASCII characters, at least one number, at least one uppercase and one lowercase character, and a length between 8 and 20."):
        User("test@example.com", "12345678")


def test_invalid_password_only_special_chars():
    with pytest.raises(ValueError, match="Invalid password. It must have one special character, only ASCII characters, at least one number, at least one uppercase and one lowercase character, and a length between 8 and 20."):
        User("test@example.com", "!@#$%^&*")


def test_invalid_password_exceeds_max_length():
    with pytest.raises(ValueError, match="Invalid password. It must have one special character, only ASCII characters, at least one number, at least one uppercase and one lowercase character, and a length between 8 and 20."):
        User("test@example.com", "Abcd1234!TooLongPassword")
