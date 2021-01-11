from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
import datetime as DT

from flask import Flask, render_template, request, session, send_from_directory, url_for, redirect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from base64 import b64encode, b64decode
import re
import requests
import os
from uuid import uuid4

DATA_ROOT = './data'
PROFILE_DIR = os.path.join(DATA_ROOT, 'profile')
VEHICLE_DIR = os.path.join(DATA_ROOT, 'vehicle')
DOCS_DIR = os.path.join(DATA_ROOT, 'docs')

# Initialize SQL Alchemy
engine = create_engine('mysql://admin:adminPassword@localhost/shotgundb?charset=utf8mb4')
Base = automap_base()
metadata = MetaData()
Base.prepare(engine, reflect=True)

# Shortcuts to database tables
UserTable = Base.classes.user
DriverTable = Base.classes.driver
DriverCertificationTable = Base.classes.drivercertificationapplication
EventTable = Base.classes.event
RideTable = Base.classes.ride
PaymentMethodTable = Base.classes.paymentmethod
CreditCardTable = Base.classes.creditcard
PayPalTable = Base.classes.paypalaccount
UserRatingTable = Base.classes.userrating
DriverRatingTable = Base.classes.driverrating
ApplicationTable = Base.classes.application
FutureEventView = Table("future_events", metadata, autoload=True, autoload_with=engine)
AvgDriverRatingView = Table("avg_driver_rating", metadata, autoload=True, autoload_with=engine)
AvgUserRatingView = Table("avg_user_rating", metadata, autoload=True, autoload_with=engine)

# Start
db_session = Session(engine)
app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5rt2L"F4xFz\n\xec]/'

# Create data directories
if not os.path.exists(PROFILE_DIR):
    os.makedirs(PROFILE_DIR)
if not os.path.exists(VEHICLE_DIR):
    os.makedirs(VEHICLE_DIR)
if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)


def is_past_date(date_string):
    date = DT.datetime.strptime(date_string, '%a, %d %b %Y').date()
    return date < DT.datetime.now().date()


def is_valid_geolocation(lat, lng):
    # Validates geographic coordinates.
    try:
        return len(lat) <= 16 and len(lng) <= 16 and 90 > float(lat) > -90 and 180 > float(lng) > -180
    except ValueError:
        return False


def is_valid_rating(stars):
    try:
        return 1 <= int(stars) <= 5
    except ValueError:
        return


def is_valid_username(username):
    # Validates a username.
    return re.match(r'^[A-Za-z0-9_-]+$', username) and 3 <= len(username) <= 16


def is_valid_password(password):
    # Validates a password.
    return password.isprintable() and len(password) >= 6


def save_image(data, filename):
    # Saves a base64-encoded image.
    with open(filename, 'wb') as f:
        f.write(b64decode(data.encode('ascii')))


def check_image_ext(filename):
    # Checks whether the image file format is allowed.
    _, ext = os.path.splitext(filename)
    return ext in ['.jpg']


@app.route('/api/user', methods=['POST', 'GET'])
def UserListAdd():
    if request.method == 'POST':
        # Get request data
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        surname = request.form['surname']
        profile_picture_data = request.form.get('profile_picture')

        # Validate data
        if not is_valid_username(username):
            return {'error': 'A username must be between 3 and 16 characters. Letters, numbers, underscores and dashes only.'}
        if not is_valid_password(password):
            return {'error': 'A password must be at least 6 characters long.'}

        # Check if username is already taken
        exists = db_session.query(UserTable).filter_by(username=username).first()
        if exists:
            return {'error': 'Username is already taken.'}

        # Save profile picture
        if profile_picture_data:
            profile_picture = '{}.jpg'.format(uuid4())
            save_image(profile_picture_data, os.path.join(PROFILE_DIR, profile_picture))
        else:
            profile_picture = 'default.jpg'

        # Hash password
        pwd_hash = generate_password_hash(password)

        # Insert user into database
        newUser = UserTable(username=username, password=pwd_hash,
                            first_name=first_name, surname=surname, profile_picture=profile_picture)
        db_session.add(newUser)
        db_session.commit()
        return {'status': 'success'}, 200
    elif request.method == 'GET':
        try:
            userQuery = db_session.query(UserTable, AvgDriverRatingView, AvgUserRatingView).join(
                AvgDriverRatingView, AvgDriverRatingView.columns.ratee == UserTable.username, isouter=True).join(
                AvgUserRatingView, AvgUserRatingView.columns.ratee == UserTable.username, isouter=True).all()

            # Return all data except from passwords
            userDict = {'users': [{
                'username': u.user.username,
                'first_name': u.user.first_name,
                'surname': u.user.surname,
                'profile_picture': u.user.profile_picture,
                'avg_user_rating': str(u.average_user_rating)[:3],
                'avg_driver_rating': str(u.average_driver_rating)[:3]
            } for u in userQuery]
            }
            return userDict
        except NoResultFound:
            return {'error': 'No users exist in the database'}
        except Exception as e:
            return {'error': str(e)}


@app.route('/api/user/<string:username>', methods=['PUT', 'GET', 'DELETE'])
def User(username):
    if request.method == 'PUT':
        # Update user data
        if request.form:
            user = db_session.query(UserTable).filter(UserTable.username == username).one()
            if 'first_name' in request.form:
                user.first_name = request.form['first_name']
            if 'surname' in request.form:
                user.surname = request.form['surname']
            if 'profile_picture' in request.form:
                user.profile_picture = '{}.jpg'.format(uuid4())
                save_image(request.form['profile_picture'], os.path.join(PROFILE_DIR, user.profile_picture))
            db_session.commit()
        return {'status': 'success'}
    elif request.method == 'GET':
        # return a user data
        # Maybe do a /api/sth for data as json and a /sth for frontend
        # Maybe /api/user/<user_id> returns json user data and /user loads a user profile and calls
        # multiple api endpoints like /api/rating/ or /api/driver/
        try:
            userQuery = db_session.query(UserTable, AvgDriverRatingView, AvgUserRatingView).join(
                AvgDriverRatingView, AvgDriverRatingView.columns.ratee == UserTable.username, isouter=True).join(
                AvgUserRatingView, AvgUserRatingView.columns.ratee == UserTable.username, isouter=True).filter(
                UserTable.username == username).one()
            # return all data except from passwords
            userDict = {'username': userQuery.user.username,
                        'password': userQuery.user.password,
                        'first_name': userQuery.user.first_name,
                        'surname': userQuery.user.surname,
                        'profile_picture': userQuery.user.profile_picture,
                        'avg_user_rating': str(userQuery.average_user_rating)[:3],
                        'avg_driver_rating': str(userQuery.average_driver_rating)[:3]}
            return userDict
        except NoResultFound:
            return {'error': 'User with provided credentials does not exist in the database'}
        except Exception as e:
            return {'error': str(e)}
    elif request.method == 'DELETE':
        # Update the events that were created by this user
        events = db_session.query(EventTable).filter_by(creator=username)
        for row in events:
            row.creator = None

        # Delete user rides
        rides = db_session.query(RideTable.ride_id).filter_by(driver_username=username)
        apps = db_session.query(ApplicationTable).filter(ApplicationTable.ride_id.in_(rides.subquery()))
        apps.delete(synchronize_session=False)
        rides.delete()

        # Delete driver data
        db_session.query(DriverRatingTable).filter(
                (DriverRatingTable.rater == username) | (DriverRatingTable.ratee == username)).delete()
        db_session.query(DriverCertificationTable).filter_by(username=username).delete()
        db_session.query(DriverTable).filter_by(username=username).delete()

        # Delete user data
        db_session.query(UserRatingTable).filter(
                (UserRatingTable.rater == username) | (UserRatingTable.ratee == username)).delete()
        db_session.query(ApplicationTable).filter_by(username=username).delete()
        db_session.query(PayPalTable).filter_by(username=username).delete()
        db_session.query(CreditCardTable).filter_by(username=username).delete()
        db_session.query(PaymentMethodTable).filter_by(username=username).delete()

        # Delete user
        num_rows = db_session.query(UserTable).filter_by(username=username).delete()
        db_session.commit()
        if num_rows > 0:
            return {'status': 'success'}
        else:
            return {'error': 'User does not exist'}


