import json
from .encryption import encrypt_data, decrypt_data, generate_key_from_password

class PasswordManager:
    def __init__(self, account_name, master_password):
        self.account_name = account_name
        self.master_password = master_password
        self.key = generate_key_from_password(f"{account_name}_{master_password}")
        self.passwords = {}

    def add_password(self, name, password):
        self.passwords[name] = password
        self.save_passwords()

    def get_password(self, name):
        return self.passwords.get(name)

    def delete_password(self, name):
        if name in self.passwords:
            del self.passwords[name]
            self.save_passwords()

    def save_passwords(self):
        encrypted_data = encrypt_data(self.key, json.dumps(self.passwords))
        with open(f"passwords_{self.account_name}.enc", "wb") as f:
            f.write(encrypted_data)

    def load_passwords(self):
        try:
            with open(f"passwords_{self.account_name}.enc", "rb") as f:
                encrypted_data = f.read()
            decrypted_data = decrypt_data(self.key, encrypted_data)
            self.passwords = json.loads(decrypted_data)
            return True
        except (FileNotFoundError, ValueError):
            return False

    def export_to_json(self, filename, export_password):
        key = generate_key_from_password(export_password)
        encrypted_data = encrypt_data(key, json.dumps(self.passwords))
        with open(filename, "wb") as f:
            f.write(encrypted_data)

    def import_from_json(self, filename, import_password):
        try:
            with open(filename, "rb") as f:
                encrypted_data = f.read()
            key = generate_key_from_password(import_password)
            decrypted_data = decrypt_data(key, encrypted_data)
            self.passwords = json.loads(decrypted_data)
            self.save_passwords()
        except Exception:
            raise ValueError("Failed to import passwords: incorrect password.")
