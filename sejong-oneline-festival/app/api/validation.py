from datetime import datetime
from flask_validation_extended.rules import ValidationRule
from bson.objectid import ObjectId


class ObjectIdValid(ValidationRule):
    """ObjectId Validation"""
    @property
    def types(self):
        return str

    def invalid_str(self):
        return "This isn't ObjectId Format."

    def is_valid(self, data) -> bool:
        try:
            ObjectId(data)
            return True
        except:
            return False


class DatetimeFormatValid(ValidationRule):
    """YYY-MM-DD HH:MM:SS format validation"""
    @property
    def types(self):
        return str

    def invalid_str(self):
        return "This isn't YYYY-MM-DD Format."

    def is_valid(self, data) -> bool:
        try:
            datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
            return True
        except:
            return False