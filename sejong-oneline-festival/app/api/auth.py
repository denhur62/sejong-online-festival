"""
Auth API
"""
from flask import Blueprint, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_validation_extended import Validator, Json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.api import response_200, bad_request
from controller.sejong_auth import SejongAuth
from controller.user import make_user_document
from model.mongodb import User

auth  = Blueprint('auth', __name__)


@auth.route('/signin', methods=['POST'])
@Validator(bad_request)
def auth_signin_api(
    id=Json(str),
    pw=Json(str)
):
    user_model = User(g.db)
    user = user_model.get_identity(id)
    
    # SignUp
    if not user:
        sejong_auth = SejongAuth()
        auth_resp = sejong_auth.do_sejong(id, pw)

        if not auth_resp['result']:
            return bad_request('user_id is not exists.')

        new_user = make_user_document(
            user_model.schema, id, 
            generate_password_hash(pw),
            auth_resp
        )

    
    # Password check
    elif not check_password_hash(user['password'], pw):
        return bad_request('password is incorrect.')

    return response_200({
        'access_token': create_access_token(
            identity={'user_id':id, 'roles': user['roles']}
        )
    })