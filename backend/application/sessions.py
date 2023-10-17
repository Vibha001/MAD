from application.database import db
from application.models import RolesUsers, Role, Show, Booking, User, VenShow, Venue
from flask import jsonify, url_for
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime
# from main import cache


#################################### ADMIN FUNCTIONS ######################################################

def all_theatre():
    # from main import cache
    ven=db.session.query(Venue).all()
    # cache.set('my_cached_data', ven, timeout=30, key_prefix='theatreData')
    return ven

def deleteTheatre(id):
    v=db.session.query(Venue).filter((Venue.vid==id)).first()
    new=db.session.query(VenShow).filter((VenShow.vid==id)).all()
    #print(new[0])
    if v is None:
        return False
    else:
        db.session.delete(v)
        db.session.commit()
        if new is not None:
            for sh in new:
                sid=sh.sid
                dd=db.session.query(Show).filter((Show.sid==sid)).first()
                db.session.delete(dd)
                db.session.commit()
            #print(new)
            for sh in new:
                db.session.delete(sh)
                db.session.commit()
            return True

    

    return "Theater and associated VenShow entries deleted successfully"


def editTheatre(id,name):
    v=db.session.query(Venue).filter(Venue.vid==id).first()
    v.vname=name
    db.session.add(v)
    db.session.commit()
    return True

def AddShow(id,name,tags,price,timing,seats,booked,rate):
    exist = db.session.query(Show).filter(Show.sname==name).first()
    if exist and exist.time == timing:
        print("cannot add show")
        return "cannot add show"
    new=Show(sname=name, stags=tags, sprice=price, time=timing, seats=seats,booked=booked,srate=rate)
    db.session.add(new)
    db.session.commit()
    s=new.sid
    newVS=VenShow(vid=id, sid=s)
    db.session.add(newVS)
    db.session.commit()

# @cache.cached(timeout=30,key_prefix='vanues_anD_shows')
def Th_Shows():
    # cache = current_app.extensions['cache']  
    venues = Venue.query.all()
    venue_data = {}

    for venue in venues:
        shows = Show.query.join(VenShow).filter(VenShow.vid == venue.vid).all()
        show_data = []
        
        for show in shows:
            show_info = {
                'sid': show.sid,
                'sname': show.sname,
                'srate': show.srate,
                'stags': show.stags,
                'sprice': show.sprice,
                'time': show.time,
                'seats': show.seats,
                'booked': show.booked,
            }
            show_data.append(show_info)

        venue_info = {
            'vid': venue.vid,
            'vname': venue.vname,
            'vplace': venue.vplace,
            'vcapacity': venue.vcapacity,
            'vimage_url': url_for('get_venue_image', vid=venue.vid),
            'shows': show_data,
        }
        venue_data[venue.vid] = venue_info
    
    # cache.set('Venue_Data', jsonify( venue_data), timeout=30)

    return jsonify( venue_data)


def EditShow(id,name):
    print(id,name)
    show = db.session.query(Show).filter(Show.sid == id).first()
    print(show.sname)
    show.sname = name
    db.session.add(show)
    db.session.commit()
    return True

def deleteShow(id):
    print("dels 1")
    new=db.session.query(VenShow).filter((VenShow.sid==id)).first()
    v=db.session.query(Show).filter((Show.sid==id)).first()
    print(new.sid)
    print(v.sid)
    if new is not None:
        print("dels 2")
        db.session.delete(new)
        db.session.delete(v)
        db.session.commit()
        return True

def summary_show():
    shows = db.session.query(Show).all()
    show_names, occupancy_ratios = [], []

    for show in shows:
        show_names.append(show.sname)
        occupancy_ratio = show.booked / show.seats
        occupancy_ratios.append(occupancy_ratio)

    plt.bar(show_names, occupancy_ratios)
    plt.xlabel("Shows")
    plt.ylabel("Percentage of Seats Filled/Booked")
    plt.title("Seat Occupancy for Different Shows")
    plt.savefig('static/show_occupancy.png', dpi=100)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the image bytes in Base64
    encoded_image = base64.b64encode(buffer.read()).decode('utf-8')

    return jsonify({'theatre_image_base64': encoded_image})

def summary_theatre():
    venues = db.session.query(Venue).all()
    theatre_names, theatre_occupancy_ratios = [], []

    for venue in venues:
        theatre_names.append(venue.vname)
        
        # Query the shows for each venue using the junction table venshow
        shows = db.session.query(Show).join(VenShow).filter(VenShow.vid == venue.vid).all()
        
        total_booked_seats = sum([show.seats for show in shows])
        total_seats = sum([show.vcapacity for show in venues])
        
        # Check if total_seats is zero before calculating the ratio
        if total_seats == 0:
            theatre_occupancy_ratio = 0
        else:
            theatre_occupancy_ratio = total_booked_seats / total_seats
        
        theatre_occupancy_ratios.append(theatre_occupancy_ratio)

    plt.bar(theatre_names, theatre_occupancy_ratios)
    plt.xlabel("Theatres")
    plt.ylabel("Percentage of Occupancy")
    plt.title(" Occupancy by Different Theatres")
    plt.savefig('static/theatre_occupancy.png', dpi=100)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the image bytes in Base64
    encoded_image = base64.b64encode(buffer.read()).decode('utf-8')

    return jsonify({'theatre_image_base64': encoded_image})

