import time
import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from settings import *

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 'Здравствуйте! Для начала мне потребуется узнать некоторую информацию о Вас для того, чтобы решить, как Вы можете изменить свою карьеру! 📝\nМне потребуется: текущая должность, предпочтения, ощущения от работы и некоторые детали по желанию.')

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('Да'))
    markup.add(KeyboardButton('Нет'))

    bot.send_message(
        message.chat.id, 'Готовы ли Вы сейчас ответить на некоторые вопросы?', reply_markup=markup)
    bot.register_next_step_handler(message, handle_answer)


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 'Вы попали в отдел помощи навигации по боту! Доступные команды:\n/start - приветствие бота и инструкция')


def handle_answer(message):
    if message.text == "Да":
        bot.reply_to(message, 'Хорошо, давайте начнем 🔥\nКакая у Вас сейчас должность 💼?',
                     reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, interests_handler)
    elif message.text == "Нет":
        bot.reply_to(message, "Без проблем, я буду ждать Вас.", reply_markup=ReplyKeyboardRemove())


def interests_handler(message):
    bot.reply_to(message, 'Интересная профессия! Перейдем ко второму вопросу.')
    time.sleep(1)
    bot.send_message(message.chat.id,
                     'Какие у Вас интересы? (рисование, программирование, черчение)\nМожете написать несколько хобби.', )
    bot.register_next_step_handler(message, feelings)


def feelings(message):
    bot.send_message(message.chat.id, 'Отличные хобби! Перейдем к третьему вопросу.',
                     reply_markup=ReplyKeyboardRemove())
    time.sleep(1)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = KeyboardButton('Хорошие')
    itembtn2 = KeyboardButton('Плохие')
    itembtn3 = KeyboardButton('По-разному')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id,
                     'Какие у Вас ощущение от работы и все, что с ней связано? (хорошие, плохие, по-разному).',
                     reply_markup=markup)
    bot.register_next_step_handler(message, general)


def general(message):
    global good
    bot.reply_to(message, 'Отлично! Перейдем к последнему вопросу.', reply_markup=ReplyKeyboardRemove())

    # bot.register_next_step_handler(message, general)


bot.infinity_polling()
