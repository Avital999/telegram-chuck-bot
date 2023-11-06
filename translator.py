import boto3
import langcodes
from cryptography.fernet import Fernet


def language_name_to_iso_code(language_name):
    try:
        code = langcodes.find(language_name).language
        return code
    except langcodes.LanguageNotFoundError:
        return None


def key_for_encryption():
    with open("encryptionkey.txt", "rb") as key_file:
        encryption_key = key_file.read()
    return encryption_key


def access_key(encryption_key):
    with open("encrypted_keys.txt", "rb") as file:
        lines = file.readlines()

    # Decrypt the AWS access key and decode it to a UTF-8 string
    cipher_suite = Fernet(encryption_key)
    access_key = cipher_suite.decrypt(lines[0].strip()).decode('utf-8')
    return access_key


def secret_key(encryption_key):
    with open("encrypted_keys.txt", "rb") as file:
        lines = file.readlines()

    # Decrypt the AWS secret key and decode it to a UTF-8 string
    cipher_suite = Fernet(encryption_key)
    secret_key = cipher_suite.decrypt(lines[1].strip()).decode('utf-8')
    return secret_key


def translate_text(text: str, target_language: str) -> str:
    """ Given a text and a target language, using AWS translate services,
    translate the given text to the language."""

    encryption_key = key_for_encryption()

    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True,
                             aws_access_key_id=access_key(encryption_key),
                             aws_secret_access_key=secret_key(encryption_key))

    result = translate.translate_text(Text=text,
                                      SourceLanguageCode="en",
                                      TargetLanguageCode=language_name_to_iso_code(target_language))
    translated_text: str = result.get('TranslatedText')
    print(translated_text)
    return translated_text


