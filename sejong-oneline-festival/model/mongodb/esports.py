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
            'status': False, # 대회 진행 현황 (시작 / 미시작)
            'participants': [], # 참가팀 리스트
            'match_logs': [], # 팀 매치업 로그
            'created_at': datetime.now(),
            '__version__': self.VERSION
        }

    def insert_event(self, name: str, owner_id: str):
        return self.col.insert_one(self.schemize(
                {'name': name, 'owner_id': owner_id}
            )
        )

    def update_event(self, event_id: ObjectId, field_obj: dict):
        self.col.update_one(
            {'_id': event_id},
            {field_obj}
        )

    def delete_event(self, event_id: ObjectId, owner_id: str):
        self.col.delete_one(
            {
                '_id': event_id,
                'owner_id': owner_id
            }
        )

    def update_status(self, event_id: ObjectId, status: bool):
        self.col.update_one(
            {'_id': event_id},
            {'$set': {'status': status}}
        )

    def insert_team(self, event_id: ObjectId, team: dict):
        self.col.update_one(
            {'_id': event_id},
            {'$push': {'participants': team}}
        )

    def delete_team(self, event_id: ObjectId, owner_id: str, team_name: str):
        self.col.update_one(
            {'_id': event_id, 'owner_id': owner_id},
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
    
    def update_match_log(self, event_id: ObjectId, match_logs: list):
        self.col.update_one(
            {'_id': event_id},
            {'$set': {'match_logs': match_logs}}
        )