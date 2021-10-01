from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model


class Exhibition(Model):

    VERSION = 1

    @property
    def index(self) -> list:
        return [
            IndexModel([('owner_id', ASCENDING)])
        ]

    @property
    def schema(self) -> dict:
        return {
            'name': "", # 전시회 이름
            'banner_photo': None, # 배너 이미지 링크
            'owner_id': None, # 전시회 관리자 id
            'owner_name': None, # 전시회 관리자 이름
            'type': "", # 전시회 타입
            'post': "", # 전시회 설명 문구
            'contents': [], # 전시회 작품 리스트
            'created_at': datetime.now(),
            '__version__': self.VERSION
        }