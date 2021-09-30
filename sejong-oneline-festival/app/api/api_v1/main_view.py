"""
MainView API
축제 일정, 연예인 라인업, 라이브 스트리밍과 같은 메인 뷰 API
"""
from flask_validation_extended import Validator, Query
from flask_validation_extended import ValidationRule
from app.api import response_200, bad_request
from app.api.api_v1 import api_v1 as api
from app.api.decorator import timer