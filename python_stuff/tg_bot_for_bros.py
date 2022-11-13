import telebot
import fsm_chat

BotProcessor = fsm_chat.FSM_chat("start")

token = "5697525150:AAGdmO8bX4yTtI1r99_LeTng4_tumzMxpq8"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет")

@bot.message_handler(content_types='text')
def message_reply(message):
    BotProcessor.Process(message)
    bot.send_message(message.chat.id, BotProcessor.GiveMessage())

bot.infinity_polling()