@app.route('/api/user/<string:username>/verify', methods=['GET', 'POST'])
def UserVerify(username):
    if request.method == 'POST':
        # Check if the user has already applied
        exists = db_session.query(DriverCertificationTable).filter_by(username=username).first()
        if exists:
            return {'error': 'User has already applied'}

        # Save images
        rid = str(uuid4())
        driver_license_path = os.path.join(rid, 'license.jpg')
        registration_path = os.path.join(rid, 'registration.jpg')
        vehicle_image_path = os.path.join(rid, 'vehicle.jpg')
        identity_path = os.path.join(rid, 'identity.jpg')

        os.makedirs(os.path.join(DOCS_DIR, rid))
        save_image(request.form['driver_license'], os.path.join(DOCS_DIR, driver_license_path))
        save_image(request.form['registration'], os.path.join(DOCS_DIR, registration_path))
        save_image(request.form['vehicle_image'], os.path.join(DOCS_DIR, vehicle_image_path))
        save_image(request.form['identity'], os.path.join(DOCS_DIR, identity_path))

        # Add to database
        vehicle = request.form['vehicle']
        newApplication = DriverCertificationTable(username=username, license=driver_license_path,
                                                  registration=registration_path,
                                                  vehicle=vehicle, vehicle_image=vehicle_image_path,
                                                  identification_document=identity_path)
        db_session.add(newApplication)
        db_session.commit()
        return {'status': 'success'}, 200
    elif request.method == 'GET':
        try:
            applicationQuery = db_session.query(DriverCertificationTable).filter(
                DriverCertificationTable.username == username).one()
            driverApplicationDict = {'username': applicationQuery.username,
                                     'license': applicationQuery.license,
                                     'registration': applicationQuery.registration,
                                     'vehicle': applicationQuery.vehicle,
                                     'vehicle_image': applicationQuery.vehicle_image,
                                     'identity': applicationQuery.identification_document}
            return driverApplicationDict
        except NoResultFound:
            return {'error': 'User doesn\'t have an active driver certification application in the database.'}
        except Exception as e:
            return {'error': str(e)}


@app.route('/mod/api/verification_applications', methods=['GET'])
def VerificationApplicationList():
    if request.method == 'GET':
        try:
            # all pending applications
            driverQuery = db_session.query(DriverTable.username)
            applicationQuery = db_session.query(DriverCertificationTable).filter(
                ~DriverCertificationTable.username.in_(driverQuery)).join(
                UserTable, UserTable.username == DriverCertificationTable.username).all()
            driverApplicationDict = {'applications': [
                                    {'username': a.username,
                                     'license': a.license,
                                     'registration': a.registration,
                                     'vehicle': a.vehicle,
                                     'vehicle_image': a.vehicle_image,
                                     'identity': a.identification_document,
                                     'first_name': a.user.first_name,
                                     'surname': a.user.surname
                                     } for a in applicationQuery]}
            return driverApplicationDict
        except NoResultFound:
            return {'error': 'No pending driver certification applications in the database.', 'applications': []}
        except Exception as e:
            return {'error': str(e), 'applications': []}


@app.route('/api/user/<string:username>/payment_info', methods=['GET', 'POST'])
def UserPaymentInfo(username):
    if request.method == 'POST':
        # Check if user exists
        query = db_session.query(UserTable).filter_by(username=username).first()
        if not query:
            return {'error': 'User does not exist'}, 400

        # Get request data
        method = request.form['method']
        name = request.form['name']

        # Validate data
        if method != 'credit_card' and method != 'paypal':
            return {'error': 'Invalid payment method type'}, 400

        # Get new payment ID
        payment_id = db_session.query(
                func.max(PaymentMethodTable.payment_id)).filter_by(username=username).scalar()
        payment_id = payment_id + 1 if payment_id else 1

        # Insert PaymentMethod record
        baseData = PaymentMethodTable(payment_id=payment_id, username=username,
                                      name=name, is_primary=False)
        db_session.add(baseData)

        if method == 'credit_card':
            number = request.form['number']
            exp_date = request.form['exp_date']
            cvv = request.form['cvv']
            card_type = request.form['type']
            data = CreditCardTable(payment_id=payment_id, username=username, number=number,
                                   cvv=cvv, exp_date=exp_date, type=card_type)
        elif method == 'paypal':
            paypal_token = request.form['paypal_token']
            data = PayPalTable(payment_id=payment_id, username=username, paypal_token=paypal_token)

        db_session.add(data)
        db_session.commit()
        return {'status': 'success'}, 200
    elif request.method == 'GET':
        # get a list of users payment info
        # return json
        # if not session['username'] == username:
        #     return {'error': 'Access denied!'}
        try:
            creditCardQuery = db_session.query(
                CreditCardTable).join(
                PaymentMethodTable, (PaymentMethodTable.username == CreditCardTable.username) &
                                    (PaymentMethodTable.payment_id == CreditCardTable.payment_id)).filter(
                CreditCardTable.username == username).all()
            payPalQuery = db_session.query(
                PayPalTable).join(
                PaymentMethodTable, (PaymentMethodTable.username == PayPalTable.username) &
                                    (PaymentMethodTable.payment_id == PayPalTable.payment_id)).filter(
                PayPalTable.username == username).all()
            # return all data except from passwords
            paymentDict = {'credit_cards':
                               [{'name': cc.paymentmethod.name,
                                 'payment_id': cc.payment_id,
                                 'is_primary': cc.paymentmethod.is_primary,
                                 'number': cc.number,
                                 'cvv': cc.cvv,
                                 'exp_date': cc.exp_date,
                                 'type': cc.type
                                 } for cc in creditCardQuery],
                           'paypal_accounts':
                               [{'name': pp.paymentmethod.name,
                                 'payment_id': pp.payment_id,
                                 'is_primary': pp.paymentmethod.is_primary,
                                 'token': pp.paypal_token,
                                 } for pp in payPalQuery]
                           }
            return paymentDict
        except NoResultFound:
            return {'error': 'User has no payment info in the database',
                    'credit_cards': [], 'paypal_accounts': []}
        except Exception as e:
            return {'error': str(e)}


@app.route('/api/user/<string:username>/set_primary_pm', methods=['PUT'])
def SetPrimary(username):
    if request.method == 'PUT':
        # useful api for setting primary payment methods
        # autochanges every other to non primary
        if request.values:
            try:
                paymentmethods = db_session.query(PaymentMethodTable).filter(PaymentMethodTable.username == username).all()
                if int(request.values['payment_id']) in [int(pm.payment_id) for pm in paymentmethods]:
                    for pm in paymentmethods:
                        if pm.payment_id == int(request.values['payment_id']):
                            pm.is_primary = 1
                        else:
                            pm.is_primary = 0
                    db_session.commit()
                    return {'status': 'success'}, 200
            except Exception as e:
                return {'error': str(e)}
        else:
            return {'error': 'Invalid request, data missing'}


@app.route('/api/user/<string:username>/rides', methods=['GET'])
def UserRides(username):
    if request.method == 'GET':
        # get ride data for a preview list
        # return json
        try:
            userRideQuery = db_session.query(RideTable).filter(RideTable.driver_username == username).all()
            rideDict = {'rides':
                            [{'ride_id': r.ride_id,
                              'start_datetime': r.start_datetime,
                              'return_datetime': r.return_datetime,
                              'cost': r.cost,
                              'description': r.description,
                              'seats': r.seats,
                              'available_seats': r.available_seats,
                              'longitude': r.longitude,
                              'latitude': r.latitude,
                              'location_name': r.location_name,
                              'driver_username': r.driver_username,
                              'event_id': r.event_id
                              } for r in userRideQuery]
                        }
            return rideDict
        except NoResultFound:
            return {'error': 'No rides by user {} in the database'.format(username), 'rides': []}
        except Exception as e:
            return {'error': str(e)}


