"""
Event & Form API
기타 이벤트(설문조사, 깜짝 퀴즈) 등을 다루는 API
"""
from flask_validation_extended import Validator, Query
from flask_validation_extended import ValidationRule
from app.api import response, bad_request
from app.api.api_v1 import api_v1 as api
from app.api.decorator import timer