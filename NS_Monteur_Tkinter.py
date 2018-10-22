import telepot

bot = telepot.Bot("635183711:AAHNPw-eMij4zJGZuG0OZNWdtquLgrRj5RA")


def send_message(chat_id, message):
    bot.sendMessage(chat_id, message)
