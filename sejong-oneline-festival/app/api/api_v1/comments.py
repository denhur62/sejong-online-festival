"""
Comments API
응원 이벤트 관련 API
"""

from flask_validation_extended import Validator,Json,Route
from flask_validation_extended import ValidationRule
from app.api import response_200, bad_request
from app.api.api_v1 import api_v1 as api
from app.api.decorator import timer
from model.mongodb import Comment,User
from app.api.validation import ObjectIdValid
from flask import g

@api.route('/comment' ,methods=['POST'])
@timer
@Validator(bad_request)
def comment_commit_api_v1(
    author_id=Json(str),
    object_id=Json(str,rules=ObjectIdValid()),
    comments=Json(str)
):
    documents = {'user_id':'author_id', 'name':'author_name', 
    'major':'author_major'}
    data = User(g.db).get_user_info(author_id)
    documents=dict((documents[key], value) for (key, value) in data[0].items())
    documents['content_id']=object_id
    documents['comment']=comments
    Comment(g.db).commit_comment(documents)
    return response_200()

@api.route('/comment/<object_id>')
@timer
@Validator(bad_request)
def get_commit_api_vi(
    object_id=Route(str,rules=ObjectIdValid())
):
    documents=Comment(g.db).get_comment(object_id)
    return response_200(documents)

