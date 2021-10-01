"""
Esports API
이스포츠 이벤트 관련 API
"""
from flask_validation_extended import Validator, ValidationRule
from flask_validation_extended import File, Ext, Min, Form, MaxFileCount
from flask_validation_extended import Query, Route, Json, List, Dict
from app.api.validation import ObjectIdValid
from bson.objectid import ObjectId
from flask import g
from app.api import response_200, bad_request
from app.api.api_v1 import api_v1 as api
from app.api.decorator import login_required, timer
from model.mongodb import Esports
from controller.util import make_filename
from controller.esports import (make_team_document,
                                make_match_log_document)


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


# 매칭 로그 기록하기
@api.route('v1/esports/<event_id>/match_log', methods=['PUT'])
@Validator(bad_request)
@timer
def esports_v1_insert_match_log(
    event_id=Route(str, rules=ObjectIdValid()),
    match_round=Json(int),
    match_teams=Json(List(str))
):
    event = Esports(g.db).find_event(ObjectId(event_id))
    document = make_match_log_document(
        event['participants'],
        match_round,
        match_teams
    )
    Esports(g.db).insert_match_log(ObjectId(event_id), document)

    return response_200()


# 매칭 로그 수정하기
@api.route('v1/esports/<event_id>/match_log', methods=['UPDATE'])
@Validator(bad_request)
@timer
def esports_v1_insert_match_log(
    event_id=Route(str, rules=ObjectIdValid()),
    match_round=Json(int),
    match_teams=Json(List(str))
):
    event = Esports(g.db).find_event(ObjectId(event_id))
    document = make_match_log_document(
        event['participants'],
        match_round,
        match_teams
    )
    Esports(g.db).insert_match_log(ObjectId(event_id), document)

    return response_200()