@app.route('/api/event', methods=['POST', 'GET'])
def EventAddList():
    if request.method == 'POST':
        # Get request data
        title = request.form['title'] if 'title' in request.form.keys() else ''
        event_type = request.form['type'] if 'type' in request.form.keys() and not request.form['type'] == 'Select Event Type' else None
        creator = request.form['creator'] if 'creator' in request.form.keys() else None
        longitude = request.form['longitude'] if 'longitude' in request.form.keys() and len(request.form['longitude']) > 0 else '-1000'
        latitude = request.form['latitude'] if 'latitude' in request.form.keys() and len(request.form['latitude']) > 0 else '-1000'
        location_name = request.form['location_name'] if 'location_name' in request.form.keys() else ''
        date = request.form['date']
        time = request.form['time']
        datetime = DT.datetime.combine(DT.datetime.strptime(date, '%Y-%m-%d').date(),
                                       DT.datetime.strptime(time, '%H:%M').time())

        # Validate data
        if not is_valid_geolocation(latitude, longitude):
            return {'error': 'invalid geolocation'}, 400
        if len(title) == 0 or len(date) == 0 or len(time) == 0 or len(location_name) == 0:
            return {'error': 'empty data'}, 400

        # Get new event ID
        event_id = db_session.query(func.max(EventTable.event_id)).scalar()
        event_id = event_id + 1 if event_id else 1

        # Insert event into database
        newEvent = EventTable(event_id=event_id, title=title, type=event_type,
                              status='pending', creator=creator, datetime=datetime,
                              latitude=latitude, longitude=longitude, location_name=location_name)
        db_session.add(newEvent)
        db_session.commit()
        return {'status': 'success'}, 200
    elif request.method == 'GET':
        # get list of future events
        # here maybe also use query params for search like type etc and general filters
        try:
            eventQuery = db_session.query(EventTable).join(
                FutureEventView, FutureEventView.columns.event_id == EventTable.event_id).all()
            eventDict = {'events': [
                {
                    'event_id': e.event_id,
                    'title': e.title,
                    'type': e.type,
                    'status': e.status,
                    'latitude': e.latitude,
                    'longitude': e.longitude,
                    'location_name': e.location_name,
                    'datetime': e.datetime,
                    'creator': e.creator
                } for e in eventQuery]
            }
            return eventDict
        except NoResultFound:
            return {'error': 'No future events exist in the database', 'events': []}
        except Exception as e:
            return {'error': str(e)}


@app.route('/api/event/search', methods=['GET'])
def EventSearchAPI():
    if request.method == 'GET':
        # perform search on events
        old_events = (request.args.get('old') == '1')
        search_tag = request.args.get('tag')
        sql_like_tag = "%{}%".format(search_tag)
        try:
            if not old_events:
                eventQuery = db_session.query(EventTable).join(
                    FutureEventView, FutureEventView.columns.event_id == EventTable.event_id).filter(
                    EventTable.title.like(sql_like_tag)).all()
            else:
                eventQuery = db_session.query(EventTable).filter(
                    EventTable.title.like(sql_like_tag)).all()
            eventDict = {'events': [
                {
                    'event_id': e.event_id,
                    'title': e.title,
                    'type': e.type,
                    'status': e.status,
                    'latitude': e.latitude,
                    'longitude': e.longitude,
                    'location_name': e.location_name,
                    'datetime': e.datetime,
                    'creator': e.creator
                } for e in eventQuery]
            }
            return eventDict
        except NoResultFound:
            return {'error': 'No events match the given tags', 'events': []}
        except Exception as e:
            return {'error': str(e)}


@app.route('/api/event/<int:event_id>', methods=['PUT', 'GET', 'DELETE'])
def Event(event_id):
    if request.method == 'PUT':
        # edit event data
        # add event to base
        return
    elif request.method == 'GET':
        # return an event's data
        try:
            eventQuery = db_session.query(EventTable).filter(EventTable.event_id == event_id).one()
            eventDict = {
                'event_id': eventQuery.event_id,
                'title': eventQuery.title,
                'type': eventQuery.type,
                'status': eventQuery.status,
                'latitude': eventQuery.latitude,
                'longitude': eventQuery.longitude,
                'location_name': eventQuery.location_name,
                'datetime': eventQuery.datetime,
                'creator': eventQuery.creator
            }
            return eventDict
        except NoResultFound:
            return {'error': "Event {} doesn't exist in the database".format(event_id)}
        except Exception as e:
            return {'error': str(e)}
    elif request.method == 'DELETE':
        # Delete event rides
        rides = db_session.query(RideTable.ride_id).filter_by(event_id=event_id)
        apps = db_session.query(ApplicationTable).filter(ApplicationTable.ride_id.in_(rides.subquery()))
        apps.delete(synchronize_session=False)
        rides.delete()

        # Delete event
        num_rows = db_session.query(EventTable).filter_by(event_id=event_id).delete()
        db_session.commit()
        if num_rows > 0:
            return {'status': 'success'}
        else:
            return {'error': 'Event does not exist'}


@app.route('/api/event/<int:event_id>/rides', methods=['GET'])
def EventRidesAPI(event_id):
    if request.method == 'GET':
        # get ride data for a preview list
        # return json
        full_rides = (request.args.get('full') == '1')
        try:
            if not full_rides:
                eventRideQuery = db_session.query(RideTable).filter(RideTable.event_id == event_id).all()
            else:
                eventRideQuery = db_session.query(RideTable).filter(RideTable.event_id == event_id).filter(
                    RideTable.available_seats > 0).all()
            # return all data except from event_id (redundant)
            rideDict = {'rides':
                               [{'ride_id': r.ride_id,
                                 'start_datetime': r.start_datetime,
                                 'return_datetime': r.return_datetime,
                                 'cost': r.cost,
                                 'description': r.description,
                                 'seats': r.seats,
                                 'available_seats': r.available_seats,
                                 'longitude': r.longitude,
                                 'latitude': r.latitude,
                                 'location_name': r.location_name,
                                 'driver_username': r.driver_username
                                 } for r in eventRideQuery]
                           }
            return rideDict
        except NoResultFound:
            return {'error': 'No rides for event {} in the database'.format(event_id), 'rides':[]}
        except Exception as e:
            return {'error': str(e)}


