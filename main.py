from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from jokes_scraper import chuck_joke
from translator import translate_text


TOKEN: Final = open("bottoken.txt", "r").read().strip("\n")
BOT_USERNAME: Final = '@ch_jokes_bot'


# helpful functions
def set_language(language: str):
    with open('language.txt', "w") as file:
        file.write(language)
    return translate_text(target_language=language, text="no problem")


def send_chuck_joke(joke_number: int):
    # Check if the user already chose a language
    with open('language.txt', "r") as file:
        language = file.read()
    if len(language) == 0:
        return 'please set language first.'

    # Send the joke to the user
    joke: str = chuck_joke(joke_number)
    translated_joke: str = translate_text(text=joke, target_language=language)
    return translated_joke


# Commands
async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! Wanna hear a joke?")


async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("fulfill later the command.")


# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'set language' in processed:
        return set_language(language=processed[13:])

    if processed.isnumeric():
        joke_number = int(processed)
        if 1 < joke_number < 25:
            return send_chuck_joke(joke_number)
        else:
            return 'In case you wanna hear a joke, please choose number between 1 and 25.'

    return 'I do not understand you. you can set langauge X or choose a number between 1 to 25 to get a joke!'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id} in {message_type}: "{text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '')
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
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
