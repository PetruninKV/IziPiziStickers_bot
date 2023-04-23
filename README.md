## IziPiziStickers

[IziPiziStickers](https://t.me/make_photo_for_sticker_bot) - this Telegram bot helps users create their own custom
stickers.

## Features

The best part is that users can create their own stickers without the need for any additional software
The bot receives images or file from users and converts them into .png format that has no background and doesn't exceed
512x512
resolution - these are the necessary requirements for creating stickers. All that's left for you to do is to forward the
resulting file to [@Stickers](https://t.me/Stickers).


## Setup

1. Get your Telegram bot token from [@BotFather](https://t.me/BotFather)
2. Rename .env.example to .env and edit to set your tokens
3. Run 
    ```bash
   docker build . -f Dockerfile -t izipizibot
   docker run -it izipizibot
    ```
   