@app.route('/api/ride', methods=['GET', 'POST'])
def RideList():
    if request.method == 'GET':
        # get ride data for a preview list
        # return json
        try:
            rideQuery = db_session.query(RideTable).all()
            # return all data except from event_id (redundant)
            rideDict = {'rides':
                               [{'ride_id': r.ride_id,
                                 'start_datetime': r.start_datetime,
                                 'return_datetime': r.return_datetime,
                                 'cost': r.cost,
                                 'description': r.description,
                                 'seats': r.seats,
                                 'available_seats': r.available_seats,
                                 'longitude': r.longitude,
                                 'latitude': r.latitude,
                                 'location_name': r.location_name,
                                 'driver_username': r.driver_username
                                 } for r in rideQuery]
                           }
            return rideDict
        except NoResultFound:
            return {'error': 'No rides in the database', 'rides': []}
        except Exception as e:
            return {'error': str(e)}

    elif request.method == 'POST':
        required_data = ['event_id', 'start_date', 'start_time', 'driver_username',
                         'location_name', 'cost','description', 'seats']
        if not (all(field in request.form.keys() for field in required_data)
                and all(len(request.form[field]) > 0 for field in request.form.keys())):
            return {'error': 'missing data'}, 400

        # Get request data
        event_id = request.form['event_id']
        start_date = request.form['start_date']
        start_time = request.form['start_time']
        driver_username = request.form['driver_username']
        longitude = request.form['longitude'] if 'longitude' in request.form.keys() and len(
            request.form['longitude']) > 0 else '-1000'
        latitude = request.form['latitude'] if 'latitude' in request.form.keys() and len(
            request.form['latitude']) > 0 else '-1000'
        location_name = request.form['location_name'] if 'location_name' in request.form.keys() else ''
        cost = request.form['cost']
        description = request.form['description']
        seats = request.form['seats']
        available_seats = request.form['seats']
        return_date = request.form['return_date'] if 'return_date' in request.form.keys() else None
        return_time = request.form['return_time'] if 'return_time' in request.form.keys() else None

        start_datetime = DT.datetime.combine(DT.datetime.strptime(start_date, '%Y-%m-%d').date(),
                                       DT.datetime.strptime(start_time, '%H:%M').time())
        if return_date and return_time:
            return_datetime = DT.datetime.combine(DT.datetime.strptime(return_date, '%Y-%m-%d').date(),
                                                 DT.datetime.strptime(return_time, '%H:%M').time())
        else:
            return_datetime = None

        # Validate data
        if not is_valid_geolocation(latitude, longitude):
            return {'error': 'invalid geolocation'}, 400

        # Get new ride ID
        ride_id = db_session.query(func.max(RideTable.ride_id)).scalar()
        ride_id = ride_id + 1 if ride_id else 1

        # Insert event into database
        newRide = RideTable(ride_id=ride_id, event_id=event_id, start_datetime=start_datetime,
                            return_datetime=return_datetime, cost=cost, driver_username=driver_username,
                            latitude=latitude, longitude=longitude, location_name=location_name,
                            description=description, seats=seats, available_seats=available_seats)
        db_session.add(newRide)
        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/ride/<int:ride_id>', methods=['GET', 'DELETE'])
def Ride(ride_id):
    if request.method == 'GET':
        # return a ride's data
        try:
            rideQuery = db_session.query(RideTable).filter(RideTable.ride_id == ride_id).one()
            rideDict = {
                'ride_id': rideQuery.ride_id,
                'start_datetime': rideQuery.start_datetime,
                'return_datetime': rideQuery.return_datetime,
                'cost': rideQuery.cost,
                'description': rideQuery.description,
                'seats': rideQuery.seats,
                'available_seats': rideQuery.available_seats,
                'longitude': rideQuery.longitude,
                'latitude': rideQuery.latitude,
                'location_name': rideQuery.location_name,
                'driver_username': rideQuery.driver_username,
                'event_id': rideQuery.event_id
                }
            return rideDict
        except NoResultFound:
            return {'error': "Ride {} doesn't exist in the database".format(ride_id)}
        except Exception as e:
            return {'error': str(e)}
    elif request.method == 'DELETE':
        # Delete ride data
        db_session.query(ApplicationTable).filter_by(ride_id=ride_id).delete()

        # Delete ride
        num_rows = db_session.query(RideTable).filter_by(ride_id=ride_id).delete()
        db_session.commit()
        if num_rows > 0:
            return {'status': 'success'}
        else:
            return {'error': 'Ride does not exist'}


@app.route('/api/ride/<int:ride_id>/users', methods=['GET'])
def RideUsers(ride_id):
    if request.method == 'GET':
        # return a ride's list of users
        try:
            rideUsersQuery = db_session.query(ApplicationTable, UserTable, AvgUserRatingView).join(
                UserTable, UserTable.username == ApplicationTable.username, isouter=True).join(
                AvgUserRatingView, AvgUserRatingView.columns.ratee == ApplicationTable.username, isouter=True).filter(
                ApplicationTable.ride_id == ride_id, ApplicationTable.status == 'accepted').all()
            rideUsersDict = {'users': [{
                    'username': u.user.username,
                    'first_name': u.user.first_name,
                    'surname': u.user.surname,
                    'avg_user_rating': str(u.average_user_rating)[:3]
                } for u in rideUsersQuery]}
            return rideUsersDict
        except NoResultFound:
            return {'error': 'No users found', 'users': []}
        except Exception as e:
            return {'error': str(e)}


@app.route('/api/user/<string:username>/application', methods=['GET'])
def UserApplicationList(username):
    if request.method == 'GET':
        # get list of user applications
        try:
            userApplicationsQuery = db_session.query(ApplicationTable, RideTable, EventTable).join(
                RideTable, ApplicationTable.ride_id == RideTable.ride_id, isouter=True).join(
                EventTable, EventTable.event_id == RideTable.event_id, isouter=True).filter(
                ApplicationTable.username == username).all()
            userApplicationsDict = {'applications': [{
                    'username': a.application.username,
                    'ride_id': a.application.ride_id,
                    'status': a.application.status,
                    'ride_driver': a.ride.driver_username,
                    'event_id': a.event.event_id,
                    'event_title': a.event.title
                } for a in userApplicationsQuery]}
            return userApplicationsDict
        except NoResultFound:
            return {'error': "No applications for user {}".format(username), 'applications': []}
        except Exception as e:
            return {'error': str(e), 'applications': []}


@app.route('/api/ride/<int:ride_id>/application', methods=['GET', 'POST'])
def RideApplication(ride_id):
    if request.method == 'GET':
        # get list of ride applications
        try:
            rideApplicationsQuery = db_session.query(ApplicationTable).filter(
                ApplicationTable.ride_id == ride_id).all()
            rideApplicationsDict = {'applications': [{
                    'username': a.username,
                    'ride_id': a.ride_id,
                    'status': a.status,
                    'message': a.message
                } for a in rideApplicationsQuery]}
            return rideApplicationsDict
        except NoResultFound:
            return {'error': "No applications for ride {}".format(ride_id), 'applications': []}
        except Exception as e:
            return {'error': str(e), 'applications': []}

    elif request.method == 'POST':
        # Check if user exists
        username = request.form['username']
        query = db_session.query(UserTable).filter_by(username=username).first()
        if not query:
            return {'error': 'User does not exist'}, 400

        # Check if ride exists
        query = db_session.query(RideTable).filter_by(ride_id=ride_id).first()
        if not query:
            return {'error': 'Ride does not exist'}, 404
        event_id = query.event_id

        # Check if user is a driver and has created a ride for this event
        query = db_session.query(RideTable).filter_by(driver_username=username, event_id=event_id).first()
        if query:
            return {'error': 'You are a driver with a ride for this event.'}, 400

        # Check if user has already applied for this ride
        query = db_session.query(ApplicationTable).filter_by(
                ride_id=ride_id, username=username, status='pending').first()
        if query:
            return {'error': 'You have already applied for this ride.'}, 400

        # Check if user has already been accepted for this ride
        query = db_session.query(ApplicationTable).filter_by(
                ride_id=ride_id, username=username, status='accepted').first()
        if query:
            return {'error': 'You have already been accepted on board this ride.'}, 400

        # Check if user has already been accepted on a ride for this event
        query = db_session.query(ApplicationTable).join(
                RideTable, ApplicationTable.ride_id == RideTable.ride_id).filter(
                        ApplicationTable.username == username, ApplicationTable.status == 'accepted',
                        RideTable.event_id == event_id).first()
        if query:
            return {'error': 'You are a passenger on another ride for this event.'}, 400

        # Get request data
        message = request.form['message']

        # Insert event into database
        newApplication = ApplicationTable(ride_id=ride_id, username=username, message=message, status='pending')
        db_session.add(newApplication)
        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/ride/<int:ride_id>/application/<string:username>', methods=['PUT', 'DELETE', 'GET'])
