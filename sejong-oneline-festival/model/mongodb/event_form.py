from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model


class EventForm(Model):

    VERSION = 1

    @property
    def index(self) -> list:
        return [
            IndexModel([('event_id', ASCENDING)])
        ]

    @property
    def schema(self) -> dict:
        return {
            'event_id': None, # 연결된 이벤트 id
            'author_id': None, # 작성자 id
            'author_name': None, # 작성자 이름
            'author_major': None, # 작성자 학과
            'answers': [], # 답변 리스트
            'created_at': datetime.now(),
            '__version__': self.VERSION
        }