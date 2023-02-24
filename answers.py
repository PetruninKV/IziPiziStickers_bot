import telebot
from telebot import types
import config
import requests
from rembg import remove
from PIL import Image
import io
from dataclasses import dataclass
from random import randint


@dataclass
class Initialization:
    bot: telebot.TeleBot
    message: telebot.types.Message

    
class Comands(Initialization):
    
    def start(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        botton1 = types.KeyboardButton('Расскажи о себе')
        botton2 = types.KeyboardButton('Инструкция')
        botton3 = types.KeyboardButton('А это безопасно?')
        botton4 = types.KeyboardButton('Ты где вообще есть?')
        markup.add(botton1, botton2, botton3, botton4)        

        start_mess = f'Воздушный гамарджоба, <b>{self.message.from_user.first_name}</b>!\nОт моего сердечка твоему душевно в душу! 🇬🇪'
        self.bot.send_message(self.message.chat.id, start_mess, parse_mode='html', reply_markup=markup)
        self.bot.send_sticker(self.message.chat.id, config.Stiсker_id.stick_welcome)

    def finish(self):
        self.bot.send_message(self.message.chat.id, 'Накхвамдис')


class Text(Initialization):
    
    def send_instruction(self):
        self.bot.send_message(self.message.chat.id, 'Подготавливаю твои фото. А именно - убираю фон, делаю нужный размер. Вот пример:')
        with open('./test_photo/photo.jpg', 'rb') as photo:
            self.bot.send_photo(self.message.chat.id, photo,  caption='Ты отправляешь мне обычное фото')    
        with open('./test_photo/test_for_stick_file.png', 'rb') as photo:
            self.bot.send_document(self.message.chat.id, photo, caption='я тебе возвращаю файл  подходящий для создания стикера')        

    def send_about_me(self):
        mes = """Чтобы сделать набор со своими стикерами, тебе необходимо написать моему братишке @Stickers. Там все интуитивно понятно:
        - отправляешь фото
        - отправляешь соответствующий смайлик
        - вуаля!
Но есть нюанс. <b>Фото для будущего стикера</b> — <i>файл в формате PNG или WEBP с прозрачным фоном. Изображение должно вписываться в квадрат 512x512</i>.
Поэтому я создан, чтобы помочь подготовить твое фото для стикера.
Нажми на 'Инструкция', чтобы увидеть пример.
        """
        self.bot.send_message(self.message.chat.id, mes, parse_mode='html')        
    
    def send_github(self):
        mes1 = """Я volvo среди авто
Я огнетушитель во время пожара
Я pfizer из всех вакцин
Я дюрекс в мире секса
В общем, Безопасность - моё второе имя!"""
        mes2 = """Мой код устроен таким образом, что я не храню ваши фотографии, а лишь обрабатываю их и возвращаю обратно. 
Можешь в этом убедиться, посмотрев исходник кода:"""
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Жмак сюда', url='https://github.com/PetruninKV/telebot_make_foto_for_sticker'))
        self.bot.send_message(self.message.chat.id, mes1)
        self.bot.send_message(self.message.chat.id, mes2, reply_markup=markup)        

    def send_location(self):
        self.bot.send_message(self.message.chat.id, 'Я то тут, то там. Кручусь, верчусь')
        location_latitude =  randint(-60, 60) + randint(20000, 70000) * 0.00001
        location_longitude =  randint(-60, 60) + randint(20000, 70000) * 0.00001
        self.bot.send_location(self.message.chat.id, location_latitude, location_longitude)
        self.bot.send_message(self.message.chat.id, 'сейчас здесь, любимка ❤️')            
    
    def other_question(self):
        self.bot.send_message(self.message.chat.id, 'Не понимать тебя. Пока что я не такой умный как ChapGPT.')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Вот его профиль', url='https://chat.openai.com'))
        self.bot.send_message(self.message.chat.id, 'Если хочется поболать с умным:', reply_markup=markup)        


class Documents(Initialization):

    def send_error(self):
        self.bot.send_message(self.message.chat.id, 'Не понимать тебя. Пока что я не такой умный как ChapGPT.')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Вот его профиль', url='https://chat.openai.com'))
        self.bot.send_message(self.message.chat.id, 'Если хочется поболать с умным:', reply_markup=markup)        


class Photos(Initialization):

    def __init__(self, bot, message):
        super().__init__(bot, message)
        self.photo = self.message.photo[-1].file_id

    def send_first_reaction(self):
        self.bot.send_message(self.message.chat.id, 'вау, какое фото!')

    def send_processing(self):
        self.bot.send_message(self.message.chat.id, '<i>идет обработка...</i> 💡', parse_mode='html')
        self.bot.send_sticker(self.message.chat.id, config.Stiсker_id.stick_processing)        

    @property
    def photo(self):
        print('property', type(self._file_content))
        return self._file_content

    @photo.setter
    def photo(self, file_id):
        file_info = self.bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{self.bot.token}/{file_info.file_path}'
        self._file_content = requests.get(file_url, verify=False).content        

    def del_background(self):
        self._file_content = remove(self._file_content)
        
    def rescaling(self):
        im = Image.open(io.BytesIO(self._file_content))
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
        resize_photo = im.resize((new_weight, new_height))
        r = resize_photo.tobytes()
        with io.BytesIO() as f:
            resize_photo.save(f, format='PNG')
            image_bytes = f.getvalue()
            self._file_content = image_bytes
        
    def send_res(self):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Перешли фото @Stickers', switch_inline_query='Инструкция' )) 

        doc = io.BytesIO(self._file_content)    
        doc.name = 'foto_for_sticker.png'
        self.bot.send_document(self.message.chat.id, doc, caption='Готово!', reply_markup=markup)





