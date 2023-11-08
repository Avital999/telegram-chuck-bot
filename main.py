from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from jokes_scraper import scrape_jokes_from_website
from translator import translate_text, language_exists
from manage_lanagues import create_csv,update_user_preferred_language,LANGUAGES_CSV
import csv
import os


BOT_USERNAME = '@ch_jokes_bot'


# helpful functions

def add_language(user_id: int, language):
    update_user_preferred_language(user_id=user_id, language=language)
    return translate_text(target_language=language, text="no problem")


def translate_joke(joke, language):
    return translate_text(text=joke, target_language=language)


def get_language_from_user_id(user_id):
    with open(LANGUAGES_CSV, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if int(row['user_id']) == user_id:
                return row['language']
    return None

def send_chuck_joke(joke_number: int, user_id: int):
    joke = scrape_jokes_from_website()[joke_number - 1]
    language = get_language_from_user_id(user_id)
    if not language:
        return 'Please set language first'

    translated_joke = translate_joke(joke=joke, language=language)
    return translated_joke


# Commands
async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    start_message = ("Hey! Want to hear a Chuck Norris joke? \U0001F604\n"
                     "Set a language and choose a number between 1 and 25.\n"
                     "For instructions, you can enter /help. \U0001F50D")
    await update.message.reply_text(start_message)


async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    friendly_message = ("\U0001F44B Hello! I'm a bot that shares Chuck Norris jokes."
                        "\nTo get started, follow these steps:\n\n"
                        "1. Set your preferred language by typing 'set language X' and pressing Enter. "
                        "Replace 'X' with the language you want to choose.\n\n"
                        "2. Once you've set your language, select a number between 1 and 25, hit Enter, "
                        "and you'll receive a Chuck Norris joke in your chosen language. \n"
                        "\nEnjoy the laughter! \U0001F604")
    await update.message.reply_text(friendly_message)


# Responses
def handle_response(text: str, user_id:int) -> str:
    text = text.lower()

    if text.startswith('set language'):
        language = text[13:]
        if not language_exists(language):
            return 'This language does not exists. Please choose an existing language!'
        return add_language(user_id=int(user_id), language=language)

    if text.isnumeric():
        joke_num = int(text)
        if 1 <= joke_num <= 25:
            return send_chuck_joke(joke_num,user_id=int(user_id))
        else:
            return 'Ready for a joke? Please choose a number between 1 and 25! \U0001F604'

    return 'I do not understand you. Please press /help for instructions.'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user_id:int = update.message.chat.id

    print(f'User ({update.message.chat.id} in {message_type}: "{text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '')
            response: str = handle_response(new_text, user_id=user_id)
        else:
            return
    else:
        response: str = handle_response(text, user_id=user_id)
    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


def main():
    if not os.path.exists(LANGUAGES_CSV):
        create_csv()

    bot_token = input("Please enter your token: ")
    temp_encryption_key = input("Please enter encryption key: ")
    with open('tempkey.txt', 'w') as file:
        file.write(temp_encryption_key)

    print('Starting bot...')
    app = Application.builder().token(bot_token).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=2)


if __name__ == "__main__":
    main()
