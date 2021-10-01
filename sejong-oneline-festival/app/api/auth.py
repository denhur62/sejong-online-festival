"""
Auth API
"""
from flask import Blueprint, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_validation_extended import Validator, Json, List, In
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.api import response_200, bad_request
from app.api.decorator import login_required, timer
from controller.sejong_auth import SejongAuth
from controller.user import make_user_document
from model.mongodb import User

auth  = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
@login_required('admin')
@Validator(bad_request)
@timer
def auth_signup_api(
    id=Json(str),
    pw=Json(str),
    name=Json(str),
    roles=Json(List(str))
):
    user_model = User(g.db)
    if user_model.get_identity(id):
        return bad_request("User already exists.")

    user = {
        'user_id': id,
        'password': generate_password_hash(pw),
        'name': name,
        'roles': roles,
    }

    user_model.insert_user(user)

    return response_200({
        'access_token': create_access_token(
            identity={'user_id': id, 'roles': user['roles']}
        ),
        'access_roles': user['roles']
    })

@auth.route('/signin', methods=['POST'])
@Validator(bad_request)
@timer
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
            return bad_request('Sejong auth failed.')
        new_user = make_user_document(
            user_model.schema, id, pw, auth_resp
        )
        user_model.insert_user(new_user)
        user['roles'] = new_user['roles']

    # Password check
    elif not check_password_hash(user['password'], pw):
        return bad_request('Incorrect password.')

    return response_200({
        'access_token': create_access_token(
            identity={'user_id':id, 'roles': user['roles']}
        ),
        'access_roles': user['roles']
    })


@auth.route("/admin-test")
@login_required("admin")
def auth_admin_test():
    return response_200("Welcome, admin. " + g.user_id)


@auth.route("/esports-test")
@login_required("esports")
def auth_esports_test():
    return response_200("Welcome, esports. " + g.user_id)


@auth.route("/exhibition-test")
@login_required("exhibition")
def auth_exhibition_test():
    return response_200("Welcome, exhibition. " + g.user_id)


@auth.route("/event-test")
@login_required("event")
def auth_event_test():
    return response_200("Welcome, event. " + g.user_id)


@auth.route("/general-test")
@login_required("general")
def auth_general_test():
    return response_200("Welcome, general. " + g.user_id)