import time
import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from settings import *
from logic import Person

bot = telebot.TeleBot(bot_token)

person_info = {}


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 'Вы попали в отдел помощи навигации по боту! Доступные команды:\n/start - приветствие бота и инструкция')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 'Здравствуйте! Для начала мне потребуется узнать некоторую информацию о Вас для того, чтобы решить, как Вы можете изменить свою карьеру! 📝\nМне потребуется: текущая должность, предпочтения, ощущения от работы и некоторые детали по желанию.')

    keyboard = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text="Да", callback_data='yes')
    b2 = InlineKeyboardButton(text="Нет", callback_data='no')
    keyboard.add(b1)
    keyboard.add(b2)
    bot.send_message(
        message.chat.id, 'Готовы ли Вы сейчас ответить на некоторые вопросы?', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_answer)


@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    if call.data == "yes":
        time.sleep(1)
        bot.send_message(call.message.chat.id, 'Хорошо, давайте начнем 🔥\nКакая у Вас сейчас должность 💼?')
        bot.register_next_step_handler(call.message, job_handler)
    elif call.data == "no":
        time.sleep(1)
        bot.send_message(call.message.chat.id, "Без проблем, я буду ждать Вас.")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.delete_message(call.message.chat.id, call.message.message_id - 1)


def job_handler(message):
    bot.reply_to(message, 'Интересная профессия! Перейдем ко второму вопросу.')
    person_info[message.chat.id] = {"job": message.text}
    bot.send_message(message.chat.id,
                     'Какие у Вас интересы? (рисование, программирование, черчение)\nМожете написать несколько хобби.', )
    bot.register_next_step_handler(message, interests_handler)


def interests_handler(message):
    bot.reply_to(message, 'Отлично! Перейдем к третьему вопросу.')
    person_info[message.chat.id]["interests"] = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = KeyboardButton('Хорошие')
    itembtn2 = KeyboardButton('Плохие')
    itembtn3 = KeyboardButton('По-разному')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id,
                     'Какие у Вас ощущение от работы и все, что с ней связано? (хорошие, плохие, по-разному).',
                     reply_markup=markup)
    bot.register_next_step_handler(message, feelings_handler)


def feelings_handler(message):
    bot.reply_to(message,
                 'Отлично! Перейдем к последнему вопросу. Какие у Вас мысли и общие ощущения, которые возникают в процессе работы 🧘?',
                 reply_markup=ReplyKeyboardRemove())
    person_info[message.chat.id]["feelings"] = message.text
    bot.register_next_step_handler(message, general_info_handler)


def general_info_handler(message):
    person_info[message.chat.id]["general"] = message.text
    person_data = person_info.pop(message.chat.id)
    person.info(message.from_user.id, person_data["job"], person_data["interests"], person_data["feelings"],
                person_data["general"])
    sent_message = bot.reply_to(message,
                                'Спасибо! Ваша информация добавлена в базу данных.\nПриступил к приготовлению информации для Вас')

    # Эффект загрузки
    loading_text = 'Спасибо! Ваша информация добавлена в базу данных.\nПриступил к приготовлению информации для Вас'
    for _ in range(5):
        for dots in range(3, 0, -1):
            bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                  text=loading_text + "." * dots)
            time.sleep(1)

    # Отправляем финальное сообщение
    bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                          text='Финальное сообщение')


if __name__ == '__main__':
    person = Person('database.db')
    person.create_tables()
    bot.infinity_polling()