def Application(ride_id, username):
    if request.method == 'GET':
        # Get application data
        try:
            query = db_session.query(ApplicationTable).filter_by(ride_id=ride_id, username=username).one()
            data = {
                'ride_id': query.ride_id,
                'username': query.username,
                'message': query.message,
                'status': query.status
            }
            return data
        except NoResultFound:
            return {'error': 'Application does not exist'}
        except Exception as e:
            return {'error': str(e)}
    elif request.method == 'PUT':
        # Update application data
        if request.form:
            app = db_session.query(ApplicationTable).filter_by(ride_id=ride_id, username=username).one()
            if 'message' in request.form:
                app.message = request.form['message']
            if 'status' in request.form:
                app.status = request.form['status']
            db_session.commit()
        return {'status': 'success'}
    elif request.method == 'DELETE':
        # Delete application
        num_rows = db_session.query(ApplicationTable).filter_by(ride_id=ride_id, username=username).delete()
        db_session.commit()
        if num_rows > 0:
            return {'status': 'success'}
        else:
            return {'error': 'Application does not exist'}


@app.route('/api/user/<string:username>/userrating', methods=['GET', 'POST'])
def UserRating(username):
    if request.method == 'GET':
        # get list of user ratings for user
        try:
            userRatingQuery = db_session.query(UserRatingTable).filter(UserRatingTable.ratee == username).all()
            userRatingDict = {'ratings': [{
                'rater': u.rater,
                'comment': u.comment,
                'stars': u.stars
            } for u in userRatingQuery]}
            return userRatingDict
        except NoResultFound:
            return {'error': 'No user ratings found', 'ratings': []}
        except Exception as e:
            return {'error': str(e)}
    elif request.method == 'POST':
        # post new user rating for user
        required_data = ['rater', 'ratee', 'stars', 'comment']
        if not (all(field in request.form.keys() for field in required_data)
                and all(len(request.form[field]) > 0 for field in request.form.keys())):
            return {'error': 'missing data'}, 400

        # Get request data
        rater = request.form['rater']
        ratee = request.form['ratee']
        stars = request.form['stars']
        comment = request.form['comment']

        # Validate data
        if not is_valid_rating(stars):
            return {'error': 'invalid star rating'}, 400
        # Insert event into database
        newUserRating = UserRatingTable(rater=rater, ratee=ratee, stars=stars, comment=comment)
        db_session.add(newUserRating)
        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/user/<string:username>/ride/<int:ride_id>/people_to_rate', methods=['GET'])
def PeopleToRate(username, ride_id):
    if request.method == 'GET':
        passengersQuery = db_session.query(ApplicationTable).filter(
            ApplicationTable.ride_id == ride_id, ApplicationTable.username != username,
            ApplicationTable.status == 'accepted').all()
        # GET passengers of ride except for myself
        passengers = [p.username for p in passengersQuery]
        alreadyRatedQuery = db_session.query(ApplicationTable).join(
            UserRatingTable, ApplicationTable.username == UserRatingTable.ratee, isouter=True).filter(
            ApplicationTable.ride_id == ride_id, UserRatingTable.rater == username).all()
        # GET people user has already rated
        alreadyRated = [p.username for p in alreadyRatedQuery]
        # GET passengers of this ride user can rate
        users_to_rate = [p for p in passengers if p not in alreadyRated]

        # GET if user can rate driver
        driverQuery = db_session.query(RideTable).join(
            DriverRatingTable, RideTable.driver_username == DriverRatingTable.ratee, isouter=True).filter(
            RideTable.ride_id == ride_id, DriverRatingTable.rater == username).count()
        if driverQuery > 0:
            driver_to_rate = None
        else:
            driver_to_rate = db_session.query(RideTable).filter(RideTable.ride_id == ride_id).one().driver_username
        return {'driver': driver_to_rate, 'users': users_to_rate}


@app.route('/api/user/<string:username>/driverrating', methods=['GET', 'POST'])
def DriverRating(username):
    if request.method == 'GET':
        # Check if user is a driver
        query = db_session.query(DriverTable).filter_by(username=username).first()
        if not query:
            return {'error': "User {} is not a driver".format(username)}

        # Get driver ratings
        try:
            driverRatingQuery = db_session.query(DriverRatingTable).filter_by(ratee=username).all()
            driverRatingDict = {'ratings': [{
                            'rater': u.rater,
                            'comment': u.comment,
                            'stars': u.stars
                            } for u in driverRatingQuery]}
            return driverRatingDict
        except NoResultFound:
            return {'error': 'No diver ratings found', 'ratings': []}
        except Exception as e:
            return {'error': str(e)}
    elif request.method == 'POST':
        # post new driver rating for user
        required_data = ['rater', 'ratee', 'stars', 'comment']
        if not (all(field in request.form.keys() for field in required_data)
                and all(len(request.form[field]) > 0 for field in request.form.keys())):
            return {'error': 'missing data'}, 400
        # Get request data
        rater = request.form['rater']
        ratee = request.form['ratee']
        stars = request.form['stars']
        comment = request.form['comment']

        # Validate data
        if not is_valid_rating(stars):
            return {'error': 'invalid star rating'}, 400
        # Insert event into database
        newDriverRating = DriverRatingTable(rater=rater, ratee=ratee, stars=stars, comment=comment)
        db_session.add(newDriverRating)
        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/driver', methods=['POST'])
def DriverAdd():
    if request.method == 'POST':
        # add driver data for user to table in base
        return


@app.route('/api/driver/<string:username>', methods=['PUT', 'GET', 'DELETE'])
def Driver(username):
    if request.method == 'PUT':
        # edit driver data
        # add driver to base
        return
    elif request.method == 'GET':
        # return a driver's data
        try:
            driverQuery = db_session.query(DriverTable).filter(DriverTable.username == username).one()
            driverDict = {'username': driverQuery.username,
                          'vehicle': driverQuery.vehicle,
                          'vehicle_image': driverQuery.vehicle_image}
            return driverDict
        except NoResultFound:
            return {'error': 'User with provided credentials does not exist in the drivers table'}
        except Exception as e:
            return {'error': str(e)}
    elif request.method == 'DELETE':
        # Delete driver rides
        rides = db_session.query(RideTable.ride_id).filter_by(driver_username=username)
        apps = db_session.query(ApplicationTable).filter(ApplicationTable.ride_id.in_(rides.subquery()))
        apps.delete(synchronize_session=False)
        rides.delete()

        # Delete driver data
        db_session.query(DriverRatingTable).filter(
                (DriverRatingTable.rater == username) | (DriverRatingTable.ratee == username)).delete()
        db_session.query(DriverCertificationTable).filter_by(username=username).delete()

        # Delete driver
        num_rows = db_session.query(DriverTable).filter_by(username=username).delete()
        db_session.commit()
        if num_rows > 0:
            return {'status': 'success'}
        else:
            return {'error': 'Driver does not exist'}


''' 
    Begin of Front End related routes
'''


@app.route('/', methods=['GET'])
def Index():
    if request.method == 'GET':
        if 'username' in session:
            return render_template("home.html", username=session['username'])
        else:
            return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        # Validate credentials and redirect accordingly
        username = request.form['username']
        password = request.form['password']

        # Request user info via API call
        response = requests.get(url_for('User', username=username, _external=True))
        user = response.json()

        # Authenticate user
        if ('error' not in user) and check_password_hash(user['password'], password):
            session['username'] = str(username)

            #add driver check in session
            response = requests.get(url_for('Driver', username=session['username'], _external=True))
            session['driver'] = 'error' not in response.json()
            # Load profile picture filename to session
            session['profile_picture'] = user['profile_picture']

            # Redirect to user profile route (yet to be implemented) and render profile page
            return render_template("home.html", username=username)
        else:
            # Render error page
            return render_template("systemMessage.html", messageTitle="Login Failed",
                                   message="The provided credentials don't match a user in our database")

    # Browser login page
    elif request.method == 'GET':
        if 'username' in session:
            return render_template("home.html", username=session['username'])
        else:
            return render_template("login.html")


@app.route('/logout', methods=['GET'])
def Logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('Index'))


