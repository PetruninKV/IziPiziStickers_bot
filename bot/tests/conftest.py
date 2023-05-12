import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.convert import PhotoRender


@pytest.fixture(autouse=True)
def create_photo_object(request):
    photo = PhotoRender('test_file_id')
    yield photo
