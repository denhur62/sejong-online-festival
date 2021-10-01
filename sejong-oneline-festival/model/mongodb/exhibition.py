from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model
from bson.objectid import ObjectId

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

    def find_all(self):
        return list(
            self.col.find({}, {
                '_id': 1,
                'name': 1,
                'banner_photo': 1,
                'owner_id': 1,
                'owner_name': 1,
                'type': 1
            })
        )

    def find_one(self, oid: ObjectId):
        return self.col.find_one(
            {'_id': oid},
            {
                '_id': 1,
                'name': 1,
                'banner_photo': 1,
                'owner_id': 1,
                'owner_name': 1,
                'type': 1,
                'post': 1,
                'contents': 1,
            }
        )

    def insert_one(self, document: dict):
        return self.col.insert_one(self.schemize(document))

    def update_one(self, oid: ObjectId, document: dict):
        self.col.update_one(
            {'_id': oid},
            {'$set': document}
        )