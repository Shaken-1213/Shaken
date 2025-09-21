import telebot
import random
import schedule
import threading
import time

def flip_coin():
    return random.choice(['Орёл', 'Решка'])

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>123456789"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password

bot = telebot.TeleBot("8418297671:AAFWgKwidmwaTg5eWTTSKgTh4_p-XGDnrCg")

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

@bot.message_handler(commands=['emoji'])
def send_emoji(message):
    emoji = gen_emodji()
    bot.reply_to(message, f"Вот эмоджи': {emoji}")

@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=['password'])
def send_password(message):
    bot.reply_to(message, gen_pass(8) )

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message,"/start \n/hello \n/bye \n/about \n /password \n/heh\nemoji \n/set\nemoji \n/unset\ncoin")

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

bot.polling()
