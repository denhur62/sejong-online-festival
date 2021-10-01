"""
MainView API
축제 일정, 연예인 라인업, 라이브 스트리밍과 같은 메인 뷰 API
"""
import os
from flask import g, current_app
from flask_validation_extended import Validator, Json, File
from flask_validation_extended import List, Dict
from flask_validation_extended import Ext, MaxFileCount
from app.api import response_200, response_201, bad_request
from app.api.api_v1 import api_v1 as api
from app.api.decorator import timer
from controller.util import make_filename
from model.mongodb import MasterConfig


@api.route('/main/festival-schedule')
@timer
def main_get_festival_schedule_api_v1():
    """축제 일정 반환 API"""
    data = MasterConfig(g.db).get_config("festival_schedule")
    result = data['schedules'] if data and 'schedules' in data else None
    return response_200(result)


@api.route('/main/festival-schedule', methods=['PUT'])
@Validator(bad_request)
@timer
def main_put_festival_schedule_api_v1(
    schedules=Json(List(Dict([str, List(Dict(str))])))
):
    """축제 일정 갱신 API"""
    MasterConfig(g.db).upsert_config({
        'config_type': 'festival_schedule',
        'schedules': schedules
    })
    return response_201


@api.route('/main/celebrity-lineup')
@timer
def main_get_celebrity_lineup_api_v1():
    """연예인 라인업 반환 API"""
    data = MasterConfig(g.db).get_config("celebrity_lineup")
    celebrities = data['celebrities'] if data and 'celebrities' in data else []
    banner_photos = data['banner_photos'] if data and 'banner_photos' in data else []
    return response_200({
        'celebrities': celebrities,
        'banner_photos': banner_photos,
    })


@api.route('/main/celebrity-lineup', methods=['PUT'])
@Validator(bad_request)
@timer
def main_put_celebrity_lineup_api_v1(
    celebrities=Json(List(Dict(str)))
):
    """연예인 라인업 갱신 API"""
    MasterConfig(g.db).upsert_config({
        'config_type': 'celebrity_lineup',
        'celebrities': celebrities
    })
    return response_201


@api.route('/main/celebrity-lineup/photo', methods=['PUT'])
@Validator(bad_request)
@timer
def main_put_celebrity_photo_api_v1(
    photos=File(
        rules=[
            Ext(['.png', '.jpg', '.jpeg', '.gif']),
            MaxFileCount(10)
        ]
    )
):
    """연예인 라인업 포토 리스트 갱신 API"""
    banner_photos = []
    for photo in photos:
        filename = make_filename(photo.filename)
        photo.save(os.path.join(current_app.config['PHOTO_UPLOAD_PATH'], filename))
        banner_photos.append(filename)

    MasterConfig(g.db).upsert_config({
        'config_type': 'celebrity_lineup',
        'banner_photos': banner_photos
    })
    return response_201


@api.route("/main/live-streaming")
@timer
def main_get_live_streaming_api_v1():
    """라이브 스트리밍 반환 API"""
    data = MasterConfig(g.db).get_config("live_streaming")
    result = data['videos'] if data and 'videos' in data else []
    return response_200(result)


@api.route("/main/live-streaming", methods=['PUT'])
@Validator(bad_request)
@timer
def main_put_live_streaming_api_v1(
    videos=Json(List(Dict(str)))
):
    """라이브 스트리밍 갱신 API"""
    MasterConfig(g.db).upsert_config({
        'config_type': 'live_streaming',
        'videos': videos
    })
    return response_201