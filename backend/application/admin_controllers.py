from flask import Flask, request, redirect, url_for,send_file
from application.database import db
from flask import render_template
from flask import current_app as app
from flask import jsonify
from application.sessions import *
from application.workers import *
from flask_jwt_extended import create_access_token, jwt_required
from application.models import *
from application.role_required import *
from main import cache




@app.route('/theatre', methods=['GET'])
@jwt_required()
@role_required(['Admin'])
def theatre():
    ven = all_theatre()
    ven_list = [{'id': v.vid, 'name': v.vname, 'place': v.vplace , 'capacity':v.vcapacity} for v in ven]

    return jsonify(ven_list) 


@app.route('/newTheatre', methods=['POST'])
@jwt_required()
@role_required(['Admin'])
def NewTheatre():
    data = request.form
    name = data.get("name")
    location = data.get("location")
    capacity = data.get("capacity")
    image = request.files.get("image")

    try:
        if image:
            # Read the image file as binary data
            image_data = image.read()
        else:
            image_data = None

        theatre = Venue(vname=name, vplace=location, vcapacity=capacity, vimage=image_data)

        db.session.add(theatre)
        db.session.commit()
        cache.delete('venues_and_shows')

        return {'msg': 'Theatre successfully added'}, 200
    except Exception as e:
        print(str(e))
        return {'error': 'Failed to add theatre', 'details': str(e)}, 500


@app.route('/deleteTheatre/<id>', methods=['POST'])
# @jwt_required()
# @role_required(['Admin'])
def method_name(id):
        if(deleteTheatre(id)):
            cache.delete('venues_and_shows')

            return {'msg':'Theatre successfully Deleted'}, 200
        else:
            return {'msg':'Theatre not found'}, 200


@app.route('/editTheatre/<id>', methods=['POST'])
@jwt_required()
@role_required(['Admin'])
def eTh(id):
    d=request.get_json()
    print(id,d.get('name'))
    print(type(d.get('name')))
    if(editTheatre(id,d.get('name'))):
        cache.delete('venues_and_shows')

        return {'msg':'Theatre successfully Edited'}, 200
    else:
        return {'msg':'Theatre not found'}, 200


@app.route('/addShow/<id>', methods=['POST'])
@jwt_required()
# @role_required(['Admin'])
def addS(id):
    data = request.json  # Use request.json to parse JSON data
    name = data.get("name")
    tags = data.get("tags")
    price = data.get("price")
    timing = data.get("timing")
    seats = data.get("seats")
    print(name,tags,price,timing,seats)
    
    try:

        AddShow(id,name,tags,price,timing,seats,booked=0,rate=0)
        cache.delete('venues_and_shows')


        return {'msg': 'Show successfully added'}, 200
    except Exception as e:
        print(str(e))
        return {'error': 'Failed to add Show', 'details': str(e)}, 500



@app.route('/getVenuesAndShows', methods=['GET'])
@jwt_required()
@role_required(['Admin'])
@cache.cached(timeout=30, key_prefix='venues_and_shows')
def getVenuesAndShows():
    return Th_Shows()

@app.route('/editShow/<id>', methods=['POST'])
@jwt_required()
@role_required(['Admin'])
def editS(id):
    d=request.get_json()
    # name    tags        price               timing        seats
    # print(id,d.get('name'),d.get('tags'),d.get('price'),d.get('timing'),d.get('seats'))
    if(EditShow(id,d.get('sname'))):
        cache.delete('venues_and_shows')

        return {'msg':'Show successfully Edited'}, 200
    else:
        return {'msg':'Failed adding Show'}, 200
    # return {"meg":"success!"},200


@app.route('/deleteShow/<id>', methods=['POST'])
@jwt_required()
@role_required(['Admin'])
def delSh(id):
    if(deleteShow(id)):
        cache.delete('venues_and_shows')

        return {'msg':'Theatre successfully Deleted'}, 200
    else:
        return {'msg':'Theatre not found'}, 200
    
@app.route('/show_summmary', methods=['GET'])
def show_summary():
    summary_show()

    # Encode the image as base64
    image_path = 'static/show_occupancy.png'
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    return jsonify({'show_image_base64': encoded_image})


@app.route('/theatre_summmary', methods=['GET'])
def theatre_summmary():
    summary_theatre()

    # Encode the image as base64
    image_path = 'static/theatre_occupancy.png'
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    return jsonify({'theatre_image_base64': encoded_image})


@app.route('/get_summary_image/', methods=['GET'])
def get_summary_image():
    summary_show()
    image_path = 'static/show_occupancy.png'
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    return jsonify({'show_image_base64': encoded_image})

@app.route('/get_th_data/<vid>',methods=['GET'])
def theatre_data(vid):
    a = generate_th_csv.delay(vid)
    return {
        "Task_ID" : a.id,
        "Task_State" : a.state,
        "Task_Result" : a.result
    }

@app.route("/download_file/<id>",methods=['GET'])
def download_file(id):
    file_path = f"static/th_data_{id}.csv"
    # print(file_path)
    return send_file(file_path,as_attachment=True)