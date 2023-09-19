import os

from cryptography.fernet import Fernet


# Function to securely generate a new encryption key
def generate_key() -> bytes:
    return Fernet.generate_key()


# Function to write CLI code to a secure file
def write_secure_cli_code(cli_code: str, file_path: str, key: bytes) -> None:
    cipher_suite = Fernet(key)
    encrypted_code = cipher_suite.encrypt(cli_code.encode())
    with open(file_path, "wb") as f:
        f.write(encrypted_code)


# Function to read CLI code from a secure file
def read_secure_cli_code(file_path: str, key: bytes) -> str:
    with open(file_path, "rb") as f:
        encrypted_code = f.read()
    cipher_suite = Fernet(key)
    decrypted_code = cipher_suite.decrypt(encrypted_code)
    return decrypted_code.decode()


# Test the secure storage and reading of CLI code
def test_secure_storage_and_reading_of_cli_code():
    key = generate_key()
    original_cli_code = (
        '{"commands": [{"name": "create_task", "options": '
        '[{"name": "title", "type": "str"}]}]}'
    )
    file_path = "./secure_cli.py.enc"

    write_secure_cli_code(original_cli_code, file_path, key)
    assert os.path.exists(file_path)

    read_cli_code = read_secure_cli_code(file_path, key)
    assert read_cli_code == original_cli_code
    os.remove(file_path)
