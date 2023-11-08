from cryptography.fernet import Fernet
import os

ENCRYPTED_KEYS_PATH = "encrypted_keys.txt"

encrypted_secret_key_position = 1
encrypted_access_key_position = 0


def get_aws_access_key():
    encryption_key = get_key_for_encrption()
    return decrypt_key_from_file(encryption_key,encrypted_access_key_position)


def get_aws_secret_key():
    encryption_key = get_key_for_encrption()
    return decrypt_key_from_file(encryption_key, encrypted_secret_key_position)


def get_key_for_encrption():
    with open(get_name_of_file_with_encryption_key(), "rb") as key_file:
        encryption_key = key_file.read()
    return encryption_key


def get_name_of_file_with_encryption_key():
    first_file = 'encryptionkey.txt'
    second_file = 'tempkey.txt'

    if os.path.exists(first_file):
        return first_file
    return second_file


def decrypt_key_from_file(encryption_key, position):
    with open(ENCRYPTED_KEYS_PATH, "rb") as file:
        lines = file.readlines()
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.decrypt(lines[position].strip()).decode('utf-8')


