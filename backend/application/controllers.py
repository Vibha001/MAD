from flask import Flask, request, redirect, url_for
from application.database import db
from flask import render_template,send_file
from flask import current_app as app
from application.sessions import *
from io import BytesIO
from application.admin_controllers import *
from application.user_controllers import *
import time
from application.models import User
from application import workers
from .workers import * #celery,
from datetime import datetime
from flask_restful import fields, marshal
from main import cache
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from application.models import User 
from application.role_required import *

test={
    'msg':fields.String,
}

@app.route("/",methods=["GET","POST"])
def home():
    
    if request.method=="GET":
        return render_template("home.html")
    
    if request.method=="POST":
        if request.form['user'] == 'admin':
            return redirect(url_for('home_ad'))

        elif request.form['user'] == 'user':
            return redirect(url_for('home_user'))
    

@app.route("/admin_register",methods=["POST"])
def ad_reg():
    # print("1")
    data = request.get_json()

    if data.get('email') and data.get('password'):
        # print("2")
        here = db.session.query(User).filter(User.email==data['email']).first()
        if here :
            # print("3")
            r_here=db.session.query(RolesUsers).filter(RolesUsers.user_id==here.id).first()
            if r_here and r_here.role_id==1 :
                # print("4")
                return {'message':'Admin exists'} , 200
            else:
                # print("5")
                ad_r=RolesUsers(user_id=here.id,role_id=1)
                db.session.add(ad_r)
                db.session.commit() 
                return {'message':'Admin role added'} , 200
        else:
            # print("6")
            ad=User(email=data['email'],username=data['username'],password=generate_password_hash(data['password']))
            db.session.add(ad)
            db.session.commit() 
            ad_r=RolesUsers(user_id=ad.id,role_id=1)
            db.session.add(ad_r)
            db.session.commit() 
            return {'message':'Admin created and added'} , 200 

@app.route('/login_admin',methods=["POST"])
@cache.cached(timeout=50, key_prefix='ad_log')
def ad_login():
    d=request.get_json()
    # print("1")
    if d.get('email') and d.get('password'):
        # print("2")
        here = db.session.query(User).filter(User.email==d['email']).first()
        u_role  = db.session.query(RolesUsers).filter(RolesUsers.user_id==here.id).first()
        # print(here.email)
        # print(u_role)
        try:
            # print(type(u_role.user_id))
            # print("3")
            if here and check_password_hash(here.password,d['password']) and u_role.role_id==1:
                # print("4")
                iden={'id':here.id, 'email':here.email, 'username':here.username}
                access_token = create_access_token(identity=iden,expires_delta=timedelta(5))
                return {'message':'Login Succcessful','access_token':access_token,'identity':iden,'role':'admin'} , 200
            else:
                # print("5")
                return {'message':'Invalid email or password or Unauthorized access'} , 409
        except Exception as e:
            # print("6")
            return {'message':'Invalid email or password or Unauthorized access'} , 402
            
    else:
        return {'message':'Give Complete Details'} , 401

@app.route('/login_user',methods=["POST"])
@cache.cached(timeout=50, key_prefix='u_log')
def u_login():
    d=request.get_json()
    print("1")
    if d.get('email') and d.get('password'):
        print("2")
        here = db.session.query(User).filter(User.email==d['email']).first()
        u_role  = db.session.query(RolesUsers).filter(RolesUsers.user_id==here.id).first()
        try:
            # u_role  = db.session.query(RolesUsers).filter(RolesUsers.user_id==d['id']).first()
            print("3")
            if here and check_password_hash(here.password,d['password']) and u_role.role_id==2:
                print("4")
                # save_login(d['email'])
                # here.last_active = str(datetime.utcnow())
                # db.session.add(here)
                # db.session.commit()          # UTC + 05 : 30 = IST time 
                iden={'id':here.id, 'email':here.email, 'username':here.username}
                access_token = create_access_token(identity=iden,expires_delta=timedelta(5))
                # here.last_active = "now" #str(datetime.utcnow())
                # db.session.add(here)
                # db.session.commit()  
                return {'message':'Login Succcessful','access_token':access_token,'identity':iden,'role':'user'} , 200
            else:
                print("5")
                return {'message':'Invalid email or password or Unauthorized access'} , 402
        except Exception as e:
            print("6")
            return {'message':'Invalid email or password or Unauthorized access'} , 402
            
    else:
        return {'message':'Give Complete Details'} , 401


@app.route('/aaa')
# @login_required
def aaaaa():
    return marshal({"msg":"hello"},test)



@app.route("/user_register",methods=["POST"])
def user_reg():
    data = request.get_json()
    # print("1")

    if data.get('email') and data.get('password'):
        # print("2")
        here = db.session.query(User).filter(User.email==data['email']).first()
        if here :
            # print("3")
            r_here=db.session.query(RolesUsers).filter(RolesUsers.user_id==here.id).first()
            if r_here and r_here.role_id==0 :
                # print("4")
                return {'message':'User exists'} , 200
            else:
                # print("5")
                ad_r=RolesUsers(user_id=here.id,role_id=2)
                db.session.add(ad_r)
                db.session.commit() 
                return {'message':'User role added'} , 200
        else:
            # print("6")
            ad=User(email=data['email'],username=data['username'],password=generate_password_hash(data['password']))
            db.session.add(ad)
            db.session.commit() 
            ad_r=RolesUsers(user_id=ad.id,role_id=2)
            db.session.add(ad_r)
            db.session.commit() 
            return {'message':'User created and added'} , 200 

@app.route('/aaaa',methods=["GET"])
@jwt_required()
@role_required(['Admin'])
def aaahg():
    return {'msg':'in!'},200



@app.route('/getVenueImage/<int:vid>', methods=['GET'])
def get_venue_image(vid):
    venue = Venue.query.get(vid)
    if venue and venue.vimage:
        return send_file(BytesIO(venue.vimage), mimetype='image/jpeg')
    else:
        # Return a default image or an error image if no image is found
        return send_file('static/default_V.jpg', mimetype='image/jpg')

@app.route('/getShowImage/<int:sid>', methods=['GET'])
def get_show_image(sid):
    show = Show.query.get(sid)
    if show and show.simage:
        return send_file(BytesIO(show.simage), mimetype='image/jpeg')
    else:
        # Return a default image or an error image if no image is found
        return send_file('static/default_S.jpg', mimetype='image/jpg')


@app.route('/save_login_time', methods=['POST'])
def save_login_time():
    data = request.get_json()
    print(data.get("id"))
    user = db.session.query(User).filter(User.id==data.get("id")).first()
    user.last_active = datetime.utcnow()
    db.session.add(user)
    db.session.commit() 
    return {'msg':'logging saved'},200

# @app.route('/HELLO', methods=['GET'])
# def GHELLO():
#     job = celery.send_task('application.workers.say_hello', args=["Vibha"])
#     resullt = job.wait()
#     return str(resullt),200

@app.route('/HELLO', methods=['GET'])
def GHELLO():
    print("now in flask")
    job = workers.Curr_time.apply_async(countdown=2,expires=10)
    # time.sleep(10)
    resullt = job.wait()
    return str(resullt),200