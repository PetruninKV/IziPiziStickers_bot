from dotenv import load_dotenv
import telebot
import answers
import os

load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'finish'])
def answer_for_commands(message):
    comand = answers.Comands(bot, message)
    if message.text == '/start':
        comand.start()
    if message.text == '/finish':
        comand.finish()

@bot.message_handler(content_types=['text'])
def answer_for_text(message):
    text = answers.Text(bot, message)
    if message.text == 'Инструкция':
        text.send_instruction()
    elif message.text == 'Расскажи о себе':
        text.send_about_me()
    elif message.text == 'А это безопасно?':
        text.send_github()
    elif message.text == 'Ты где вообще есть?':
        text.send_location()
    else:
        text.other_question()       


@bot.message_handler(content_types=['document'])
def answer_for_document(message):
    doc = answers.Documents(bot, message)
    doc.send_error()


@bot.message_handler(content_types=['photo'])
def answer_for_photo(message):
    photo = answers.Photos(bot, message)
    photo.send_first_reaction()
    photo.send_processing()
    photo.del_background()
    photo.rescaling()
    photo.send_res()


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()










