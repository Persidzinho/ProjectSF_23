import telebot
from telebot import TeleBot
from config import keys, TOKEN
from utils import CryptoConverter, APIException

bot: TeleBot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n\n <имя валюты, цену которой Вы хотите узнать>   \
<в какую валюту перевести>   \
<количество переводимой валюты>\n\nУвидеть список всех доступных валют: "/value"'
    bot.reply_to(message, text)


@bot.message_handler(commands=['value'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
