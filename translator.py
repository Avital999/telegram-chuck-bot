import boto3
import langcodes


def language_name_to_iso_code(language_name):
    try:
        code = langcodes.find(language_name).language
        return code
    except langcodes.LanguageNotFoundError:
        return None


def translate_text(text: str, target_language: str) -> str:
    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

    result = translate.translate_text(Text=text,
                                      SourceLanguageCode="en",
                                      TargetLanguageCode=language_name_to_iso_code(target_language))
    print('TranslatedText: ' + result.get('TranslatedText'))
    return result.get('TranslatedText')


translate_text(text='My name is Dana',target_language='Hebrew')
