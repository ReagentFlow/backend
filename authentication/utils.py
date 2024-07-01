import secrets


def generate_unique_string(length=8):
    return secrets.token_hex(length // 2)
