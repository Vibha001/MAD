from .database import db
# from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import backref
from sqlalchemy import LargeBinary


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    email = db.Column(db.String, unique=True, nullable=True)
    username = db.Column(db.String, unique=False, nullable=True)  
    password = db.Column(db.String, nullable=False)
    last_active = db.Column(db.DateTime)
    # fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    # roles = db.Column(db.String, db.ForeignKey("role.name"))
    


class Venue(db.Model):
    __tablename__='venue'
    vid=db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    vname=db.Column(db.String,nullable=False)
    vplace=db.Column(db.String)
    vcapacity=db.Column(db.Integer,nullable=False)
    vimage = db.Column(LargeBinary)

class Show(db.Model):
    __tablename__='show'
    sid=db.Column(db.Integer,unique=True, autoincrement=True, primary_key=True )
    sname=db.Column(db.String)
    srate=db.Column(db.Integer)
    stags=db.Column(db.String,nullable=False)
    sprice=db.Column(db.Integer)
    time=db.Column(db.String, nullable=False )
    seats=db.Column(db.Integer)
    booked=db.Column(db.Integer)
    simage = db.Column(LargeBinary)
    
class Booking(db.Model):
    __tablename__='booking'
    id=db.Column(db.Integer,unique=True, autoincrement=True, primary_key=True )
    tickets=db.Column(db.Integer)
    price=db.Column(db.Integer)
    uid=db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False)
    sid=db.Column(db.Integer, db.ForeignKey("show.sid"), primary_key=True, nullable=False)
    vid=db.Column(db.Integer, db.ForeignKey("venue.vid"), primary_key=True, nullable=False)
    date= db.Column(db.DateTime)

class VenShow(db.Model):
    __tablename__='venue_Show'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    vid=db.Column(db.Integer, db.ForeignKey("venue.vid"), primary_key=True, nullable=False)
    sid=db.Column(db.Integer, db.ForeignKey("show.sid"), primary_key=True, nullable=False)
