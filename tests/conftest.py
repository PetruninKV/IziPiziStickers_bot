import pytest
from services.convert import PhotoRender


@pytest.fixture(autouse=True)
def create_photo_object(request):
    photo = PhotoRender('test_file_id')
    yield photo