def ThDetails(vid):
    venue = Venue.query.get(vid)
    shows = Show.query.join(VenShow).filter(VenShow.vid == vid).all()
    show_data = []
    for show in shows:
        show_info = {
            'sid': show.sid,
            'sname': show.sname,
            'srate': show.srate,
            'stags': show.stags,
            'sprice': show.sprice,
            'time': show.time,
            'seats': show.seats,
            'booked': show.booked,
        }
        show_data.append(show_info)

    return show_data
    






#################################### USER FUNCTIONS ########################################################

def BookShow(id,show,seats,price,venue):
    new=Booking(uid=id, sid=show, price=price, tickets=seats,vid=venue)
    s = db.session.query(Show).filter(Show.sid==show).first()
    s.booked += int(seats)
    # new.date = str(datetime.now())
    db.session.add(new)
    db.session.add(s)
    db.session.commit()
    save_b_time(new.id)
    return True

def save_b_time(id):
    try:
        here = db.session.query(Booking).filter(Booking.id==id).first()
        current_datetime = datetime.now()  # Get the current date and time
        here.date = current_datetime
        db.session.add(here)
        db.session.commit() 
        print("date time saved")
        # return 
    except Exception as e:
        print(e)
        print("could not save time")
        # return

def Tag_Shows(tag):
    venues = Venue.query.all()
    venue_data = {}

    for venue in venues:
        shows = Show.query.join(VenShow).filter(VenShow.vid == venue.vid, Show.stags == tag).all()
        show_data = []
        
        for show in shows:
            show_info = {
                'sid': show.sid,
                'sname': show.sname,
                'srate': show.srate,
                'stags': show.stags,
                'sprice': show.sprice,
                'time': show.time,
                'seats': show.seats,
                'booked': show.booked,
            }
            show_data.append(show_info)

        venue_info = {
            'vid': venue.vid,
            'vname': venue.vname,
            'vplace': venue.vplace,
            'vcapacity': venue.vcapacity,
            'vimage_url': url_for('get_venue_image', vid=venue.vid),
            'shows': show_data,
        }
        venue_data[venue.vid] = venue_info

    return jsonify(venue_data)


def Loc_Shows(location):
    venues = Venue.query.filter_by(vplace=location).all()
    venue_data = {}

    for venue in venues:
        shows = Show.query.join(VenShow).filter(VenShow.vid == venue.vid).all()
        show_data = []

        for show in shows:
            show_info = {
                'sid': show.sid,
                'sname': show.sname,
                'srate': show.srate,
                'stags': show.stags,
                'sprice': show.sprice,
                'time': show.time,
                'seats': show.seats,
                'booked': show.booked,
            }
            show_data.append(show_info)

        venue_info = {
            'vid': venue.vid,
            'vname': venue.vname,
            'vplace': venue.vplace,
            'vcapacity': venue.vcapacity,
            'vimage_url': url_for('get_venue_image', vid=venue.vid),
            'shows': show_data,
        }
        venue_data[venue.vid] = venue_info

    return jsonify(venue_data)


def save_login(email):
    try:
        here = db.session.query(User).filter(User.email==email).first()
        here.last_active = str(datetime.now())
        db.session.add(here)
        db.session.commit() 
        print("date time saved")
        # return 
    except Exception as e:
        print("could not save time")
        # return


def user_booked_shows(user_id):
    bookings = Booking.query.filter_by(uid=user_id).all()
    
    user_data = {
        'user_id': user_id,
        'booked_shows': []
    }

    for booking in bookings:
        show = Show.query.get(booking.sid)
        venue = Venue.query.get(booking.vid)

        if show and venue:
            show_info = {
                'sid': show.sid,
                'sname': show.sname,
                'srate': show.srate,
                'stags': show.stags,
                'sprice': show.sprice,
                'time': show.time,
                'seats': show.seats,
                'booked': show.booked,
            }
            venue_info = {
                'vid': venue.vid,
                'vname': venue.vname,
                'vplace': venue.vplace,
                'vcapacity': venue.vcapacity,
                'vimage_url': url_for('get_venue_image', vid=venue.vid),  # You can replace this with the actual URL
            }
            user_data['booked_shows'].append({
                'show': show_info,
                'venue': venue_info,
                'tickets': booking.tickets,
                'price': booking.price,
                'date' : booking.date,
            })

    return jsonify(user_data)


def rate(sid,rate):
    show = db.session.query(Show).filter(Show.sid == sid).first()
    print(show.sname)
    show.srate = rate
    db.session.add(show)
    db.session.commit()
    return True


def get_profile_of(id):
    user = db.session.query(User).filter(User.id == id).first()

    if user is not None:
        roles_users = db.session.query(RolesUsers).filter(RolesUsers.user_id == id).first()

        if roles_users is not None:
            role = db.session.query(Role).filter(Role.id == roles_users.role_id).first()

            info = {
                'email': user.email,
                'username': user.username,
                'role': role.name if role else None,
                'role_descr': role.description if role else None
            }
            return jsonify(info)
        else:
            return jsonify({'error': 'RolesUsers not found for the user'}), 404
    else:
        return jsonify({'error': 'User not found'}), 404