@app.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method == 'GET':
        # Render registration page
        return render_template("register.html")
    elif request.method == 'POST':
        # Submitted info
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        surname = request.form['surname']

        # Encode profile picture
        profile_picture = None
        f = request.files['profile_picture']
        if f.filename != '':
            if not check_image_ext(f.filename):
                return render_template('systemMessage.html', messageTitle='Invalid image format',
                                       message='The profile picture must be a JPEG image.')
            profile_picture = b64encode(f.read()).decode('ascii')

        # Insert user into database by posting on /api/user
        requestData = {'username': username, 'password': password, 'first_name': first_name, 'surname': surname,
                       'profile_picture': profile_picture}
        response = requests.post(url_for('UserListAdd', _external=True), data=requestData).json()
        if 'error' not in response:
            return render_template('systemMessage.html', messageTitle='Success',
                                   message='Registration completed successfully!')
        else:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])


@app.route('/driverCertification', methods=['GET', 'POST'])
def DriverCertification():
    if request.method == 'GET':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Check if user is already a driver
        response = requests.get(url_for('Driver', username=session['username'], _external=True))
        if 'error' not in response.json():
            return render_template("systemMessage.html", messageTitle="Already a driver",
                                   message="You are already a driver and do not need to apply for certification.")

        # Check if user has already applied
        response = requests.get(url_for('UserVerify', username=session['username'], _external=True))
        if 'error' not in response.json():
            return render_template("systemMessage.html", messageTitle="Already applied",
                                   message="You have already applied to be a driver, please wait until we review your application.")

        # If none of the above hold, present the driver certification application form
        return render_template("driverCertification.html")

    elif request.method == 'POST':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        requestData = {'vehicle': request.form['vehicle']}

        # Read images
        fields = ['driver_license', 'registration', 'vehicle_image', 'identity']
        for field in fields:
            f = request.files[field]
            if not check_image_ext(f.filename):
                return render_template('systemMessage.html', messageTitle='Invalid image format',
                                       message='The required documents must be JPEG images.')
            requestData[field] = b64encode(f.read()).decode('ascii')

        # Pass request to the API endpoint
        response = requests.post(url_for('UserVerify', username=session['username'], _external=True),
                                 data=requestData).json()
        if 'error' not in response:
            return render_template('systemMessage.html', messageTitle='Application Submitted Successfully',
                                   message='Your application to be a driver has been submitted, please wait until we review your application.')
        else:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])


@app.route('/user/<string:username>', methods=['GET'])
def UserProfile(username):
    if request.method == 'GET':
        # Initialize empty driver variables
        driverFlag = False
        driverData = {}
        driverRatings = None

        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Check if user exists
        userData = requests.get(url_for('User', username=username, _external=True)).json()
        if 'error' in userData:
            return render_template('systemMessage.html', messageTitle='Error', message=userData['error'])

        # Get user ratings
        userRatings = requests.get(url_for('UserRating', username=username, _external=True)).json()
        if 'ratings' not in userRatings:
            return render_template('systemMessage.html', messageTitle='Error', message=userRatings['error'])

        # Check if user is a driver
        response = requests.get(url_for('Driver', username=username, _external=True))
        driverData = response.json()
        if 'error' not in driverData:
            driverFlag = True

            # Get driver ratings
            driverRatings = requests.get(url_for('DriverRating', username=username, _external=True)).json()
            if 'ratings' not in driverRatings:
                return render_template('systemMessage.html', messageTitle='Error', message=userRatings['error'])

        # Render the user profile
        return render_template("userProfile.html", userData=userData, driverFlag=driverFlag, driverData=driverData,
                               userRatings=userRatings, driverRatings=driverRatings)


@app.route('/user/<string:username>/edit', methods=['GET', 'POST'])
def EditUserProfile(username):
    if request.method == 'GET':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Check if the provided username belongs to the currently logged in user
        if session['username'] == username:
            # Get user data
            userData = requests.get(url_for('User', username=username, _external=True)).json()
            if 'error' in userData:
                return render_template('systemMessage.html', messageTitle='Error', message=userData['error'])

            # Check if user is a driver and get data
            driverData = requests.get(url_for('Driver', username=username, _external=True)).json()
            driverFlag = 'error' not in driverData

            return render_template("editUserProfile.html", userData=userData, driverFlag=driverFlag,
                                   driverData=driverData)
        else:
            return render_template("systemMessage.html", messageTitle="Edit user profile error",
                                   message="User does not exist or unauthorized edit was attempted.")

    elif request.method == 'POST':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Check if the provided username belongs to the currently logged in user
        if session['username'] == username:
            # Data to be PUT to /api/user/<username>
            updatedData = {}

            # Request user info via API call
            user = requests.get(url_for('User', username=username, _external=True)).json()
            if 'error' in user:
                return render_template('systemMessage.html', messageTitle='Error', message=user['error'])

            # If a new profile picture is added, update the existing one
            f = request.files['profile_picture']
            if f.filename != '':
                if not check_image_ext(f.filename):
                    return render_template('systemMessage.html', messageTitle='Invalid image format',
                                           message='The profile picture must be a JPEG image.')
                updatedData['profile_picture'] = b64encode(f.read()).decode('ascii')

            # If a new first name is sent, update the one in the database
            if (request.form['first_name'] != user['first_name']) and (request.form['first_name'] != ''):
                updatedData['first_name'] = request.form['first_name']

            # If a new surname is sent, update the one in the database
            if (request.form['surname'] != user['surname']) and (request.form['surname'] != ''):
                updatedData['surname'] = request.form['surname']

            if updatedData:
                # PUT the updated data to /api/user/<username>
                putResponse = requests.put(url_for('User', username=session['username'], _external=True),
                                           data=updatedData)

                # GET the updated resource
                userData = requests.get(url_for('User', username=session['username'], _external=True)).json()
                if 'error' not in userData:
                    # Load profile picture filename to session
                    session['profile_picture'] = userData['profile_picture']

            return redirect(url_for('UserProfile', username=session['username']))

        else:
            return render_template("systemMessage.html", messageTitle="Edit user profile error",
                                   message="User does not exist or unauthorized edit was attempted.")


@app.route('/paymentmethods', methods=['GET'])
def PaymentMethods():
    if request.method == 'GET':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Get payment methods
        username = session['username']
        response = requests.get(url_for('UserPaymentInfo', username=username, _external=True)).json()
        if 'credit_cards' not in response or 'paypal_accounts' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])

        creditCards = response['credit_cards']
        paypalAccounts = response['paypal_accounts']

        # Censor Credit Card Numbers
        for card in creditCards:
            card['number'] = 3 * '**** ' + card['number'][-4:]

        # Render page
        return render_template('paymentMethods.html', creditCards=creditCards, paypalAccounts=paypalAccounts)


@app.route('/user/set_primary_pm', methods=['POST'])
def UserSetPrimary():
    if request.method == 'POST':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # API call to set
        response = requests.put(url_for('SetPrimary', username=session['username'], _external=True),
                                params={'payment_id': request.form['payment_id']})
        if 'error' in response.json():
            return render_template("systemMessage.html", messageTitle="Error",
                                   message="An error occurred while setting the primary payment method.")

        return redirect(url_for('PaymentMethods'))


@app.route('/addpaymentmethod', methods=['GET', 'POST'])
def AddPaymentMethod():
    if request.method == 'GET':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        return render_template('addPaymentMethod.html')

    elif request.method == 'POST':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Get request data
        requestData = {
                'name': request.form['name'],
                'method': request.form['method']
        }

        method = requestData['method']
        if method == 'credit_card':
            requestData['number'] = request.form['number']
            requestData['cvv'] = request.form['cvv']
            requestData['type'] = request.form['type']
            requestData['exp_date'] = request.form['exp_date']
        elif method == 'paypal':
            requestData['paypal_token'] = request.form['paypal_token']

        # Pass request to the API endpoint
        response = requests.post(url_for('UserPaymentInfo', username=session['username'], _external=True),
                                 data=requestData).json()
        if 'error' not in response:
            return redirect(url_for('PaymentMethods'))
        else:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        return


