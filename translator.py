import boto3
import langcodes
from keys import access_key,secret_key


def language_name_to_iso_code(language_name):
    try:
        code = langcodes.find(language_name).language
        return code
    except Exception:
        return None


def language_exists(language):
    return language_name_to_iso_code(language) is not None


def translate_text(text: str, target_language: str) -> str:
    """ Given a text and a target language, using AWS translate services,
    translate the given text to the language."""


    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True,
                             aws_access_key_id=access_key(),
                             aws_secret_access_key=secret_key())

    result = translate.translate_text(Text=text,
                                      SourceLanguageCode="en",
                                      TargetLanguageCode=language_name_to_iso_code(target_language))
    translated_text: str = result.get('TranslatedText')
    print(translated_text)
    return translated_text


