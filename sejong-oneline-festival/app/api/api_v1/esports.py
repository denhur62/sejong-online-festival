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
from app.api import response_200, response_201, bad_request, forbidden
from app.api.api_v1 import api_v1 as api
from app.api.decorator import login_required, timer
from model.mongodb import Esports
from controller.util import make_filename
from controller.esports import (make_team_document,
                                make_event_document,
                                make_tournament)


# 이벤트 생성
@api.route('esports/event', methods=['PUT'])
@login_required("esports")
@Validator(bad_request)
@timer
def esports_v1_create_event(
    event_name=Json(str)
):
    _id = Esports(g.db).insert_event(event_name, g.user_id)
    return response_200(
        {"event_id": _id.inserted_id}
    )


# 이벤트 배너(이미지) 추가
@api.route('esports/<event_id>/banner_photo', methods=['POST'])
@login_required("esports")
@Validator(bad_request)
@timer
def esports_v1_insert_banner(
    event_id=Route(str, rules=ObjectIdValid()),
    banner_photo=File(
        rules=[
            Ext(['.png', '.jpg', '.jpeg', '.gif']),
            MaxFileCount(1)
        ]
    )
):
    event = Esports(g.db).find_event(ObjectId(event_id))
    if exhibition['owner_id'] != g.user_id:
        return forbidden("You are not owner.")
    filename = make_filename(photo[0].filename)
    banner_photo.save(
        os.path.join(
            current_app.config['PHOTO_UPLOAD_PATH'],
            filename
        )
    )
    banner_photo_link = "/uploads/" + filename
    Esports(g.db).update_event(
        ObjectId(event_id),
        {'banner_photo': banner_photo_link}
    )
    return response_201


# 이벤트 삭제
@api.route('esports/<event_id>', methods=['DELETE'])
@login_required("esports")
@Validator(bad_request)
@timer
def esports_v1_delete_event(
    event_id=Route(str, rules=ObjectIdValid())
):
    Esports(g.db).delete_event(ObjectId(event_id), g.user_id)
    return response_201


# 이벤트 시작
@api.route('esports/<event_id>/start', methods=['PATCH'])
@Validator(bad_request)
@login_required("esports")
@timer
def esports_v1_update_status(
    event_id=Route(str, rules=ObjectIdValid()),
    match_teams=Json(List(str))
):
    event = Esports(g.db).find_event(
        ObjectId(event_id)
    )
    if event['status']:
        return bad_request("Already is started")

    Esports(g.db).update_status(ObjectId(event_id), True)
    for i in range(0, len(match_teams), 2):
        document = {
            'match_round': 0,
            'link': None,
            'match_teams': [match_teams[i], match_teams[i+1]],
            'winner_team': None,
            'status': "scheduled",
            'created_at': datetime.now()
        }
        Esports(g.db).insert_match_log(ObjectId(event_id), document)
    
    return response_201


# 팀 추가
@api.route('esports/<event_id>/team', methods=['PUT'])
@login_required("esports")
@Validator(bad_request)
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
    return response_201


# 팀 삭제
@api.route('esports/<event_id>/<team_name>', methods=['DELETE'])
@login_required("esports")
@Validator(bad_request)
@timer
def esports_v1_delete_team(
    event_id=Route(str, rules=ObjectIdValid()),
    team_name=Route(str)
):
    Esports(g.db).delete_team(
        ObjectId(event_id),
        g.user_id,
        team_name
    )
    return response_201


# 전체 이벤트 조회
@api.route('esports/events', methods=['GET'])
@timer
def esports_v1_get_all_events():
    document = make_team_document(
        Esports(g.db).find_all_event()
    )
    return response_200(document)


# 특정 이벤트 조회
@api.route('esports/<event_id>', methods=['GET'])
@timer
def esports_v1_get_events(
    event_id=Route(str, rules=ObjectIdValid())
):
    event = Esports(g.db).find_event(ObjectId(event_id))
    event['tournaments'] = make_tournament(event['match_logs'])
    return response_200(
        event
    )


# 매칭 실시간 유튜브 링크 삽입
@api.route('esports/<event_id>/match_link', methods=['PATCH'])
@login_required("esports")
@Validator(bad_request)
@timer
def esports_v1_update_match_link(
    event_id=Route(str, rules=ObjectIdValid()),
    match_round=Json(int),
    join_team=Json(str),
    link=Json(str),
):
    event = Esports(g.db).find_event(
        ObjectId(event_id)
    )
    for match in event['match_logs']:
        if winner_team in match['match_teams'] and\
           match['match_round'] == match_round:
           match['link'] = link
           break
    Esports(g.db).update_match_log(ObjectId(event_id), event['match_logs'])
    return response_201


# 매칭 결과 수정
@api.route('esports/<event_id>/match', methods=['PATCH'])
@login_required("esports")
@Validator(bad_request)
@timer
def esports_v1_update_match(
    event_id=Route(str, rules=ObjectIdValid()),
    match_round=Json(int),
    winner_team=Json(str),
):
    # 현재 매치 로그 수정
    event = Esports(g.db).find_event(
        ObjectId(event_id)
    )
    for match in event['match_logs']:
        if winner_team in match['match_teams'] and\
           match['match_round'] == match_round:
            match['winner_team'] = winner_team
            match['status'] = "end"
            break
    Esports(g.db).update_match_log(ObjectId(event_id), event['match_logs'])

    if match_round < 2:
        # 다음 라운드 매칭 자동화
        event = Esports(g.db).find_event(
            ObjectId(event_id)
        )
        now_round = []
        next_round_teams = []
        for match in event['match_logs']:
            if match['match_round'] == match_round:
                now_round.append(match)
            if match['match_round'] == match_round + 1:
                next_round_teams += match['match_teams']
        for i in range(0, len(now_round), 2):
            if now_round[i]['winner_team'] and\
            now_round[i+1]['winner_team'] and\
            now_round[i]['winner_team'] not in next_round_teams and\
            now_round[i+1]['winner_team'] not in next_round_teams:
                document = {
                    'match_round': match_round + 1,
                    'link': None,
                    'match_teams': [
                        now_round[i]['winner_team'],
                        now_round[i+1]['winner_team']
                    ],
                    'winner_team': None,
                    'status': "scheduled",
                    'created_at': datetime.now()
                }
                Esports(g.db).insert_match_log(ObjectId(event_id), document)

    return response_201
