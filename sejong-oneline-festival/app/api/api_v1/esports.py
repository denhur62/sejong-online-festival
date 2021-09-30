"""
Esports API
이스포츠 이벤트 관련 API 
"""
from flask_validation_extended import Validator, Query
from flask_validation_extended import ValidationRule
from app.api import response, bad_request
from app.api.api_v1 import api_v1 as api
from app.api.decorator import timer