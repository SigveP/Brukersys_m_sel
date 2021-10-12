from cryptography.fernet import Fernet


def encrypt(string: str) -> tuple:
    key = Fernet.generate_key()
    encrypted_string = Fernet(key).encrypt(string.encode())
    return (encrypted_string, key)


def decrypt(encrypted_string: str, key: str) -> str:
    string = Fernet(key).decrypt(encrypted_string.encode())
    return string.decode()
