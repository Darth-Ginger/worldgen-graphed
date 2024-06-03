import inspect
import os
from apiflask import HTTPTokenAuth, Schema
from flask import app

import schemas

class Config:
    SECRET_KEY = os.getenv('API_SECRET', 'your_default_secret_key')
    WORLDS_DIR = os.path.join(os.path.dirname(__file__), 'Worlds')
    SYNC_LOCAL_SPEC = True
    LOCAL_SPEC_PATH = os.path.join(os.path.dirname(__file__), 'openapi.json')
    JSON_INDENT = 4
    DEBUG = True
    SCHEMA_CLASSES = {c: getattr(schemas, c) for c in dir(schemas) if inspect.isclass(getattr(schemas,c)) and issubclass(getattr(schemas,c), Schema)}
    AUTH = HTTPTokenAuth(scheme='ApiKey', header='X-API-KEY')
    db_config = {
        "DB_HOST": os.getenv('ARANGODB_HOST'),
        "DB_PORT": os.getenv('ARANGODB_PORT'),
        "DB_NAME": os.getenv('ARANGODB_DB'),
        "DB_USER": os.getenv('ARANGODB_USER'),
        "DB_PASS": os.getenv('ARANGODB_PASSWORD'),
        "SYS_DB_USER": os.getenv('ARANGODB_SYS_USER'),
        "SYS_DB_PASS": os.getenv('ARANGODB_SYS_PASSWORD')
    }
    

    app.security_schemes = {
        'ApiKeyAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY'
        }
    }