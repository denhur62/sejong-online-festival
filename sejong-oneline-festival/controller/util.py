from string import ascii_letters
from random import choice
from faker import Faker
from faker.providers import internet
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename


def get_fake():
    fake = Faker('ko_KR')
    fake.add_provider(internet)
    return fake


def snake2pascal(string: str):
    """String Convert: snake_case to PascalCase"""
    return (
        string
        .replace("_", " ")
        .title()
        .replace(" ", "")
    )


def pascal2snake(string: str):
    """String Convert: PascalCase to snake_case"""
    return ''.join(
        word.title() for word in string.split('_')
    )


def get_random_id():
    """Get Random String for Identification"""
    return str(ObjectId())


def make_filename(origin_filename: str):
    origin_filename = secure_filename(origin_filename)
    ext = origin_filename.rsplit('.', 1)[1].lower()
    return "%s.%s" % (get_random_id(), ext)


def remove_none_value(document: dict):
    """입력받은 dict의 None value 데이터를 제거한채 반환"""
    keys = list(document.keys())
    for key in keys:
        if document[key] is None:
            del document[key]
    return document