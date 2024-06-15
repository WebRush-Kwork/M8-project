import time
import os
import telebot
from g4f.client import Client
from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from deep_translator import GoogleTranslator
from logic import Person
from settings import *

bot = telebot.TeleBot(bot_token)

person_info = {}
prompt = ''


def ai_answer(question):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 'Вы попали в отдел помощи навигации по боту! Доступные команды:\n/start - приветствие бота и инструкция 📝\n/info - информация о пользователе, если она была занесена ℹ️\n/help - возможности бота, навигация 🧭')


@bot.message_handler(commands=['start'])
def start(message):
    if os.path.exists('database.db'):
        keyboard1 = InlineKeyboardMarkup()
        b3 = InlineKeyboardButton(text="Да", callback_data='yes-start')
        b4 = InlineKeyboardButton(text="Нет", callback_data='no-start')
        keyboard1.add(b3)
        keyboard1.add(b4)
        bot.reply_to(message, "Вы уже вводили свои данные. Хотите обновить информацию?", reply_markup=keyboard1)
    else:
        person.create_tables()
        bot.reply_to(message,
                     'Здравствуйте! Для начала мне потребуется узнать некоторую информацию о Вас для того, чтобы решить, как Вы можете изменить свою карьеру! 🌎📝\n\nМне потребуется: текущая профессия, предпочтения, ощущения от работы и некоторые детали по желанию.')

        keyboard = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text="Да", callback_data='yes')
        b2 = InlineKeyboardButton(text="Нет", callback_data='no')
        keyboard.add(b1)
        keyboard.add(b2)
        time.sleep(1)
        bot.send_message(
            message.chat.id, 'Готовы ли Вы сейчас ответить на некоторые вопросы?', reply_markup=keyboard)


def job_handler(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_message(message.chat.id,
                     'Интересная профессия! Перейдем ко второму вопросу. \nКакие у Вас интересы 🎨🎤? Можете написать несколько хобби 🔢')
    person_info[message.chat.id] = {"job": message.text}
    bot.register_next_step_handler(message, interests_handler)


def interests_handler(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)

    person_info[message.chat.id]["interests"] = message.text
    markup = InlineKeyboardMarkup(row_width=3)
    itembtn1 = InlineKeyboardButton('👍', callback_data='good')
    itembtn2 = InlineKeyboardButton('👎', callback_data='bad')
    itembtn3 = InlineKeyboardButton('🤷‍', callback_data='mixed')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id,
                     'Отлично! Перейдем к третьему вопросу. \nКакие у Вас ощущение от работы и все, что с ней связано 🧐?',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["yes-start", "no-start"])
def handle_yes_no_start_callback(call):
    if call.data == "yes-start":
        os.remove('database.db')
        start(call.message)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "no-start":
        bot.send_message(call.message.chat.id, 'Без проблем, я буду ждать Вас 🕒')
        time.sleep(1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        return


@bot.callback_query_handler(func=lambda call: call.data in ["yes", "no"])
def handle_yes_no_callback(call):
    if call.data == "yes":
        bot.reply_to(call.message, 'Хорошо, давайте начнем 🔥\nКакая у Вас сейчас профессия 💼?')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        bot.register_next_step_handler(call.message, job_handler)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Без проблем, я буду ждать Вас 🕒")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)


@bot.callback_query_handler(func=lambda call: call.data in ['good', 'bad', 'mixed'])
def handle_feelings_callback(call):
    if call.data == 'good':
        person_info[call.message.chat.id]["feelings"] = 'Хорошие'
        bot.delete_message(call.message.chat.id, call.message.message_id)
        feelings_handler(call.message)
    elif call.data == 'bad':
        person_info[call.message.chat.id]["feelings"] = 'Плохие'
        bot.delete_message(call.message.chat.id, call.message.message_id)
        feelings_handler(call.message)
    elif call.data == 'mixed':
        person_info[call.message.chat.id]["feelings"] = 'По-разному'
        bot.delete_message(call.message.chat.id, call.message.message_id)
        feelings_handler(call.message)


def feelings_handler(message):
    bot.send_message(message.chat.id,
                     'Отлично! Перейдем к последнему вопросу. \nКакие мысли Вас сопровождают в процессе работы 🧘?',
                     reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, lambda msg: general_info_handler(msg))


def general_info_handler(message):
    global prompt
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    person_info[message.chat.id]["general"] = message.text
    person_data = person_info.pop(message.chat.id)
    person.info(message.from_user.id, person_data["job"], person_data["interests"], person_data["feelings"],
                person_data["general"])
    prompt = f'Моя профессия: {person_data["job"]}. \nМои интересы: {person_data["interests"]}. \nМои ощущение от работы: {person_data["feelings"]}. \nМои мысли во времы работы: {person_data["general"]}. \nЯ хочу сменить род деятельности. Какие профессии или хобби можешь посоветовать?'
    sent_message = bot.send_message(message.chat.id,
                                    'Спасибо! Ваша информация добавлена в базу данных.\nПриступил к приготовлению ответа для Вас')

    loading_text = 'Спасибо! Ваша информация добавлена в базу данных.\nПриступил к приготовлению ответа для Вас'
    for _ in range(5):
        for dots in range(3, 0, -1):
            bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                  text=loading_text + "." * dots)
            time.sleep(0.3)

    translated = GoogleTranslator(source='auto', target='en').translate(prompt)
    ai_eng = ai_answer(translated)
    ai_rus = GoogleTranslator(source='auto', target='ru').translate(ai_eng)

    bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=ai_rus)


@bot.message_handler(commands=['info'])
def show_info(message):
    bot.send_message(message.chat.id, person.get_person_info(message.chat.id))


if __name__ == '__main__':
    person = Person('database.db')
    bot.infinity_polling()
