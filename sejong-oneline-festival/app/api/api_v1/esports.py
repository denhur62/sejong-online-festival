"""
Esports API
이스포츠 이벤트 관련 API
"""
from flask_validation_extended import Validator, ValidationRule
from flask_validation_extended import File, Ext, Min, Form, MaxFileCount
from flask_validation_extended import Query, Route, Json, List, Dict
from app.api.validation import ObjectIdValid
from bson.objectid import ObjectId
from datetime import datetime
from flask import g
from app.api import response_200, bad_request
from app.api.api_v1 import api_v1 as api
from app.api.decorator import login_required, timer
from model.mongodb import Esports
from controller.util import make_filename
from controller.esports import (make_team_document)


# 이벤트 생성
@api.route('v1/esports', methods=['PUT'])
@Validator(bad_request)
@login_required("esports")
@timer
def esports_v1_create_event(
    event_name=Json(str)
):
    Esports(g.db).insert_event(event_name, g.user_id)
    return response_200()


# 이벤트 배너(이미지) 추가
@api.route('v1/esports/<event_id>/banner', methods=['POST'])
@Validator(bad_request)
@login_required("esports")
@timer
def esports_v1_insert_banner(
    event_id=Route(str, rules=ObjectIdValid()),
    photo=File(
        optional=False,
        rules=[
            Ext(['.png', '.jpg', '.jpeg', '.gif']),
            MaxFileCount(1)
        ]
    )
):
    filename = make_filename(photo.filename)


# 이벤트 삭제
@api.route('v1/esports/<event_id>', methods=['DELETE'])
@Validator(bad_request)
@login_required("esports")
@timer
def esports_v1_delete_event(
    event_id=Route(str, rules=ObjectIdValid())
):
    Esports(g.db).delete_event(ObjectId(event_id), g.user_id)
    return response_200()


# 이벤트 시작 / 종료
@api.route('v1/esports/<event_id>/status', methods=['PATCH'])
@Validator(bad_request)
@login_required("esports")
@timer
def esports_v1_update_status(
    event_id=Route(str, rules=ObjectIdValid()),
    status=Json(bool),
    match_teams=Json(List(str))
):
    Esports(g.db).update_status(ObjectId(event_id), status)
    if status:
        for i in range(0, len(match_teams), 2):
            document = {
                'match_round': 0,
                'match_teams': [match_teams[i], match_teams[i+1]],
                'winner_team': None,
                'status': "scheduled",
                'created_at': datetime.now()
            }
            Esports(g.db).insert_match_log(ObjectId(event_id), document)
    return response_200()


# 팀 추가
@api.route('v1/esports/<event_id>/team', methods=['PUT'])
@Validator(bad_request)
@login_required("esports")
@timer
def esports_v1_create_team(
    event_id=Route(str, rules=ObjectIdValid()),
    team_name=Json(str),
    members=Json(List([dict]))
):
    Esports(g.db).insert_team(
        ObjectId(event_id),
        make_team_document(team_name, members)
    )
    return response_200()


# 팀 삭제
@api.route('v1/esports/<event_id>/<team_name>', methods=['DELETE'])
@Validator(bad_request)
@login_required("esports")
@timer
def esports_v1_delete_team(
    event_id=Route(str, rules=ObjectIdValid()),
    team_name=Route(str)
):
    Esports(g.db).delete_team(
        ObjectId(event_id),
        team_name
    )
    return response_200()


# 전체 이벤트 조회
@api.route('v1/esports', methods=['GET'])
@timer
def esports_v1_get_all_events():
    return response_200(
        Esports(g.db).find_all_event()
    )


# 특정 이벤트 조회
@api.route('v1/esports/<event_id>', methods=['GET'])
@timer
def esports_v1_get_events(
    event_id=Route(str, rules=ObjectIdValid())
):
    event = Esports(g.db).find_event(ObjectId(event_id))
    return response_200(
        Esports(g.db).find_event(ObjectId(event_id))
    )


# 매칭 승리 수정
@api.route('v1/esports/<event_id>/match_log', methods=['PATCH'])
@Validator(bad_request)
@login_required("esports")
@timer
def esports_v1_update_match_log(
    event_id=Route(str, rules=ObjectIdValid()),
    match_round=Json(int),
    winner_team=Json(str),
):
    # 현재 매치 로그 수정
    now_round = Esports(g.db).find_match_log(
        ObjectId(event_id),
        match_round
    )
    for match in now_round:
        if winner_team in match['match_teams']:
            match['winner_team'] = winner_team
            match['status'] = "end"
            break
    Esports(g.db).update_match_log(ObjectId(event_id), now_round)

    # 다음 라운드 매칭 자동화
    next_round = Esports(g.db).find_match_log(
        ObjectId(event_id),
        match_round + 1
    )
    next_round_teams = []
    for team in next_round:
        next_round_teams += team['match_teams']
    for i in range(0, len(now_round), 2):
        if now_round[i]['winner_team'] and\
           now_round[i+1]['winner_team'] and\
           now_round[i]['winner_team'] not in next_round_teams and\
           now_round[i+1]['winner_team'] not in next_round_teams:
            document = {
                'match_round': match_round + 1,
                'match_teams': [
                    now_round[i]['winner_team'],
                    now_round[i+1]['winner_team']
                ],
                'winner_team': None,
                'status': "scheduled",
                'created_at': datetime.now()
            }
            Esports(g.db).insert_match_log(ObjectId(event_id), document)

