"""
Esports API
이스포츠 이벤트 관련 API
"""
from flask_validation_extended import Validator, Query, Json, List, Dict
from flask_validation_extended import ValidationRule
from flask import g
from app.api import response_200, bad_request
from app.api.api_v1 import api_v1 as api
from app.api.decorator import login_required, timer
from model.mongodb import Esports


# 경기 생성
@api.route('v1/esports/create', methods=['PUT'])
@Validator(bad_request)
@login_required("esports")
@timer
def esports_v1_create_event(
    name=Json(str)
):
    Esports(g.db).insert_event(name, g.user_id)
    return response_200()

# 팀 추가
@api.route('v1/esports/team', methods=['PUT'])
@Validator(bad_request)
@login_required("esports")
@timer
def esports_v1_create_team(
    event_name=Json(str),
    team_name=Json(str),
    members=Json(List([dict]))
):
    print(event_name)
    print(team_name)
    print(members)
    print(Esports(g.db).find_all())
    return response_200()