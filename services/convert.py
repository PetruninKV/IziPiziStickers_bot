from dataclasses import dataclass
import asyncio
import requests

from aiogram.methods import GetFile
from aiogram.types import File

from rembg import remove
from PIL import Image
import io

from config_data.config import load_config, Config

config: Config = load_config()


class PhotoRender:
    MAX_SIZE: int = 512

    def __init__(self, file_id, width, height):
        self._file = file_id
        self.size = (width, height)

    async def get_file(self):
        file_info: File = await GetFile(file_id=self._file)
        file_url = f'https://api.telegram.org/file/bot{config.tg_bot.token}/{file_info.file_path}'
        self._file = requests.get(file_url).content

    @property
    def file(self):
        return self._file

    @property
    def size(self):
        return self._width, self._height

    @size.setter
    def size(self, value):
        self._fl_resize = False
        width, height = value
        if width > self.MAX_SIZE or height > self.MAX_SIZE:
            self._fl_resize = True
            if width == height:
                self._width = self.MAX_SIZE
                self._height = self.MAX_SIZE
            elif width > height:
                self._width = self.MAX_SIZE
                self._height = int(self.MAX_SIZE * height / width)
            else:
                self._width = int(self.MAX_SIZE * width / height)
                self._height = self.MAX_SIZE

    def remove_background(self):
        self._file = remove(self.file)

    def rescaling(self):
        im = Image.open(io.BytesIO(self.file))
        if self._fl_resize:
            im = im.resize(self.size)
        with io.BytesIO() as f:
            im.save(f, format='PNG')
            image_bytes = f.getvalue()
        self._file = image_bytes


async def photo_processing(file_id: str, width: int, height: int) -> bytes:
    photo = PhotoRender(file_id, width, height)
    await photo.get_file()
    photo.remove_background()
    photo.rescaling()
    return photo.file
