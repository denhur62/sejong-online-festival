"""
Comments API
응원 이벤트 관련 API
"""

from flask_validation_extended import Validator,Json,Route
from flask_validation_extended import ValidationRule
from app.api import response_200, bad_request , response_201
from app.api.api_v1 import api_v1 as api
from app.api.decorator import login_required, timer
from model.mongodb import Comment,User
from app.api.validation import ObjectIdValid
from flask import g
from bson.objectid import ObjectId

@api.route('/comment/<content_id>' ,methods=['PUT'])
@timer
@Validator(bad_request)
@login_required("general")
def comment_commit_api_v1(
    comments=Json([str,int]),
    content_id=Route(str,rules=ObjectIdValid())
):
    comments = str(comments)
    author_id=g.user_id
    documents = {'user_id':'author_id', 'name':'author_name', 
    'major':'author_major'}
    data = User(g.db).get_user_info(author_id)
    documents=dict((documents[key], value) for (key, value) in data[0].items())
    documents['content_id']=ObjectId(content_id)
    documents['comment']=comments
    Comment(g.db).commit_comment(documents)
    return response_201

@api.route('/comment/<content_id>/<_skip>/<_limit>')
@timer
@Validator(bad_request)
def get_commit_api_vi(
    content_id=Route(str,rules=ObjectIdValid()),
    _skip=Route(int),
    _limit=Route(int)
):
    documents=Comment(g.db).get_comment(content_id,_skip,_limit)
    return response_200(documents)

