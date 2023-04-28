from io import BytesIO

import pytest
from PIL import Image


@pytest.mark.parametrize("size, expected_result", [((1000, 500), (512, 256)),
                                                   ((500, 1000), (256, 512)),
                                                   ((1000, 1000), (512, 512)),
                                                   ((100, 50), (100, 50)),
                                                   ((50, 100), (50, 100)),
                                                   ((512, 512), (512, 512)),
                                                   ])
def test_get_size_resizes_image(create_photo_object, size, expected_result):
    # Создаем тестовое изображение размером size
    test_image = Image.new('RGB', size, color='red')
    with BytesIO() as output:
        # Сохраняем в буфер
        test_image.save(output, format='PNG')
        test_image_bytes = output.getvalue()
    create_photo_object._file = test_image_bytes
    create_photo_object.get_size()
    assert create_photo_object.size == expected_result
