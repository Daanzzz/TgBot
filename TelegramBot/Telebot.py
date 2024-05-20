import os
import telebot
import hashlib

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

GUIDE_MESSAGE = '𝐆𝐔𝐈𝐃𝐄: Upload a JPG/JPEG file, and I will calculate its hash for you!'
ERROR_MESSAGE = '𝐄𝐫𝐫𝐨𝐫: only JPG/JPEG files allowed!'
FILE_PROCESS_ERROR = 'An error occurred while processing the file.'

def calculate_md5(photo_data):
    """
    calculate_md5 function calculates the md5
    hash of a data passed to it, and returns it.

    :photo_data: the data itself
    :return: the data after hash
    """

    md5_hash = hashlib.md5(photo_data).hexdigest()
    return md5_hash

@bot.message_handler(content_types=['document', 'photo'])
def handle_file(message):
    """
    handle_file is a function that is responsible for
    handling messages that include a document/photo, it analyzes
    them and replies if they're valid or not.

    :message: the message of the user
    """

    try:
        if message.document:
            file_info = message.document
        elif message.photo:
            file_info = message.photo[-1]
       
        file_id = file_info.file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # checking if file is valid
        if file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            downloaded_file = bot.download_file(file_info.file_path)
            md5_hash = calculate_md5(downloaded_file)

            bot.reply_to(message, f"The MD5 hash of the photo is: {md5_hash}")
        else:
            bot.reply_to(message, ERROR_MESSAGE)
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        bot.reply_to(message, FILE_PROCESS_ERROR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    send_welcome function is responsible for
    replying to the /start command when starting a 
    chat with the bot
    """

    bot.reply_to(message, GUIDE_MESSAGE)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    """
    echo_all is responsible for replying to any normal messages
    (messages without document/photo/start command) and respond
    with an error message.
    """

    bot.reply_to(message, ERROR_MESSAGE)

bot.infinity_polling()
