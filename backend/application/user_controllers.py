from flask import Flask, request, redirect, url_for,send_file
from application.database import db
from flask import render_template
from flask import current_app as app
from flask import jsonify
from application.sessions import *
from flask_jwt_extended import create_access_token, jwt_required
from application.models import *
from application.role_required import *
from main import cache


@app.route('/getVandS', methods=['GET'])
@jwt_required()
@role_required(['User'])
@cache.cached(timeout=50, key_prefix='u__dash')
def getVenuesandShows():
    return Th_Shows()


@app.route('/book/<id>', methods=['POST'])
@jwt_required()
@role_required(['User'])
def book(id):
    cache.delete('u__dash')
    data=request.get_json()
    show = data.get("showId")
    venue = data.get("venueId")
    seats = data.get("numberOfSeats")
    price = data.get("price")
    if(BookShow(id,show,seats,price,venue)): #BookShow(id,show,seats,price,venue)
        return {'msg':'Show Successfully Booked by '+id}, 200
    else:
        return {'msg':'Error! Show not Booked'}, 200


@app.route('/tag_result', methods=['POST'])
@jwt_required()
@role_required(['User'])
def tag_result():
    cache.delete('u__dash')
    data=request.get_json()
    tags = data.get("tags")
    return Tag_Shows(tags)


@app.route('/loc_result', methods=['POST'])
@jwt_required()
@role_required(['User'])
def loc_result():
    cache.delete('u__dash')
    data=request.get_json()
    tags = data.get("location")
    return Loc_Shows(tags)


@app.route('/user_booked_shows/<id>', methods=['GET'])
@jwt_required()
@role_required(['User'])
def user_booked(id):
    return user_booked_shows(id)

@app.route('/rating/<sid>', methods=['POST'])
@jwt_required()
# @role_required(['User'])
def give_rating(sid):
    data=request.get_json()
    print(data.get("rating"))
    rating = data.get("rating")
    if rating is not None:
        if rate(sid, data.get("rating")):
            print("Rating Successful ")
            return {'msg':'Rating Successful'},  200
        else:
            print("Unable to Rate ")
            return {'msg':'Unable to Rate'}, 200
    else:
        print("Rating data is missing ")
        return {'msg':'Rating data is missing'}, 200
    

@app.route('/profile/<id>', methods=['GET'])
@jwt_required()
@role_required(['User'])
@cache.memoize(3600)
def get_profile(id):
    return get_profile_of(id)

