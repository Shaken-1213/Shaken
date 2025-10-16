import telebot
import random
import threading, time, schedule
import os
import requests
from telebot import TeleBot, types

def get_pokemon_image_url():
    url = 'https://pokeapi.co/api/v2/pokemon-form/132/'
    res = requests.get(url)
    data = res.json()
    return data['sprites']['front_default']


def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


def flip_coin():
    return random.choice(['Орёл', 'Решка'])


def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>123456789"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password


bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2) 
    itembtn1 = types.InlineKeyboardButton('info', callback_data ='info')  
    itembtn2 = types.InlineKeyboardButton('bye', callback_data ='bye')   
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, "Привет!", reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "info":
        bot.send_message(call.message.chat.id, "/bye - пока \n/about - про бота \n/password - создает пароль\n/emoji - рандомный эмоджи \n/set - таймер\n/unset - откл. таймер\n/coin - подбрасывает монетку\n/duck - фото утки\n/pokemon - фото покемона\n/meme - мем")
    elif call.data == "bye":
        bot.send_message(call.message.chat.id, "Пока! Удачи!")
        


@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")


def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Beep!')


@bot.message_handler(commands=['emoji'])
def send_emoji(message):
    emojis = ['😀', '😎', '🙂', '😡']
    emoji = random.choice(emojis)
    bot.reply_to(message, "Вот твой эмоджи: " + emoji)
    return emoji


@bot.message_handler(commands=['duck'])
def duck(message):
    image_url = get_duck_image_url()
    bot.reply_to(message, image_url)


@bot.message_handler(commands=['pokemon'])
def send_pokemon(message):
    image_url = get_pokemon_image_url()
    bot.reply_to(message, image_url)


@bot.message_handler(commands=['meme'])
def send_mem(message):
    images = os.listdir('meme2')
    name = random.choice(images)
    with open(f'meme2/{name}', 'rb') as f:
        bot.send_photo(message.chat.id, f)


@bot.message_handler(commands=['advice'])
def send_advice(message):
    advices = ["Хочешь изменить мир? Начни с мусорки.",
               "Экология  — это наука о жизни и её «доме»",
               "Один человек может начать большие перемены.",
               "Оставь природу чище, чем нашёл.",
               "Пешком или на велике — чище воздух."]
    advices1 = random.choice(advices)
    bot.reply_to(message, advices1)
    return advices1


@bot.message_handler(commands=["joke"])
def send_joke(message):
    joke = ["Сибирские экологи забили тревогу. Насмерть.",
            """Армянское радио спрашивают:
             — Что едят людоеды-вегетарианцы?
             — Мы точно не знаем, но думаем, что гринписовцев…""",
            "— А речка какая у нас! Вот внук у меня фотографией увлекся — так прямо в этой речке пленку и проявляет. Красота!!!",
            "Вчера на штат Колорадо обрушился небывалый ураган. Разрушены дома, уничтожены посевы. По сообщению местных экологов ни один жук не пострадал.",
            """Очень богата фауна Полесья. Здесь насчитывается до 16 тысяч видов животных. Одних комаров, например, 15 с половиной тысяч видов."""
            ]
    joke1 = random.choice(joke)
    bot.reply_to(message, joke1)
    return joke1


@bot.message_handler(commands=['poems'])
def send_poems(message):
    poems = ["""

            Когда фантик бросишь мимо урны,
            Иль в реку сток ядовитый хлынет,
            Думаешь: Мелочь, не стоит суеты! —
            Но планета от мелочей этих стонет.
            Нефтяная плёнка на синей воде,
            Где чайки бьются в предсмертной агонии,
            Это — шрамы на её теле,
            Результат нашего страшного забвья.
            Неужели мы просто жильцы-нахлебники,
            Что выжмем природу, как лимон, до дна?
            Чтобы выжить, нам нужны не только технологии,
            А чистая река, леса и луна.
            Так давай же с тобой попробуем
            Этот мир бережней хранить.
            С фантиком в кулаке к урне дойдём,
            Будем воду и свет экономить.
            Чтоб планета, наш общий зелёный причал,
            Для потомков твоих уцелела,
            Чтоб она и для них излучала
            Ту же силу, любовь и тепло!
            """,

             """
             Мы дышим не просто каким-то воздухом,
             А тем, что листва вырастила.
             Мы пьём не H2O по расчётам мудрёным,
             А дождь, что туча нам принесла.
             Мы строим дома, мы кроим дороги,
             Роя под небом траншеи.
             И мним себя Богами, забыв о тревоге,
             Что рушим мы дом свой, спеша и спеша.
             Но время пришло оглянуться назад,
             Увидеть, что мы натворили.
             Ведь каждый пластиковый стаканчик подряд —
             Удар по планете, что нас приютила.
             Не стоит считать, что один — не воин,
             Что глобально — решат другие.
             Твой шаг — это камень, что, в воду покоем,
             Расходится ритмом живым.
             Посадишь деревце, сдашь батарейку,
             Пакет откажешься брать в супермаркете.
             И мир отзовётся зелёной улыбкой,
             Подарив чистоту на планете.
             Чтоб утром просыпаться с птицами, а не с гудками,
             И видеть в окне не дым, а сирень.
             Верни ей долги не словами, а делами —
             И Земля станет настоящею матерью вновь, каждый день.
             """,
             """
             Проснись, человек, венец природы,
             Ты царь, но в ответе за каждый свой шаг.
             Ты больше не можешь ждать от свободы
             Прощенья за горы измусоренных благ.
             Твои города задыхаются в дыме,
             А реки несут не воду, а яд.
             Уже не укрыться нигде от проблемы,
             Которую создал ты сам, и не рад.
             Возьми же мешок, убери у дороги
             То, что бездумно когда-то разбросал.
             Сажай не для вида, а чтобы берёзы
             Шумели для внуков, им счастье предвещал.
             Ведь мир этот хрупок, как тонкое стекло,
             И трещина в нём уже пробежала.
             Чтоб жизнь на Земле не угасла светло,
             Её защитить наша главная стала задача!
             """
             ]
    poems1 = random.choice(poems)
    bot.reply_to(message, poems1)
    return poems1


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)
    bot.reply_to(message,"Таймер остановлен ✅")


@bot.message_handler(commands=['password'])
def send_password(message):
    password = gen_pass(8)
    bot.reply_to(message, f"Пароль создан ✅\nТвой пароль: {password}")



@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "/bye - пока \n/about - про бота \n/password - создает пароль\n/emoji - рандомный эмоджи \n/set - таймер\n/unset - откл. таймер\n/coin - подбрасывает монетку\n/duck - фото утки\n/pokemon - фото покемона\n/meme - мем")


@bot.message_handler(commands=['about'])
def send_about(message):
    bot.reply_to(message, "Creator: Shaken \nBots name:@horoshikzbot \nPractic bot\nVersion 1.0")


@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    
    


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
