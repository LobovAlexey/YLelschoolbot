import telebot
from elschool import to_str, get_diary
from data.db_session import add_user, get_user, delete_user, global_init

token: str
bot = telebot.TeleBot(token)
global_init('db/users.db')


@bot.message_handler(commands=['start'])
def button_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    reg_button = telebot.types.KeyboardButton("/reg")
    del_button = telebot.types.KeyboardButton("/del")
    markup.add(reg_button)
    markup.add(del_button)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(commands=['reg'])
def log_in(message):
    bot.send_message(message.chat.id,
                     "Введите ваш логин, пароль и код (натуральное число от 1 до 50) через пробел, число надо будет запомнить")
    bot.register_next_step_handler(message, get_data)


def get_data(message):
    data = message.text.split()
    login, password, secret_key = data
    add_user(login, password, secret_key, message.chat.id)
    bot.send_message(message.chat.id, "Запись успешно создана")


@bot.message_handler(commands=['del'])
def delete(message):
    try:
        delete_user(message.chat.id)
        bot.send_message(message.chat.id, "Запись успешно удалена")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Произошла ошибка. Проверьте корректность введённых данных.")


@bot.message_handler(content_types=['text'])
def start_message(message):
    if len(message.text.split()) == 2:
        login, password = message.text.split()
        try:
            ans = to_str(get_diary(login, password, logging=(bot, message.chat.id)))
            bot.send_message(message.chat.id, ans)
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "Произошла ошибка. Проверьте корректность введённых данных.")
    elif len(message.text.split()) == 1:
        try:
            login, password = get_user(message.chat.id, message.text)
            ans = to_str(get_diary(login, password, logging=(bot, message.chat.id)))
            bot.send_message(message.chat.id, ans)
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "Произошла ошибка. Проверьте корректность введённых данных.")
    else:
        bot.send_message(message.chat.id, "Произошла ошибка. Проверьте корректность введённых данных.")


if __name__ == '__main__':
    bot.polling()
