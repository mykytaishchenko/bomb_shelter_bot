import telebot
from telebot import types

from config import Config
from geocoder import geocode
from shelter_base import Data

conf = Config("data/config.csv")
hide = types.ReplyKeyboardRemove()
data = Data()

bot = telebot.TeleBot(conf.get("token"))


def set_my_commands(commands: list):
    bot.delete_my_commands()
    bot.set_my_commands([telebot.types.BotCommand(f"/{cmd[0]}", cmd[1]) for cmd in commands])


def new_keyword(btns: list):
    keyword = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyword.add(*[types.KeyboardButton(txt) for txt in btns])
    return keyword


@bot.message_handler(commands=["start"])
def start(message):
    msg = '''
    *Слава Україні!*

Я бот-помічник у пошуку найблищого *бомбосховища*.
Для того щоб почати *пошук*, використайте команду _/search_.

_*зараз, на жаль, бот працює лише у Львові._
    '''
    bot.send_message(message.chat.id, msg, reply_markup=hide, parse_mode="markdown")


@bot.message_handler(commands=["search"])
def search_start(message):
    msg = '''
    Спершу, надішліть свою геолокацію за допомогою функції у телеграм, або напишіть її власноруч за зразком.
 
Зразок написання адреси:
_проспект Свободи, 28, Львів, Львівська область_.
    '''
    send = bot.send_message(message.chat.id, msg, reply_markup=hide, parse_mode="markdown")
    bot.register_next_step_handler(send, loc_send)


def loc_send(message, frm=0, to=10):
    if message.text is not None and message.text.startswith("/"):
        return
    if message.location is not None:
        loc = (message.location.latitude, message.location.longitude)
    else:
        loc = geocode(message.text)
        if loc is None:
            msg = '''
            На жаль, ми не могли розпізнати ваше місце розташування, спробуйте задати адресу точніше.
            '''
            send = bot.send_message(message.chat.id, msg, reply_markup=hide, parse_mode="markdown")
            bot.register_next_step_handler(send, loc_send)
            return
    lst = data.closest(loc, frm, to)
    msg = "Ось декілька сховищ, які ми знайшли для вас:\n"
    for el in lst:
        lat_lon = f"{el[0]},{el[1]}"
        msg += f"▹ [{el[2]}](https://www.google.com/maps/place/{lat_lon}).\n"
    bot.send_message(message.chat.id, msg, reply_markup=hide, parse_mode="markdown")
    send = bot.send_message(message.chat.id, "Показати більше варіантів?", reply_markup=new_keyword(["Так", "Ні"]),
                            parse_mode="markdown")
    bot.register_next_step_handler(send, more_search, frm, to)


def more_search(message, frm, to):
    if message.text == "Так":
        loc_send(message, frm + 10, to + 10)
    else:
        bot.send_message(message.chat.id, "Не панікуйте та швидко прямуйте до сховища.", reply_markup=hide,
                         parse_mode="markdown")


@bot.message_handler(commands=["support"])
def support(message):
    msg = '''
    Знайшли у боті помилки або некоректну працю, помітили недійсні сховища або бажаєте доповнити реєстр сховищ - пишіть @nick_ishchenko або @mar1cha.
    
Адреси бомбосховищ взяті з сайту map.city-adm.lviv.ua

_(Повідомляйте команду про не актуальні укриття)_.
    '''
    bot.send_message(message.chat.id, msg, reply_markup=hide)


@bot.message_handler(commands=["important"])
def important(message):
    msg = '''
    *ВАЖЛИВА ІНФОРМАЦІЯ*
    
• 🔰112 — Єдиний номер виклику всіх служб екстреної допомоги. Зателефонуйте за цим номером, і диспетчер викличе бригаду потрібної служби.
• 🚒101 — Пожежна служба
• 👮102 — Поліція
• 🚑103 — Швидка медична допомога
При відсутності лінії 103 швидку допомогу можна викликати за телефонами: 293-29-12; 293-29-14; 293-29-05; 293-29-19; 293-29-16; 293-29-25
• 👨‍🚒104 — Аварійна служба газової мережі


💪телефон довіри СБУ
• 0-800-501-482
• +38-(032)-258-83-33
• +38-(032)-298-66-22


❗️Координаційний центр Штабу оборони Львівщини. Центр займається волонтерською допомогою. 
 +380-63-841-01-39


👉 Знайшли ворожі мітки (хрест, коло) на дорогах і дахах, засипати чи замальовувати та повідомляти в бот, створений Кіберполіцією: https://t.me/ukraine_avanger_bot
👉 зафіксували пересування ворожої техніки і надсилайте в тг-чат @vseodnoikhnesadyat (його читають правоохоронці)


💰 Допомогти фінансово:

Офіційні реквізити спеціального рахунку Нацбанку для сбору коштів на потреби армії: UA843000010000000047330992708
👉 Перерахувати кошти з ЄПідтримки для фонду Повернись живим через Portmone https://bit.ly/3IpXNIm
👉 Задонатити таким фондам як Армія SOS чи Крила Фенікса


🌿Центри психологічної допомоги

• (093)436-67-33 Телефон Довіри (цілодобово)
• (032)276-13-55 (з 9:00 до 18:00) - Львівський міський центр соціальних служб


🔷Яким каналам довіряти

• Канал Верховної Ради України - https://t.me/verkhovnaradaukrainy
• Міністерство оборони України - https://www.facebook.com/MinistryofDefence.UA
• Кабінет міністрів України - https://www.facebook.com/KabminUA
• Телеграм канал Президента України - https://t.me/V_Zelenskiy_official
• Телеграм канал ДСНС - https://t.me/dsns_telegram
• Телеграм канал МВС - https://t.me/mvs_ukraine
• Телеграм канал СБУ - https://t.me/SBUkr


*Слава Україні та нашим Захисникам! Разом переможемо! 🇺🇦*
    '''
    bot.send_message(message.chat.id, msg, reply_markup=hide, parse_mode="markdown")


if __name__ == "__main__":
    set_my_commands(conf.commands)
    # bot.polling(none_stop=True)
