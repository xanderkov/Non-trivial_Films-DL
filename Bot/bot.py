import telebot
import Bot.constants as constants
from FilmFinder import find_film

bot = telebot.TeleBot(constants.BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, 'Категорически приветсвую. Я могу найти фильм похожий по описанию вашего любимого фильма. \n'
                                'Вы можете отправить название фильма или ссылку на кинопоиск.')


@bot.message_handler(commands=["help"])
def start(m):
    bot.send_message(m.chat.id, 'Просто отправьте название фильма как в кинопоиске, например "Матрица", или же https://www.kinopoisk.ru/film/301/')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    films = find_film(message.text)
    if films != None:
        for film in films:
            answer = film[0] + "\n" + film[1]
            bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, "Такого фильма в базе данных нет(")


bot.polling(none_stop=True, interval=0)
