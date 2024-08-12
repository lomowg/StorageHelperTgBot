from cryptography.fernet import Fernet

key = Fernet.generate_key().decode()
print(key)
