LEXICON_MESSAGE: dict[str, str] = {
    '/start': 'Воздушный Гамарджоба! \nОт моего сердечка твоему душевно в душу! 🇬🇪',
    '/start continue': 'Зацени мой набор стикеров - просто нажми на него.',
    '/instruction': 'Что такое стикеры, их виды, как создать и редактировать - в короткой, но подробной '
                    '<a href="https://telegra.ph/create-stickers-04-21">статье</a>.\n'
                    'Официальная техническая <a href="https://core.telegram.org/stickers#static-emoji">'
                    'документация</a> Telegram о стикерах.',
    '/about': 'Чтобы создать набор со своими стикерами, необходимо написать официальному боту - @Stickers. \n'
                   'Все довольно просто:\n<pre>- создаешь новый набор стикеров;\n- придумываешь ему название;\n' 
                   '- отправляешь свое фото;\n- отправляешь соответствующий смайлик;\n- вуаля!</pre>\n\n'
                   '<b>Но есть нюанс.</b>' 
                   '\nФото для будущего стикера — <u>файл в формате PNG или WEBP с прозрачным фоном.</u> ' 
                   'Изображение должно вписываться в квадрат <u>512x512 px</u>. \nЕсли отправить файл, не ' 
                   'соответствующий этим требованиям, бот не примет его. \nНекоторым может быть непросто ' 
                   'быстро подготовить свое фото для стикера, а кому то лень возиться с фоторедакторами '
                    'поэтому я и создан, чтобы упростить процесс подготовки фото. ' 
                    '\nНажми на /demo, чтобы увидеть пример.',
    '/demo': 'демонстрация работы бота',
    '/formatting': '',
    '/privacy': '<b>А это безопасно!?</b>\n'
                '<pre>Я гид на незнакомой местности \nЯ огнетушитель во время пожара '
                '\nЯ панамка против солнцепека \nЯ якорь в штормовом море.'
                ' \nВ общем, Безопасность - моё второе имя!</pre>\n\n'
                'Уважаю Вашу конфиденциальность! \nМой код устроен таким образом, что я не сохраняю Ваши фотографии, '
                'а лишь обрабатываю их и возвращаю обратно. \nМожете в этом убедиться, посмотрев исходный код: '
                '<a href="https://github.com/PetruninKV/telebot_make_foto_for_sticker">GitHub</a>',
    '/lang': 'Пока что мы в поисках переводчиков...',
    '/help': 'Запусти режим редактирования фото - /formatting и отправь мне фотографии из которой ты хочешь сделать '
             'стикер. Я отформатирую их и отправлю обратно в виде файла, готового к добавлению в Ваш стикер пак '
             'и удовлетворяющего всем требованиям Telegram. Подробная '
             '<a href="https://telegra.ph/create-stickers-04-21">инструкция</a> о создании стикеров.',
    'other_mess': 'Не понимаю тебя. Пока что я не такой умный как ChapGPT.',
    'reaction_to_photo': ['Вау, это фото просто потрясающее!', 'Ого, какое красивое фото!',
                          'Невероятно, я в восторге от этого фото!', 'Удивительно, как хорошо снято это фото!',
                          'Какое изумительное фото, я просто не могу оторваться!', 'Это фото заставляет меня '
                          'восхищаться каждый раз, когда я его вижу!', 'Я впечатлен красотой и качеством этого фото!',
                          'Как же красиво, удивительное фото!', 'Очарован этим прекрасным фото!', 'Великолепное'
                          'фото, я просто без ума от него!'],
    'processing': '<pre><i>идет обработка...</i></pre>💡',



}

LEXICON_MENU: dict[str,str] = {

    'instruction': 'подробно о стикерах',
    'about': 'краткое описание бота',
    'demo': 'демонстрация работы',
    'formatting': 'запустить редактор фото',
    'privacy': 'конфиденциальность',
    'lang': 'сменить язык бота',
    'help': 'справка'

}


LEXICON_KEYBOARD: dict[str, str] = {
    'instruction': 'Инструкция',
    'about you': 'Расскажи о себе',
    'security': 'А это безопасно?',
    'location': 'Ты где вообще есть?'
}