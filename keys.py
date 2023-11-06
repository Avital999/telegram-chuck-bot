from cryptography.fernet import Fernet


def key_for_encryption():
    with open("encryptionkey.txt", "rb") as key_file:
        encryption_key = key_file.read()
    return encryption_key


def access_key():
    encryption_key = key_for_encryption()

    with open("encrypted_keys.txt", "rb") as file:
        lines = file.readlines()

    # Decrypt the AWS access key and decode it to a UTF-8 string
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.decrypt(lines[0].strip()).decode('utf-8')


def secret_key():
    encryption_key = key_for_encryption()

    with open("encrypted_keys.txt", "rb") as file:
        lines = file.readlines()

    # Decrypt the AWS secret key and decode it to a UTF-8 string
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.decrypt(lines[1].strip()).decode('utf-8')