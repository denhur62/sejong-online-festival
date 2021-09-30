from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from config import config

# Collections
from .comment import Comment
from .esports import Esports
from .event import Event
from .event_form import EventForm
from .exhibition import Exhibition
from .log import Log
from .master_config import MasterConfig
from .user import User

MODELS = [
    Comment, Esports, Event, 
    EventForm, Exhibition,
    Log, MasterConfig, User
]


def get_cursor(uri=config.MONGODB_URI) -> MongoClient:
    """Get MongoDB Cursor"""
    return MongoClient(uri)


class ModelInitializer:

    def __init__(self):
        self.uri = config.MONGODB_URI
        self.db = config.MONGODB_NAME

    @property
    def cursor(self):
        return get_cursor(self.uri)

    def init_model(self):
        """Initializer All Process"""
        with self.cursor as cur:
            self.init_index(cur)
            self.init_author(cur)
            self.init_admins(cur)

    @staticmethod
    def init_index(cur):
        """Create Indexes each Collection"""
        for model in MODELS:
            model(cur).create_index()

    @staticmethod
    def init_author(cur):
        """Insert Author config"""
        MasterConfig(cur).insert_author('IML')

    @staticmethod
    def init_admins(cur):
        """Insert Admin User"""
        user_model = User(cur)
        roles = ['admin', 'esports', 'exhibition', 'event']
        user = user_model.schema
        for role in roles:
            user['user_id'] = "%s_%s" % (role, config.ADMIN_ID)
            user['password'] = generate_password_hash(config.ADMIN_PW)
            user['roles'] = [role]
            user['name'] = "[%s]관리자" % role
            user_model.insert_user(user)


