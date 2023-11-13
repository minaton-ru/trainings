import telebot
from extensions import ConverionException, Converter
from config import TOKEN, currencies

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Бот конвертирует валюты по текущему курсу ЦБ РФ.\nОтправьте сообщение боту через пробел в формате:\n <сумма> <валюта> <в какую валюту>\nСписок всех доступных валют по команде: /values\nОписание по команде /help\nAPI курсов валют - www.cbr-xml-daily.ru"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConverionException('Неверное количество параметров!')

        amount, quote, base = values
        result = Converter.get_price(amount, quote, base)
    except ConverionException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка:\n{e}")
    else:
        bot.reply_to(message, result)


bot.infinity_polling()
