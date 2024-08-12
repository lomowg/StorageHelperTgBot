from cryptography.fernet import Fernet


def encrypt_message(message: str, key: bytes) -> bytes:
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message


def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message
