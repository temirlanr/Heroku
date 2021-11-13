import logging
import os
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))

# Hide the telegram bot token
TOKEN = os.environ["TOKEN"]

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def get_last_post():
    """Gets the info about the last post"""
    url = "https://instagram40.p.rapidapi.com/account-feed"

    querystring = {"username":"student_council_nis_kst"}

    headers = {
        'x-rapidapi-host': "instagram40.p.rapidapi.com",
        'x-rapidapi-key': "75a080a24bmsh79caf9b2328fd8dp167288jsn32cf0cdfd80d"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    last_post = response.json()[0]

    text = last_post['node']['edge_media_to_caption']['edges'][0]['node']['text']
    shortcode = last_post['node']["shortcode"]

    return text + "\nСсылка на инстаграм пост: https://www.instagram.com/p/" + shortcode


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет! Я тут чтобы помочь. Отправь /help для справки по боту.')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
    """
    Привет еще раз! У меня есть несколько команд:
    /help - это сообщение которое вы сейчас читаете, тут справка по командам и функциям бота
    /ig - отправляет вам последний пост в инстаграме Student Council
    /suggestion - если у вас есть предложения по улучшению нашей школы, мы будем рады вас выслушать
    /complaint - если вас что-то не устраивает в нашей школе, пишите с этой командой
    /question - если у вас есть вопрос к Student Council, задавайте сюда
    /bot_feedback - любые предложение/жалобы/вопросы/благодарности по боту
    Последние 4 команды должны быть в формате /(команда) текст. Например, /suggestion хотелось бы провести киновечер.
    В других случаях я отправляю ваши сообщения в группу NIS Kostanay Counselling, где вы сможете анонимно поделиться какой-либо проблемой с волонтерами и психологами, которые присутствуют в этой группе и готовы вам оказать психологическую поддержку. 
    Просьба отправлять ваши сообщения в одном длинном тексте, чтобы предотвратить флуд и спам. Заранее благодарим!
    """
    )


def suggestion(update, context):
    """Handles the /suggestion command"""
    context.bot.send_message(chat_id=-1001096346677, text=update.message.text)


def complaint(update, context):
    """Handles the /complaint command"""
    context.bot.send_message(chat_id=-1001096346677, text=update.message.text)


def question(update, context):
    """Handles the /question command"""
    context.bot.send_message(chat_id=-1001096346677, text=update.message.text)


def bot_feedback(update, context):
    """Handles the /bot_feedback command"""
    context.bot.send_message(chat_id=-1001096346677, text=update.message.text)


def ig(update, context):
    """Send the last instagram post when the command /ig is issued"""
    update.message.reply_text(get_last_post())


def redirect(update, context):
    """Redirect the user message."""
    context.bot.send_message(chat_id=-1001248260165, text=update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ig", ig))
    dp.add_handler(MessageHandler(Filters.command, suggestion))
    dp.add_handler(MessageHandler(Filters.command, complaint))
    dp.add_handler(MessageHandler(Filters.command, question))
    dp.add_handler(MessageHandler(Filters.command, bot_feedback))

    # on noncommand i.e message - redirect the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & (~Filters.chat([-1001248260165, -1001096346677])), redirect))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://niskostanaycounsellingbot.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
