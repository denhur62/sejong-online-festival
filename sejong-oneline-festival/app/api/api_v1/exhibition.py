"""
Exhibition API
전시회 관련 API
"""
from flask import g, current_app
from flask_validation_extended import Validator, Query, Route, Json, List, In
from flask_validation_extended import ValidationRule, File, MaxFileCount
from bson.objectid import ObjectId
from app.api.validation import ObjectIdValid
from app.api import response_200, bad_request, response_201, forbidden
from app.api.api_v1 import api_v1 as api
from app.api.decorator import timer, login_required
from model.mongodb import Exhibition, User
from controller.util import remove_none_value, make_filename


@api.route("/exhibition")
@timer
def get_exhs_api_v1():
    """전시회 리스트 반환"""
    return response_200(Exhibition(g.db).find_all())


@api.route("/exhibition/<exhibition_id>")
@Validator(bad_request)
@timer
def get_exh_api_v1(
    exhibition_id=Route(str, rules=ObjectIdValid())
):
    """단일 전시회 반환"""
    oid = ObjectId(exhibition_id)
    return response_200(Exhibition(g.db).find_one(oid))


@api.route('/exhibition', methods=['POST'])
@login_required('exhibition')
@Validator(bad_request)
@timer
def post_exh_api_v1(
    name=Json(str),
    type=Json(str, rules=In(['gallery_normal', 'gallery_grid', 'video_youtube'])),
    post=Json(str),
    contents=Json(List(str), optional=True),
):
    """전시회 생성하기"""
    user = User(g.db).get_user_info_one(g.user_id)
    document = {
        'name': name,
        'owner_id': user['user_id'],
        'owner_name': user['name'],
        'type': type,
        'post': post,
        'contents': contents if type.startswith('video') and contents else []
    }
    _id = Exhibition(g.db).insert_one(document)
    return response_200(_id.inserted_id)


@api.route("/exhibition/<exhibition_id>", methods=["PUT"])
@login_required('exhibition')
@Validator(bad_request)
@timer
def put_exh_api_v1(
    exhibition_id=Route(str, rules=ObjectIdValid()),
    name=Json(str, optional=True),
    post=Json(str, optional=True),
    contents=Json(List(str), optional=True)
):
    """전시회 수정하기"""
    document = remove_none_value(locals())
    del document['exhibition_id']
    oid = ObjectId(exhibition_id)
    exhibition = Exhibition(g.db).find_one(oid)
    if exhibition['owner_id'] != g.user_id:
        return forbidden("You are not owner.")
    if exhibition['type'].startswith('gallery'):
        del document['contents']
    Exhibition(g.db).update_one(oid, document)
    return response_201


@api.route("/exhibition/<exhibition_id>/banner", methods=['PUT'])
@login_required('exhibition')
@Validator(bad_request)
@timer
def put_exh_banner_api_v1(
    exhibition_id=Route(str, rules=ObjectIdValid()),
    banner_photo=File(rules=MaxFileCount(1))
):
    """전시회 배너 이미지 업로드"""
    oid = ObjectId(exhibition_id)
    exhibition = Exhibition(g.db).find_one(oid)
    if exhibition['owner_id'] != g.user_id:
        return forbidden("You are not owner.")
    
    filename = make_filename(banner_photo[0].filename)
    banner_photo[0].save(
        os.path.join(
            current_app.config['PHOTO_UPLOAD_PATH'],
            filename
        )
    )
    banner_photo_link = "/uploads/" + filename
    Exhibition(g.db).update_one(oid, {'banner_photo': banner_photo_link})
    return response_201


@api.route('/exhibition/<exhibition_id>/photo', methods=['PUT'])
@login_required('exhibition')
@Validator(bad_request)
@timer
def put_exh_photo_api_v1(
    exhibition_id=Route(str, rules=ObjectIdValid()),
    photos=File()
):
    """전시회 포토 리스트 업로드"""
    oid = ObjectId(exhibition_id)
    exhibition = Exhibition(g.db).find_one(oid)
    if exhibition['owner_id'] != g.user_id:
        return forbidden("You are not owner.")

    banner_photos = []
    for photo in photos:
        filename = make_filename(photo.filename)
        photo.save(os.path.join(current_app.config['PHOTO_UPLOAD_PATH'], filename))
        banner_photos.append("/uploads/" + filename)

    Exhibition(g.db).update_one(oid, {'contents': banner_photos})
    return response_201