import telebot
from config import keys, TOKEN
from extensions import ConvertionException, get_price

bot = telebot.TeleBot(TOKEN)

#Инструкция по работе
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Welcome, {message.chat.first_name}')
    text = 'Чтобы начать работу введите значения через пробел в следующем формате:\n \
<начальная валюта> <конечная валюта> <количество переводимой валюты>\n \
Чтобы увидеть список доступных валют введите: /values'
    bot.reply_to(message, text)

#Вывод списка оступных валют.
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

#отправка запроса API
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values_lower = message.text.lower()
    try:
        values = values_lower.split(' ')

        if len(values) != 3:
            raise ConvertionException('Количество параметров отличается от требуемого.')

        quote, base, amount = values
        total_base = get_price.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling()

