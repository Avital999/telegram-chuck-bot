import boto3
import langcodes


def is_rtl_language(language):
    rtl_languages = ['arabic', 'hebrew', 'persian', 'urdu', 'yiddish', 'sindhi',
                     'dhivehi', 'pashto', 'kurdish', 'sorani', 'kurmanji', 'uighur', 'jawi', 'thaana']
    return language.lower() in rtl_languages


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
    translated_text: str = result.get('TranslatedText')
    if is_rtl_language(target_language):
        translated_text = translated_text[::-1]
    print(translated_text)
    return translated_text


