from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from bson.objectid import ObjectId
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

    def insert_event(self, name: str, owner_id: str):
        self.col.insert_one(self.schemize(
                {'name': name, 'owner_id': owner_id}
            )
        )

    def delete_event(self, event_id: ObjectId, owner_id: str):
        self.col.delete_one(
            {
                '_id': event_id,
                'owner_id': owner_id
            }
        )

    def insert_team(self, event_id: ObjectId, team: dict):
        self.col.update_one(
            {'_id': event_id},
            {'$push': {'participants': team}}
        )

    def delete_team(self, event_id: ObjectId, team_name):
        self.col.update_one(
            {'_id': event_id},
            {'$pull': {
                'participants': {'team_name': team_name}
            }}
        )

    def find_all_event(self):
        return list(self.col.find())

    def find_event(self, event_id: ObjectId):
        return self.col.find_one(
            {'_id': event_id}
        )
    
    def insert_match_log(self, event_id: ObjectId, log: dict):
        self.col.update_one(
            {'_id': event_id},
            {'$push': {'match_logs': log}}
        )