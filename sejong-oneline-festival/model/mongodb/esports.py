from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model


class Esports(Model):

    VERSION = 1

    @property
    def index(self) -> list:
        return [
            IndexModel([
                ('owner_id', ASCENDING)
            ])
        ]

    @property
    def schema(self) -> dict:
        return {
            'name': None, # 이스포츠 이름
            'owner_id': None, # 이벤트 관리자 id
            'banner_photo': None, # 배너 이미지 링크
            'participants': [], # 참가팀 리스트
            'match_logs': [], # 팀 매치업 로그
            'created_at': datetime.now(),
            '__version__': self.VERSION
        }