import os
from flask import Flask, render_template
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_mail import Mail
from application.models import User,Role
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
from application import workers
from flask_caching import Cache



app=None
celery=None
cache=None
def create_app():
    app=Flask(__name__, template_folder="templates")
    if os.getenv('ENV',"development")=="production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    JWTManager(app)
    CORS(app,origins="*")

    app.config["MAIL_SERVER"] = 'smtp.gmail.com'
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = 'vibhaashas@gmail.com'
    app.config["MAIL_PASSWORD"] = 'aqiadrwmyqptgktk'
    mail = Mail(app)
    app.app_context().push()

    # celery=workers.celery

    # app.config.update(
    # CELERY_BROKER_URL='redis://127.0.0.1:6379/1',
    # CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/2')
    # celery.Task=workers.ContextTask
    cache = Cache(app,config={'CACHE_TYPE': 'redis', 'CACHE_KEY_PREFIX': 'myapp'})
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_URL'] = 'redis://127.0.0.1:6379/0'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.app_context().push()
    return app,  cache
        
app,cache=create_app()



        

# import controllers
from application.controllers import *

@app.errorhandler(404)
def PageNotDefined(e):
    return render_template('404.html')


if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
    
     