@app.route('/events', methods=['GET', 'POST'])
def BrowseEvents():
    if request.method == 'GET':
        # Get future events and then their info via API call
        response = requests.get(url_for('EventAddList', _external=True)).json()
        if 'events' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        events = response['events']

        # Check if user is logged in and is a driver so he can create rides
        driverFlag = False
        userEventsWithRide = []
        if 'username' in session:
            driverCheck = requests.get(url_for('Driver', username=session['username'], _external=True))
            driverFlag = 'error' not in driverCheck.json()

            # Get user rides
            response = requests.get(url_for('UserRides', username=session['username'], _external=True)).json()
            if 'rides' not in response:
                return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
            userEventsWithRide = [r['event_id'] for r in response['rides']]

        # Render template
        return render_template("browseEvents.html", events=events, title="Browse Events", driverFlag=driverFlag, userEventsWithRide=userEventsWithRide)


@app.route('/events/new', methods=['GET', 'POST'])
def CreateEvent():
    if request.method == 'GET':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Render template
        return render_template("createEvent.html")
    elif request.method == 'POST':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))
        required_fields = ['title', 'location_name', 'latitude', 'longitude', 'date', 'time']
        missing_fields = not (all(field in request.form.keys() for field in required_fields)
                              and all(len(request.form[field]) > 0 for field in request.form.keys()))
        if missing_fields:
            return render_template("systemMessage.html", messageTitle="Missing Fields",
                                   message="Please fill all the required fields.")
        requestData = {field: request.form[field] for field in required_fields}
        requestData['type'] = request.form['type'] if 'type' in request.form.keys() else ''
        requestData['creator'] = session['username']
        response = requests.post(url_for('EventAddList', _external=True),
                                 data=requestData)
        return render_template('systemMessage.html', messageTitle='Event Submitted Successfully',
                               message='Your event has been submitted! Please wait for a mod to approve it.')


@app.route('/events/search', methods=['GET', 'POST'])
def SearchEvents():
    if request.method == 'GET':
        # Render template
        return redirect(url_for('BrowseEvents', _external=True))

    elif request.method == 'POST':
        searchQuery = request.form['searchQuery']
        oldEventsFlag = 1 if 'oldEvents' in request.form else 0

        # Query the database
        params = {'tag': searchQuery, 'old': oldEventsFlag}
        response = requests.get(url_for('EventSearchAPI', _external=True), params=params).json()
        if 'events' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        events = response['events']

        # Check if user is logged in and is a driver so he can create rides
        driverFlag = False
        userEventsWithRide = []
        if 'username' in session:
            driverCheck = requests.get(url_for('Driver', username=session['username'], _external=True))
            driverFlag = 'error' not in driverCheck.json()

            # Get user rides
            response = requests.get(url_for('UserRides', username=session['username'], _external=True)).json()
            if 'rides' not in response:
                return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
            userEventsWithRide = [r['event_id'] for r in response['rides']]

        # Render template
        return render_template("browseEvents.html", events=events, title="Search Results for {}".format(searchQuery), driverFlag=driverFlag, userEventsWithRide=userEventsWithRide)


@app.route('/data/profile/<filename>')
def ProfilePicture(filename):
    filename = secure_filename(filename)
    return send_from_directory(PROFILE_DIR, filename)


@app.route('/data/vehicle/<filename>')
def VehicleImage(filename):
    filename = secure_filename(filename)
    return send_from_directory(VEHICLE_DIR, filename)


@app.route('/events/<int:event_id>/rides', methods=['GET'])
def EventRides(event_id):
    if request.method == 'GET':
        # Get event rides
        response = requests.get(url_for('EventRidesAPI', event_id=event_id, _external=True)).json()
        if 'rides' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        rides = response['rides']

        # Get event data
        event = requests.get(url_for('Event', event_id=event_id, _external=True)).json()
        if 'error' in event:
            return render_template('systemMessage.html', messageTitle='Error', message=event['error'])

        # Check if user logged in and is a driver
        driverFlag = False
        createRideFlag = False
        if 'username' in session:
            driverCheck = requests.get(url_for('Driver', username=session['username'], _external=True))
            if 'error' not in driverCheck.json():
                driverFlag = True

                # Get user rides
                response = requests.get(url_for('UserRides', username=session['username'], _external=True)).json()
                if 'rides' not in response:
                    return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
                userEventsWithRide = [r['event_id'] for r in response['rides']]

                # Check if driver already has a ride for this event
                createRideFlag = event_id not in userEventsWithRide

        # Load driver data
        for ride in rides:
            driverInfo = requests.get(url_for('Driver', username=ride['driver_username'], _external=True)).json()
            if 'error' in driverInfo:
                return render_template('systemMessage.html', messageTitle='Error', message=driverInfo['error'])
            ride['vehicle_image'] = driverInfo['vehicle_image']

        # Render template
        return render_template("eventRides.html", title="{}".format(event['title']), event=event, rides=rides,
                               driverFlag=driverFlag, createRideFlag=createRideFlag)


@app.route('/events/<int:event_id>/createride', methods=['GET', 'POST'])
def CreateRide(event_id):
    if request.method == 'GET':
        # Check if user logged in, is a driver and already has a ride for the current event
        driverFlag = False
        if 'username' in session:
            driverCheck = requests.get(url_for('Driver', username=session['username'], _external=True))
            if 'error' not in driverCheck.json():
                driverFlag = True

                # Get user rides
                response = requests.get(url_for('UserRides', username=session['username'], _external=True)).json()
                if 'rides' not in response:
                    return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
                userEventsWithRide = [r['event_id'] for r in response['rides']]

                # Check if driver already has a ride for this event
                if event_id in userEventsWithRide:
                    return render_template("systemMessage.html", messageTitle="Ride already created",
                                           message="You have already created a ride for this event.")
            else:
                # Render error page
                return render_template("systemMessage.html", messageTitle="You are not a certified driver",
                                       message="To create rides you need to be a certified driver. Apply from the top right menu")
        else:
            # Render error page
            return redirect(url_for("Login", _external=True))

        # Get event details
        eventData = requests.get(url_for('Event', event_id=event_id, _external=True)).json()
        if 'error' in eventData:
            return render_template('systemMessage.html', messageTitle='Error', message=eventData['error'])

        return render_template("createRide.html", event=eventData)

    elif request.method == 'POST':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Check for missing fields
        required_fields = ['description', 'seats', 'cost', 'start_date', 'start_time', 'location_name', 'latitude', 'longitude']
        if ('return_date' in request.form) and ('return_time' in request.form):
            required_fields.append(['return_date', 'return_time'])
        missing_fields = not (all(field in request.form.keys() for field in required_fields)
                              and all(len(request.form[field]) > 0 for field in request.form.keys()))
        if missing_fields:
            return render_template("systemMessage.html", messageTitle="Missing Fields",
                                   message="Please fill all the required fields.")

        requestData = {field: request.form[field] for field in required_fields}
        requestData['driver_username'] = session['username']
        requestData['event_id'] = event_id
        response = requests.post(url_for('RideList', _external=True), data=requestData)
        if 'error' in response:
            return render_template('systemMessage.html', messageTitle='Error Submitting Ride',
                                   message='An error occured while submitting your ride, please try again later.')
        return render_template('systemMessage.html', messageTitle='Ride Submitted Successfully',
                               message='Your ride has been submitted! Make sure to check back soon to approve passenger applications.')


