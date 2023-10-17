import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = True
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    CELERY_BROKER_URL = "127.0.0.1:6379/1"
    CELERY_RESULT_BACKEND = "127.0.0.1:6379/2"
    REDIS_URL = "redis://127.0.0.1:6379"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir,"../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(SQLITE_DB_DIR,"proj.sqlite3")
    DEBUG = True
    SECRET_KEY = "tbJNSwbzeOzOfLsphgKR140cmKqbnJzx"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "1CfWXSNNP1dZ7Zyqzn2igua4cdTDA8TL"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = True

    JWT_TOKEN_LOCATION = ["headers"]
    CELERY_BROKER_URL = "127.0.0.1:6379/1"
    CELERY_RESULT_BACKEND = "127.0.0.1:6379/2"

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'vibhaashas@gmail.com'
    MAIL_PASSWORD = 'aqiadrwmyqptgktk'

    REDIS_URL = "redis://127.0.0.1:6379"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379