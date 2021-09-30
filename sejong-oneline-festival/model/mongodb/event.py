from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model


class Event(Model):

    VERSION = 1

    @property
    def index(self) -> list:
        return [
            IndexModel([
                ('owner_id', ASCENDING)
            ]),
            IndexModel([
                ('created_at', ASCENDING)
            ])
        ]

    @property
    def schema(self) -> dict:
        return {
            'name': None, # 이벤트 이름
            'banner_photo': None, # 배너 이미지 링크
            'owner_id': None, # 이벤트 관리자 id
            'post': "", # 이벤트 설명 문구
            'forms': [], # 설문지 폼
            'created_at': datetime.now(),
            '__version__': self.VERSION
        }