import config
import telebot
from telebot import types
from rembg import remove
from PIL import Image
import io
import requests
import tempfile


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    botton1 = types.KeyboardButton('Расскажи о себе')
    botton2 = types.KeyboardButton('Инструкция')
    botton3 = types.KeyboardButton('А это безопасно?')
    botton4 = types.KeyboardButton('Ты где вообще есть?')
    markup.add(botton1, botton2, botton3, botton4)

    start_mess = f'Воздушный гамарджоба, <b>{message.from_user.first_name}</b>!\nОт моего сердечка твоему душевно в душу! 🇬🇪'
    bot.send_message(message.chat.id, start_mess, parse_mode='html', reply_markup=markup)
    bot.send_sticker(message.chat.id, config.Stiсker_id.stick_welcome)


@bot.message_handler(content_types=['text'])
def answer_text(message):
    if message.text == 'Ты где вообще есть?':
        bot.send_location(message.chat.id, 41.64207, 41.61689)
        bot.send_message(message.chat.id, 'я здесь, любимка ❤️')

    elif message.text == 'Инструкция':
        bot.send_message(message.chat.id, 'Подготавливаю твои фото. А именно - убираю фон, делаю нужный размер. Вот пример:')
        with open('./test_foto/photo.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo,  caption='Ты отправляешь мне обычное фото')    
        with open('./test_foto/for_stick_file.png', 'rb') as photo:
            bot.send_document(message.chat.id, photo, caption='я тебе возвращаю файл  подходящий для создания стикера')        

    elif message.text == 'Расскажи о себе':
        mes = """Чтобы сделать набор со своими стикерами, тебе необходимо написать моему братишке @Stickers. Там все интуитивно понятно:
        - отправляешь фото
        - отправляешь соответствующий смайлик
        - вуаля!
Но есть нюанс. <b>Фото для будущего стикера</b> — <i>файл в формате PNG или WEBP с прозрачным фоном. Изображение должно вписываться в квадрат 512x512</i>.
Поэтому я создан, чтобы помочь подготовить твое фото для стикера.
Нажми на 'Инструкция', чтобы увидеть пример.
        """
        bot.send_message(message.chat.id, mes, parse_mode='html')

    elif message.text == 'А это безопасно?':
        mes1 = """Я volvo среди авто
Я pfizer из всех вакцин
Я дюрекс в мире секса"""
        mes2 = """Мой код устроен таким образом, что я не храню ваши фотографии, а лишь обрабатываю их и возвращаю обратно. 
Можешь в этом убедиться, посмотрев исходник кода:"""
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Жмак сюда', url='https://github.com/PetruninKV'))
        bot.send_message(message.chat.id, mes1)
        bot.send_message(message.chat.id, mes2, reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Не понимать тебя. Пока что я не такой умный как ChapGPT.')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Вот его профиль', url='https://chat.openai.com'))
        bot.send_message(message.chat.id, 'Если хочется поболать с умным:', reply_markup=markup)


@bot.message_handler(content_types=['document'])
def get_user_document(message):
    bot.send_message(message.chat.id, 'TypeError. Пришли мне именно фото, не документ.')


@bot.message_handler(content_types=['photo'])
def get_user_foto(message):
    bot.send_message(message.chat.id, 'вау, какое фото!')
    file_info = bot.get_file(message.photo[-1].file_id)
    file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'
    file_content = requests.get(file_url).content
    
    bot.send_message(message.chat.id, '<i>идет обработка...</i> 💡', parse_mode='html')
    bot.send_sticker(message.chat.id, config.Stiсker_id.stick_processing)

    output_file = remove(file_content) 

    im = Image.open(io.BytesIO(output_file))
    weight, height = im.size
    if weight <= 512 and height <= 512:
        new_weight = weight
        new_height = height
    else:
        if weight == height:
            new_weight = 512
            new_height = 512
        elif weight > height:
            new_weight = 512
            new_height = int(512 * height/weight)
        else:
            new_weight = int(512  * weight / height)
            new_height = 512
    output_image = im.resize((new_weight, new_height))   

    markup2 = types.InlineKeyboardMarkup()
    markup2.add(types.InlineKeyboardButton('Перешли фото @Stickers', switch_inline_query='Инструкция' ))  

    with tempfile.NamedTemporaryFile(prefix='for_stick_file_', suffix='.png') as temp:
    # Сохранить обработанное изображение во временный файл
        output_image.save(temp.name)
        with open(temp.name, 'rb') as f:
            bot.send_document(message.chat.id, f, caption='Готово!', reply_markup=markup2)
          

bot.polling(none_stop=True)