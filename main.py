import telebot
import random
import schedule
import threading
import time
import os
import requests


def get_pokemon_image_url():
    url = 'https://pokeapi.co/api/v2/pokemon-form/132/'
    res = requests.get(url)
    data = res.json()
    return data['url']

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

bot = telebot.TeleBot("Token")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я bot. Напиши что-нибудь!")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

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
def pokemon(message):
    image_url = get_pokemon_image_url()
    bot.reply_to(message, image_url)

@bot.message_handler(commands=['meme'])
def send_mem(message):
    with open('meme2/meme(1).jpeg', 'rb') as f:
        bot.send_photo(message.chat.id, f)

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

@bot.message_handler(commands=['meme'])
def send_mem(message):
    names = os.listdir('meme2')
    name = random.choice(names)
    with open(f'meme2/{name}', 'rb') as f:
        bot.send_photo(message.chat.id, f)


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)

@bot.message_handler(commands=['password'])
def send_password(message):
    bot.reply_to(message, gen_pass(8) )

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message,"/bye - пока \n/about \n/password \n/heh\n/emoji \n/set\n/unset\n/coin")

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
