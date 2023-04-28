import io

from aiogram.methods import GetFile
from aiogram.types import File

from rembg import remove
from PIL import Image
import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError

from config_data.config import load_config, Config

config: Config = load_config()


class PhotoRender:
    MAX_SIZE: int = 512

    def __init__(self, file_id) -> None:
        self._file_id = file_id
        self._file: bytes = b""
        self._width: int = 0
        self._height: int = 0
        self._fl_resize: bool = False

    async def get_file(self) -> None:
        file_info: File = await GetFile(file_id=self._file_id)
        file_url = f'https://api.telegram.org/file/bot{config.tg_bot.token}/{file_info.file_path}'
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            self._file = response.content
        except HTTPError as e:
            raise RequestException(f"Ошибка чтения: {e}")
        except ConnectionError:
            raise ConnectionError("Ошибка подключения")

    @property
    def file(self) -> bytes:
        return self._file

    @property
    def size(self) -> tuple[int, int]:
        return self._width, self._height

    def remove_background(self) -> None:
        self._file = remove(self.file)

    def get_size(self) -> None:
        im = Image.open(io.BytesIO(self.file))
        self._fl_resize = False
        width, height = im.size
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
        else:
            self._width = width
            self._height = height

    def rescaling(self) -> None:
        im = Image.open(io.BytesIO(self.file))
        if self._fl_resize:
            im = im.resize(self.size)
        with io.BytesIO() as f:
            im.save(f, format='PNG')
            image_bytes = f.getvalue()
        self._file = image_bytes


async def photo_processing(file_id: str) -> bytes | str:
    photo = PhotoRender(file_id)
    try:
        await photo.get_file()
        photo.remove_background()
        photo.get_size()
        photo.rescaling()
    except (RequestException, ConnectionError):
        return f'Сетевая ошибка. Не удалось получить изображение. Попробуйте позже.'
    return photo.file
