> README in english [here](README.md)

[![Build status](https://github.com/PetruninKV/telebot_make_foto_for_sticker/actions/workflows/checks.yml/badge.svg?branch=master)](https://github.com/PetruninKV/telebot_make_foto_for_sticker/actions/workflows/checks.yml)

## IziPiziStickers [![Telegram bot](https://img.shields.io/badge/bot-online-success?style=plastick&logo=telegram&labelColor=FCFCFC)](https://t.me/make_photo_for_sticker_bot)

[IziPiziStickers](https://t.me/make_photo_for_sticker_bot) - помогает создавать свои собственные стикеры Telegram.

## Основное назначение
Пользователи могут создавать свои собственные стикеры без использования какого-либо дополнительного программного обеспечения - не покидая Telegram.

Бот получает изображение или файл от пользователей и преобразует их в формат .png без фона, разрешение которого не превышает 512x512px - это необходимые требования для создания стикеров. Все, что вам остаетя сделать, это переслать полученный файл [@Stickers](https://t.me/Stickers).

Подробная хронология развития проекта и описание всех возвожностей бота [здесь](description.md)

## Используемые ехнологии
- Python3.10: язык программирования
- Aiogram3.x: фреймворк для создания телеграм ботов
- Redis: РСУБД работающая со структурами данных типа "ключ - значение"
- InfluxDB:2.7: СУБД для хранения временных рядов
- Grafana: визуализация данных
- Docker и docker-compose: контейнеризация всех компонентов
- Git Actions: автоматизированная система сборки, тестирования и развертывания кода
  и другие.

<h1>Для локального запуска</h1>

## Подготовительные шаги
1. Скопируй репозитрорий
    ```bash
   git clone https://github.com/PetruninKV/IziPiziStickers_bot.git
    ```
2. Перейди в созданную директорию и создай внутри три поддиректории
    ```bash
   mkdir influxdb_data grafana_data redis_data
    ```

## Переменные окружения
1. Переименуй .env.example в .env
2. Заполни .env:
   - получи телеграм токен у [@BotFather](https://t.me/BotFather)
   - укажи id администратора для доступа к командам администратора
   - токен для InfluxDB добавим немного позже
   - выполни  ```id -u ``` и укажи полученное значение для UID

## Docker
1. В первый раз следует поднять только контейнер с InfluxDB для создания пользователя и получения token
    ```bash
   docker-compose up influxdb
    ```
2. Открой в браузере http://localhost:8086
   - Get started
   - Заполни Username и Password на свое усмотрение, а Org Name - 'stats-bot', Bucket Name - 'events'
   - Выбери Quick start, перейди в Load Data - API Tokens
   - Создай новый токен - Generate API Token (Custom API Token)
   - Придумай описание, добавь events из Buckets выбрав read-write. Нажми Generate.
   - Скопируй сгенерированный токен и вставь в .env INFLUXDB_TOKEN=
3. Запусти оставшиеся сервисы
    ```bash
   docker-compose up
    ```
4. Открой в браузере http://localhost:3000
   - admin admin - логин и пароль по умолчанию. На следующем шаге измени их или пропусти эти настройки
   - Перейди на домашнюю страницу и выбери "Add your first data sourse"
   - Выбери из списка InfluxDB
     - В Query Language выбери Flux
     - HTTP URL - http://influxdb:8086
     - В Auth отключи все
     - В InfluxDB Details:
       - Organization - 'stats-bot'
       - Token - укажи тот, что получили ранее, на втором шаге
       - Default Bucket - 'events'
     - Нажми Save & test
     - Увидишь Datasource updated и datasource is working. 1 buckets found - значит все хорошо.
     - В строке браузера необходимо скопировать идентефикатор базы данных, пример: localhost:3000/datasources/edit/<b>D4p5Afw4k</b>. У тебя он будет свой. Вставь значение в .env файл ID_DATA_SRC_INFLIXDB.
   - Выполни
      ```bash
      ./scripts/change_id.sh
      ```
      Он переименует [конфигурационный файл](dashboard.example.json) с настройками в dashboard.json и во всех строках  <b>"uid": "YOUR_ID"</b> подставит твой идентефикатор полученный в предыдущем пункте.

      Если скрипт не иммет права на выполнение, используй:
      ```bash
      chmod +x ./scripts/change_id.sh
      ```

   - Перейди в [найстройки дашбордов](http://localhost:3000/dashboard/import) и импортируй dashboard.json
   - Теперь тебе доступна статистика

![Пример работы статистики](images/stats-image.png)
- "Menu commands" : Этот график отображает использование команд в определенном временном промежутке. Он показывает количество использования команд из меню, за определенный период времени.
- "Formatting photo" : Этот график отображает количество фотографий, отформатированных пользователем в определенный период времени. Он позволяет отследить активность пользователей, связанную с форматированием фотографий.
- "User activity" : Этот график отображает общее количество сообщений от пользователя в определенный период времени. Он демонстрирует активность пользователя, основанную на количестве отправленных им сообщений.
- "Messages" : Эта таблица отображает: сообщения, которые не были обработаны как команды,  сообщает о фотографиях, если они отправлены пользователем, когда он не находился в режиме редактирования, и просто текстовые сообщения. Эта таблица позволяет оценить флуд от пользователей, неправильность использования режима редактирования и команды которые не были обработаны ботом.
