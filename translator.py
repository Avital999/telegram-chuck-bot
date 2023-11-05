import os

import boto3
import langcodes
from secret import aws_secret_access_key, aws_access_key_id


def language_name_to_iso_code(language_name):
    try:
        code = langcodes.find(language_name).language
        return code
    except langcodes.LanguageNotFoundError:
        return None


def translate_text(text: str, target_language: str) -> str:
    """ Given a text and a target language, using AWS translate services,
    translate the given text to the language."""

    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True,
                             aws_access_key_id=aws_access_key_id(),
                             aws_secret_access_key=aws_secret_access_key())

    result = translate.translate_text(Text=text,
                                      SourceLanguageCode="en",
                                      TargetLanguageCode=language_name_to_iso_code(target_language))
    translated_text: str = result.get('TranslatedText')
    print(translated_text)
    return translated_text

