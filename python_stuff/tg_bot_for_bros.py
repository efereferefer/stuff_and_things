import telebot

token = "5697525150:AAGdmO8bX4yTtI1r99_LeTng4_tumzMxpq8"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])

def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️ ")

bot.infinity_polling()
