LEXICON_MESSAGE: dict[str, str] = {
    '/start': 'Воздушный Гамарджоба! \nОт моего сердечка твоему душевно в душу! 🇬🇪',
    '/start continue': '🔝🔝🔝\nЗацени мой набор стикеров - просто нажми на него. \nХочешь собственные? Жми - /about',
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
    '/demo': 'Ты присылаешь мне свое фото, а я - убираю фон, делаю нужный размер, так чтобы бот принял готовый файл. '
             '\nВот пример:',
    '/demo continue': 'Готовый файл можно переслать @Stickers и он его примет. ИзиПизи ;) \n'
                      'Давай скорее попробуем. Переходим в режим редактирования - /formatting',
    '/formatting': 'Отлично! Отправьте мне свои фото. Вы можете отправить мне изображения c сжатием, а можете '
                   'отправить без сжатия - документом. Я работаю с обоими форматами.',
    '/formatting_continue': 'Чтобы выйти из режима редактирования фото используйте команду /stop_formatting',
    '/stop_formatting': 'Режим редактирования фото выключен. Надеюсь вы довольны результатом. Жду Вас снова!',
    '/stop_formatting_error': 'Вы находитесь вне режима редактирования фото',
    'formatting_work_on': 'Пришлите мне фото или изображение в виде документа - jpg, png, webp. \nЧтобы выйти из '
                          'режима редактирования фото используйте команду /stop_formatting ',
    '/privacy': '<b>А это безопасно!?</b>\n'
                '<pre>Я гид на незнакомой местности \nЯ огнетушитель во время пожара '
                '\nЯ панамка против солнцепека \nЯ якорь в штормовом море.'
                ' \nВ общем, Безопасность - моё второе имя!</pre>\n\n'
                'Уважаю Вашу конфиденциальность! \nМой код устроен таким образом, что я не сохраняю Ваши фотографии, '
                'а лишь обрабатываю их и возвращаю обратно. \nМожете в этом убедиться, посмотрев исходный код: '
                '<a href="https://github.com/PetruninKV/IziPiziStickers_bot">GitHub</a>',
    '/lang': 'Пока что мы в поисках переводчиков...',
    '/help': 'Запусти режим редактирования фото - /formatting и отправь мне фотографии из которых ты хочешь сделать '
             'стикер. Я отформатирую их и отправлю обратно в виде файла, готового к добавлению в Ваш стикерпак '
             'и удовлетворяющего всем требованиям Telegram. Подробная '
             '<a href="https://telegra.ph/create-stickers-04-21">инструкция</a> о создании стикеров.',
    'other_mess': 'Воспользуйся коммандами из Меню.\nДля справки - /help',
    'photo_doc_mes': 'Включите режим редактирования изображения с помощью /formatting и отправляйте фото на обработку',
    'reaction_to_photo': ['Вау, это фото просто потрясающее!', 'Ого, какое красивое фото!',
                          'Невероятно, я в восторге от этого фото!', 'Удивительно, как хорошо снято это фото!',
                          'Какое изумительное фото, я просто не могу оторваться!',
                          'Это фото заставляет меня восхищаться каждый раз, когда я его вижу!',
                          'Я впечатлен красотой и качеством этого фото!',
                          'Как же красиво, удивительное фото!', 'Очарован этим прекрасным фото!',
                          'Великолепное фото, я просто без ума от него!'],
    'finish': 'Готово! Проверь получившийся файл и перешли его @Stickers',

}

LEXICON_MENU: dict[str, str] = {

    'instruction': 'подробно о стикерах',
    'about': 'краткое описание бота',
    'demo': 'демонстрация работы',
    'formatting': 'запустить редактор фото',
    'stop_formatting': 'выйти из редактора',
    'privacy': 'конфиденциальность',
    'lang': 'сменить язык бота',
    'help': 'справка',

}

LEXICON_KEYBOARD: dict[str, str] = {
    'forward': 'переслать сообщение',
}

LEXICON_MIDDLEWARES: dict[str, str] = {
    'formatting': 'Мы обнаружили подозрительную активность. Для обработки нового фото подождите 10 секунд.',
    'default': 'Подозрительная активность.',
    'flood': 'Подозрительная активность.',
}
