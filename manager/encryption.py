import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

SALT = b"salt_solid"

def generate_key_from_password(password):
    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=1_000_000,
    )
    return base64.urlsafe_b64encode(key.derive(password.encode()))

def encrypt_data(key, data):
    return Fernet(key).encrypt(data.encode())


def decrypt_data(key, encrypted_data):
    return Fernet(key).decrypt(encrypted_data).decode()

# password = "my_password"
# data = "This is my password, do not tell anyone."
#
# key = generate_key_from_password(password)
# print(f"Generated Key: {key}")
#
# encrypted_data = encrypt_data(key, data)
# print(f"Encrypted Data: {encrypted_data}")
#
# decrypted_data = decrypt_data(key, encrypted_data)
# print(f"Decrypted Data: {decrypted_data}")