@app.route('/ride/<int:ride_id>', methods=['GET', 'POST'])
def RideView(ride_id):
    if request.method == 'GET':
        # Get ride info
        rideInfo = requests.get(url_for('Ride', ride_id=ride_id, _external=True)).json()
        if 'error' in rideInfo:
            return render_template('systemMessage.html', messageTitle='Error', message=rideInfo['error'])
        event_id = rideInfo['event_id']
        driver = rideInfo['driver_username']

        # Get users on ride info
        response = requests.get(url_for('RideUsers', ride_id=ride_id, _external=True)).json()
        if 'users' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        passengers = response['users']

        # Get event info
        eventInfo = requests.get(url_for('Event', event_id=event_id, _external=True)).json()
        if 'error' in eventInfo:
            return render_template('systemMessage.html', messageTitle='Error', message=eventInfo['error'])

        # Get driver info
        driverInfo = requests.get(url_for('Driver', username=driver, _external=True)).json()
        if 'error' in driverInfo:
            return render_template('systemMessage.html', messageTitle='Error', message=driverInfo['error'])

        # Check if user logged in, is a driver and already has a ride for the current event
        driverFlag = False
        driverWithRideFlag = False
        alreadyAppliedFlag = False
        alreadyAcceptedFlag = False
        passengerInOtherRideFlag = False
        if 'username' in session:
            # Check if user is a driver
            username = session['username']
            driverCheck = requests.get(url_for('Driver', username=username, _external=True))
            if 'error' not in driverCheck.json():
                driverFlag = True

                # Get user rides
                response = requests.get(url_for('UserRides', username=username, _external=True)).json()
                if 'rides' not in response:
                    return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
                userEventsWithRide = [r['event_id'] for r in response['rides']]

                # Check if driver already has a ride for this event
                if event_id in userEventsWithRide:
                    driverWithRideFlag = True

            # Get user applications
            response = requests.get(url_for('UserApplicationList', username=username, _external=True)).json()
            if 'applications' not in response:
                return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
            userApplications = response['applications']
            userRidesAsPassenger = [a['ride_id'] for a in userApplications if a['status'] == 'accepted']

            # Get event rides
            response = requests.get(url_for('EventRidesAPI', event_id=event_id, _external=True)).json()
            if 'rides' not in response:
                return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
            eventRides = [e['ride_id'] for e in response['rides']]

            alreadyAcceptedFlag = ride_id in userRidesAsPassenger
            alreadyAppliedFlag = ride_id in [a['ride_id'] for a in userApplications if a['status'] == 'pending']
            passengerInOtherRideFlag = any(ride in userRidesAsPassenger for ride in eventRides)

        return render_template("rideView.html", rideInfo=rideInfo, passengers=passengers, eventInfo=eventInfo,
                               driverInfo=driverInfo, driverWithRideFlag=driverWithRideFlag,
                               alreadyAcceptedFlag=alreadyAcceptedFlag, alreadyAppliedFlag=alreadyAppliedFlag,
                               passengerInOtherRideFlag=passengerInOtherRideFlag)

    elif request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('Login'))

        # POST to RideApplication
        postData = {
            'username': session['username'],
            'message': request.form['message']
        }
        response = requests.post(url_for('RideApplication', ride_id=ride_id, _external=True), data=postData).json()
        if 'error' not in response:
            return render_template('systemMessage.html', messageTitle='Application Submitted Successfully',
                                   message='The driver will soon look into your application.')
        else:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])


@app.route('/rate_rides', methods=['GET', 'POST'])
def RateRides():
    if request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('Login'))

        username = session['username']

        # Get user applications
        response = requests.get(url_for('UserApplicationList', username=username, _external=True)).json()
        if 'applications' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        my_rides = [a['ride_id'] for a in response['applications'] if a['status'] == 'accepted']

        # Get past rides
        response = requests.get(url_for('RideList', username=username, _external=True)).json()
        if 'rides' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        past_rides = [r['ride_id'] for r in response['rides'] if is_past_date(r['start_datetime'][:16])]

        # converting a large list to a set speeds up the program tremendously
        my_past_rides = [ride for ride in my_rides if ride in set(past_rides)]
        to_rate_by_ride = []
        for r in my_past_rides:
            rate_data = requests.get(url_for('PeopleToRate', username=username, ride_id=r, _external=True)).json()

            # Get ride info
            rideInfo = requests.get(url_for('Ride', ride_id=r, _external=True)).json()
            if 'error' in rideInfo:
                continue
            rate_data['event_id'] = rideInfo['event_id']

            # Get event info
            eventInfo = requests.get(url_for('Event', event_id=rate_data['event_id'], _external=True)).json()
            if 'error' in eventInfo:
                continue
            rate_data['event_title'] = eventInfo['title']

            to_rate_by_ride.append(rate_data)

        # TODO: Here render_template and provide to_rate_by_ride as context
        return render_template('ratePastRides.html', ride_rating_data=to_rate_by_ride)
    if request.method == 'POST':
        # Create POST
        return


@app.route('/my_rides', methods=['GET', 'POST'])
def ManageMyRides():
    if request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('Login'))

        username = session['username']
        response = requests.get(url_for('UserRides', username=username, _external=True))
        rides = response.json()['rides']
        not_expired_rides = [r for r in rides if not is_past_date(r['start_datetime'][:16])]
        rides = []
        users = {}
        for r in not_expired_rides:
            ride = r
            ride['event_title'] = requests.get(url_for('Event', event_id=r['event_id'], _external=True)).json()['title']
            ride['applications'] = requests.get(url_for('RideApplication', ride_id=r['ride_id'], _external=True)).json()['applications']
            for application in ride['applications']:
                users[application['username']] = requests.get(url_for("User", username=application['username'], _external=True)).json()
            rides.append(r)
        return render_template('manageRides.html', rides=rides, users=users)

    elif request.method == 'POST':

        # TODO: Add extra validation (can this driver do this, seat limitations etc) to POST requests possibly in the API route
        # POST to RideApplication endpoint according to response (Accept/Reject)
        putData = {
            "status": request.form['status']
        }
        response = requests.put(url_for("Application", ride_id=request.form['ride_id'],
                                        username=request.form['username'], _external=True), data=putData)
        if 'error' in response.json():
            # Render error page
            return render_template("systemMessage.html", messageTitle="An error occurred",
                                   message="An error occurred while processing application. Please try again later.")

        return redirect(url_for('ManageMyRides'))


@app.route('/my_applications', methods=['GET'])
def MyRideApplications():
    if 'username' not in session:
        return redirect(url_for('Login'))

    username = session['username']

    # Get applications
    response = requests.get(url_for('UserApplicationList', username=username, _external=True))
    applications = response.json()['applications']

    # Form events -> ride-application structure
    events = {application['event_id']:
                  {
                      'title': application['event_title'],
                      'applications': []
                   } for application in applications}

    # Get driver profile pictures and names
    driverPictures = {
        application['ride_driver']: {}
        for application in applications
    }
    for application in applications:
        response = requests.get(url_for("User", username=application['ride_driver'], _external=True)).json()
        driverPictures[application['ride_driver']]['profile_picture'] = response['profile_picture']
        driverPictures[application['ride_driver']]['first_name'] = response['first_name']
        driverPictures[application['ride_driver']]['surname'] = response['surname']

    # Complete events -> ride-application structure
    for application in applications:
        events[application['event_id']]['applications'].append({
            'ride_id': application['ride_id'],
            'status': application['status'],
            'ride_driver': application['ride_driver'],
            'driver_picture': driverPictures[application['ride_driver']]['profile_picture'],
            'driver_first_name': driverPictures[application['ride_driver']]['first_name'],
            'driver_surname': driverPictures[application['ride_driver']]['surname']
        })

    return render_template('myRideApplications.html', events=events)


@app.route('/mod/events_to_approve', methods=['GET'])
def ModEventsToApprove():
    events = requests.get(url_for('EventAddList', _external=True)).json()['events']
    events_to_approve = [event for event in events if event['status'] == 'pending']
    return render_template('modApproveEvents.html', title='Approve Events', events=events_to_approve)


@app.route('/mod/drivers_to_approve', methods=['GET'])
def ModDriversToApprove():
    applications = requests.get(url_for('VerificationApplicationList', _external=True)).json()['applications']
    return render_template('modApproveDrivers.html', title='Approve Drivers', applications=applications)
