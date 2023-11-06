from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from jokes_scraper import chuck_joke
from translator import translate_text
import json
import csv
import os


TOKEN: Final = open("bottoken.txt", "r").read().strip("\n")
BOT_USERNAME: Final = '@ch_jokes_bot'


# helpful functions
def add_language(user_id: int, language):
    # Define the file path
    file_path = 'languages.csv'

    # Check if the CSV file already exists, and create it if not
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as csv_file:
            fieldnames = ['user_id', 'language']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

    # Open the CSV file for reading and create a list of dictionaries from its contents
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)

    # Flag to check if the user_id exists in the CSV
    user_id_exists = False

    # Find the matching row and update it if user_id exists
    for row in data:
        if int(row['user_id']) == user_id:
            row['language'] = language
            user_id_exists = True
            break

    # If user_id doesn't exist, add a new row
    if not user_id_exists:
        data.append({'user_id': str(user_id), 'language': language})

    # Write the updated data back to the CSV file
    with open(file_path, 'w', newline='') as csv_file:
        fieldnames = ['user_id', 'language']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)

    return translate_text(target_language=language, text="no problem")


def send_chuck_joke(joke_number: int, user_id: int):
    # Define the file path
    file_path = 'languages.csv'

    # Check if the CSV file exists and user_id exists in the CSV
    if not os.path.exists(file_path):
        return 'Please set language first'

    # Read the CSV file and search for the user_id
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if int(row['user_id']) == user_id:
                language = row['language']
                joke = chuck_joke(joke_number)
                translated_joke = translate_text(text=joke, target_language=language)
                return translated_joke

    # If user_id doesn't exist in the CSV, return 'Please set language first'
    return 'Please set language first'


# Commands
async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! Wanna hear a joke? set a language and choose a number between 1 and 25.")


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

    if 'set language' in text:
        return add_language(user_id=int(user_id), language=text[13:])

    if text.isnumeric():
        joke_num = int(text)
        if 1 < joke_num < 25:
            return send_chuck_joke(joke_num,user_id=int(user_id))
        else:
            return 'In case you wanna hear a joke, please choose number between 1 and 25.'

    return 'I do not understand you. you can set langauge X or choose a number between 1 to 25 to get a joke!'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user_id:int = update.message.chat.id

    print(f'User ({update.message.chat.id} in {message_type}: "{text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '')
            response: str = handle_response(new_text,user_id=user_id)
        else:
            return
    else:
        response: str = handle_response(text, user_id=user_id)
    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


def main():
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

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
