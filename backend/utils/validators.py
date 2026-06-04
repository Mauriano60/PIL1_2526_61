import re

def is_valid_email(email):
    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    return bool(re.match(pattern, email))

def is_valid_password(password):
    return len(password) >= 8
