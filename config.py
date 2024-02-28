
import os
from sqlalchemy import create_engine
import urllib

class Config(object):
    SECRET_KEY = 'clave_nueva'
    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:10012003@127.0.0.1/practicasdbidgs803'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
