import boto3
import langcodes
from keys import access_key,secret_key


def convert_language_name_to_iso_code(language_name):
    try:
        code = langcodes.find(language_name).language
        return code
    except Exception:
        return None


def language_exists(language):
    return convert_language_name_to_iso_code(language) is not None


def translate_text(text: str, target_language: str) -> str:
    translator = create_boto3_client()

    result = translator.translate_text(Text=text,
                                       SourceLanguageCode="en",
                                       TargetLanguageCode=convert_language_name_to_iso_code(target_language))

    translated_text: str = result.get('TranslatedText')
    print(translated_text)
    return translated_text


def create_boto3_client():
    return boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True,
                        aws_access_key_id=access_key(),
                        aws_secret_access_key=secret_key())


