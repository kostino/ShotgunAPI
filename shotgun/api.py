from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from flask import Flask, render_template, request, session, send_from_directory, url_for, redirect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from base64 import b64encode
import requests
from uuid import uuid4

from utils import *

from config import ShotgunConfig

CONFIG_DIR = './config.ini'
config = ShotgunConfig(CONFIG_DIR)

DATA_ROOT = config.data_root
PROFILE_DIR = os.path.join(DATA_ROOT, 'profile')
VEHICLE_DIR = os.path.join(DATA_ROOT, 'vehicle')
DOCS_DIR = os.path.join(DATA_ROOT, 'docs')
EVENT_PICS_DIR = os.path.join(DATA_ROOT, config.event_pics_dir)


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
if not os.path.exists(EVENT_PICS_DIR):
    os.makedirs(EVENT_PICS_DIR)


@app.route('/api/user', methods=['POST', 'GET'])
def UserListAdd():
    db_session = Session(engine)
    if request.method == 'POST':
        # Get request data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        surname = request.form['surname']
        profile_picture_data = request.form.get('profile_picture')

        # Validate data
        if not is_valid_username(username):
            return {'error': 'A username must be between 3 and 16 characters. Letters, numbers, underscores and dashes only.'}
        if not is_valid_password(password):
            return {'error': 'A password must be at least 6 characters long.'}

        # Generate profile picture filename
        if profile_picture_data:
            profile_picture = '{}.jpg'.format(uuid4())
        else:
            profile_picture = 'default.jpg'

        # Create instance
        pwd_hash = generate_password_hash(password)
        newUser = UserTable(username=username, password=pwd_hash, email=email, first_name=first_name,
                            surname=surname, profile_picture=profile_picture)
        try:
            # Try to insert into database
            with db_session.begin_nested():
                db_session.add(newUser)
                db_session.flush()
        except IntegrityError:
            return {'error': 'Username or email already used.'}

        # Save profile picture
        if profile_picture_data:
            save_image(profile_picture_data, os.path.join(PROFILE_DIR, profile_picture))

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
                'avg_user_rating': str(u.average_user_rating)[:3] if u.average_user_rating else None,
                'avg_driver_rating': str(u.average_driver_rating)[:3] if u.average_driver_rating else None
            } for u in userQuery]}
            return userDict
        except NoResultFound:
            return {'error': 'No users exist in the database'}
        except Exception as e:
            return {'error': str(e)}


@app.route('/api/user/<string:username>', methods=['PUT', 'GET', 'DELETE'])
def User(username):
    db_session = Session(engine)
    if request.method == 'PUT':
        user = db_session.query(UserTable).filter_by(username=username).first()
        if not user:
            return {'error': 'User does not exist'}, 404

        # Update user data
        if request.form:
            if 'first_name' in request.form:
                user.first_name = request.form['first_name']
            if 'surname' in request.form:
                user.surname = request.form['surname']
            if 'profile_picture' in request.form:
                user.profile_picture = '{}.jpg'.format(uuid4())
                save_image(request.form['profile_picture'], os.path.join(PROFILE_DIR, user.profile_picture))
            db_session.commit()
        return {'status': 'success'}, 200
    elif request.method == 'GET':
        # return a user data
        # Maybe do a /api/sth for data as json and a /sth for frontend
        # Maybe /api/user/<user_id> returns json user data and /user loads a user profile and calls
        # multiple api endpoints like /api/rating/ or /api/driver/
        try:
            query = db_session.query(UserTable, AvgDriverRatingView, AvgUserRatingView).join(
                AvgDriverRatingView, AvgDriverRatingView.columns.ratee == UserTable.username, isouter=True).join(
                AvgUserRatingView, AvgUserRatingView.columns.ratee == UserTable.username, isouter=True).filter(
                UserTable.username == username).one()
            # return all data except from passwords
            userDict = {'username': query.user.username,
                        'password': query.user.password,
                        'first_name': query.user.first_name,
                        'surname': query.user.surname,
                        'profile_picture': query.user.profile_picture,
                        'avg_user_rating': str(query.average_user_rating)[:3] if query.average_user_rating else None,
                        'avg_driver_rating': str(query.average_driver_rating)[:3] if query.average_driver_rating else None}
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


@app.route('/api/user/<string:username>/verify', methods=['GET', 'POST', 'DELETE'])
def UserVerify(username):
    db_session = Session(engine)
    if request.method == 'POST':
        # Generate image filenames
        rid = str(uuid4())
        driver_license_path = os.path.join(rid, 'license.jpg')
        registration_path = os.path.join(rid, 'registration.jpg')
        vehicle_image_path = os.path.join(rid, 'vehicle.jpg')
        identity_path = os.path.join(rid, 'identity.jpg')

        # Create instance
        vehicle = request.form['vehicle']
        newApplication = DriverCertificationTable(username=username, license=driver_license_path,
                                                  registration=registration_path,
                                                  vehicle=vehicle, vehicle_image=vehicle_image_path,
                                                  identification_document=identity_path)
        try:
            # Try to insert into database
            with db_session.begin_nested():
                db_session.add(newApplication)
                db_session.flush()
        except IntegrityError:
            return {'error': 'User has already applied'}

        # Save documents
        os.makedirs(os.path.join(DOCS_DIR, rid))
        save_image(request.form['driver_license'], os.path.join(DOCS_DIR, driver_license_path))
        save_image(request.form['registration'], os.path.join(DOCS_DIR, registration_path))
        save_image(request.form['vehicle_image'], os.path.join(DOCS_DIR, vehicle_image_path))
        save_image(request.form['identity'], os.path.join(DOCS_DIR, identity_path))

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
    elif request.method == 'DELETE':
        # Delete application
        num_rows = db_session.query(DriverCertificationTable).filter_by(username=username).delete()
        db_session.commit()
        if num_rows > 0:
            return {'status': 'success'}
        else:
            return {'error': 'Driver certification application does not exist'}


@app.route('/api/verification_applications', methods=['GET'])
def VerificationApplicationList():
    db_session = Session(engine)
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
def PaymentInfoList(username):
    db_session = Session(engine)
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

        # Create instance
        baseData = PaymentMethodTable(username=username, name=name, is_primary=False)

        while True:
            try:
                # Get new payment ID
                payment_id = db_session.query(
                        func.max(PaymentMethodTable.payment_id)).filter_by(username=username).scalar()
                payment_id = payment_id + 1 if payment_id else 1
                baseData.payment_id = payment_id

                # Try to insert into database
                with db_session.begin_nested():
                    db_session.add(baseData)
                    db_session.flush()
                    break
            except IntegrityError:
                # Retry
                pass

        # Insert payment method data
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


@app.route('/api/user/<string:username>/payment_info/<int:payment_id>', methods=['GET', 'DELETE'])
def PaymentInfo(username, payment_id):
    db_session = Session(engine)
    if request.method == 'GET':
        # Get base info
        query = db_session.query(PaymentMethodTable).filter_by(username=username, payment_id=payment_id).first()
        if not query:
            return {'error': 'Payment method does not exist'}

        data = {
            'username': query.username,
            'payment_id': query.payment_id,
            'name': query.name,
            'is_primary': query.is_primary
        }

        # Get credit card info
        query = db_session.query(CreditCardTable).filter_by(username=username, payment_id=payment_id).first()
        if query:
            data['number'] = query.number
            data['cvv'] = query.cvv
            data['exp_date'] = query.exp_date
            data['type'] = query.type

        # Get PayPal info
        query = db_session.query(PayPalTable).filter_by(username=username, payment_id=payment_id).first()
        if query:
            data['paypal_token'] = query.paypal_token

        return data

    elif request.method == 'DELETE':
        # Delete payment info
        db_session.query(CreditCardTable).filter_by(username=username, payment_id=payment_id).delete()
        db_session.query(PayPalTable).filter_by(username=username, payment_id=payment_id).delete()
        num_rows = db_session.query(PaymentMethodTable).filter_by(username=username, payment_id=payment_id).delete()
        db_session.commit()
        if num_rows > 0:
            return {'status': 'success'}
        else:
            return {'error': 'Payment method does not exist'}


@app.route('/api/user/<string:username>/set_primary_pm', methods=['PUT'])
def SetPrimary(username):
    db_session = Session(engine)
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
    db_session = Session(engine)
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
    db_session = Session(engine)
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
            return {'error': 'Invalid geolocation'}, 400
        if len(title) == 0 or len(date) == 0 or len(time) == 0 or len(location_name) == 0:
            return {'error': 'Empty data'}, 400

        # Create instance
        newEvent = EventTable(title=title, type=event_type, status='pending', creator=creator,
                datetime=datetime, latitude=latitude, longitude=longitude, location_name=location_name)

        while True:
            try:
                # Get new event ID
                event_id = db_session.query(func.max(EventTable.event_id)).scalar()
                newEvent.event_id = event_id + 1 if event_id else 1

                # Try to insert into database
                with db_session.begin_nested():
                    db_session.add(newEvent)
                    db_session.flush()
                    break
            except IntegrityError:
                # Retry
                pass

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
    db_session = Session(engine)
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
    db_session = Session(engine)
    if request.method == 'PUT':
        event = db_session.query(EventTable).filter_by(event_id=event_id).first()
        if not event:
            return {'error': 'Event does not exist'}, 404

        # Update event data
        if request.form:
            if 'title' in request.form:
                event.title = request.form['title']
            if 'type' in request.form:
                event.type = request.form['type']
            if 'status' in request.form:
                event.status = request.form['status']
            if 'latitude' in request.form:
                event.latitude = request.form['latitude']
            if 'longitude' in request.form:
                event.longitude = request.form['longitude']
            if 'location_name' in request.form:
                event.location_name = request.form['location_name']
            if 'datetime' in request.form:
                event.datetime = request.form['datetime']
            db_session.commit()
        return {'status': 'success'}, 200
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
    db_session = Session(engine)
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
    db_session = Session(engine)
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
            return {'error': 'Missing data'}, 400

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
            return {'error': 'Invalid geolocation'}, 400

        # Insert event into database
        newRide = RideTable(event_id=event_id, start_datetime=start_datetime,
                            return_datetime=return_datetime, cost=cost, driver_username=driver_username,
                            latitude=latitude, longitude=longitude, location_name=location_name,
                            description=description, seats=seats, available_seats=available_seats)

        while True:
            try:
                # Get new ride ID
                ride_id = db_session.query(func.max(RideTable.ride_id)).scalar()
                newRide.ride_id = ride_id + 1 if ride_id else 1

                # Try to insert into database
                with db_session.begin_nested():
                    db_session.add(newRide)
                    db_session.flush()
                    break
            except IntegrityError:
                # Retry
                pass

        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/ride/<int:ride_id>', methods=['GET', 'DELETE'])
def Ride(ride_id):
    db_session = Session(engine)
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
    db_session = Session(engine)
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
                    'avg_user_rating': str(u.average_user_rating)[:3] if u.average_user_rating else None
                } for u in rideUsersQuery]}
            return rideUsersDict
        except NoResultFound:
            return {'error': 'No users found', 'users': []}
        except Exception as e:
            return {'error': str(e)}


@app.route('/api/user/<string:username>/application', methods=['GET'])
def UserApplicationList(username):
    db_session = Session(engine)
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
    db_session = Session(engine)
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

        # Create instance
        newApplication = ApplicationTable(ride_id=ride_id, username=username, message=message, status='pending')
        try:
            # Try to insert into database
            with db_session.begin_nested():
                db_session.add(newApplication)
                db_session.flush()
        except IntegrityError:
            return {'error': 'You have already applied for this ride.'}, 400

        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/ride/<int:ride_id>/application/<string:username>', methods=['PUT', 'DELETE', 'GET'])
def Application(ride_id, username):
    db_session = Session(engine)
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
        application = db_session.query(ApplicationTable).filter_by(ride_id=ride_id, username=username).first()
        if not application:
            return {'error': 'Application does not exist'}, 404

        # Update application data
        if request.form:
            if 'message' in request.form:
                application.message = request.form['message']
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


@app.route('/api/ride/<int:ride_id>/application/<string:username>/accept', methods=['POST'])
def ApplicationAccept(ride_id, username):
    db_session = Session(engine)
    if request.method == 'POST':
        application = db_session.query(ApplicationTable).filter_by(ride_id=ride_id, username=username).first()
        if not application:
            return {'error': 'Application does not exist'}, 404
        if application.status != 'pending':
            return {'error': 'Application is not pending'}, 400

        # Get ride data
        ride = db_session.query(RideTable).filter_by(ride_id=ride_id).first()
        if not ride:
            return {'error': 'Ride does not exist'}, 404

        # Update ride data
        if ride.available_seats > 0:
            ride.available_seats = ride.available_seats - 1
            if ride.available_seats == 0:
                # Ride full, reject remaining applications
                query = db_session.query(ApplicationTable).filter_by(ride_id=ride_id, status='pending').all()
                for a in query:
                    a.status = 'rejected'
        else:
            return {'error': 'Ride is full'}, 400

        # Reject the pending applications to rides of the same event
        query = db_session.query(ApplicationTable).join(
                RideTable, ApplicationTable.ride_id == RideTable.ride_id).filter(
                        RideTable.event_id == ride.event_id, RideTable.ride_id != ride_id,
                        ApplicationTable.status == 'pending', ApplicationTable.username == username).all()
        for a in query:
            a.status = 'rejected'

        # Accept application
        application.status = 'accepted'
        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/ride/<int:ride_id>/application/<string:username>/reject', methods=['POST'])
def ApplicationReject(ride_id, username):
    db_session = Session(engine)
    if request.method == 'POST':
        application = db_session.query(ApplicationTable).filter_by(ride_id=ride_id, username=username).first()
        if not application:
            return {'error': 'Application does not exist'}, 404
        if application.status != 'pending':
            return {'error': 'Application is not pending'}, 400

        # Reject application
        application.status = 'rejected'
        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/user/<string:username>/userrating', methods=['GET', 'POST'])
def UserRating(username):
    db_session = Session(engine)
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
            return {'error': 'Missing data'}, 400

        # Get request data
        rater = request.form['rater']
        ratee = request.form['ratee']
        stars = request.form['stars']
        comment = request.form['comment']

        # Validate data
        if not is_valid_rating(stars):
            return {'error': 'Invalid star rating'}, 400

        # Create instance
        newUserRating = UserRatingTable(rater=rater, ratee=ratee, stars=stars, comment=comment)

        try:
            # Try to insert into database
            with db_session.begin_nested():
                db_session.add(newUserRating)
                db_session.flush()
        except IntegrityError:
            return {'error': 'User rating already exists.'}, 400

        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/user/<string:username>/ride/<int:ride_id>/people_to_rate', methods=['GET'])
def PeopleToRate(username, ride_id):
    db_session = Session(engine)
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

        if driverQuery != 0:
            driver_to_rate = False
        else:
            driver_to_rate = True
        return {'driver_flag': driver_to_rate, 'users': users_to_rate}


@app.route('/api/user/<string:username>/driverrating', methods=['GET', 'POST'])
def DriverRating(username):
    db_session = Session(engine)
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
            return {'error': 'Missing data'}, 400

        # Get request data
        rater = request.form['rater']
        ratee = request.form['ratee']
        stars = request.form['stars']
        comment = request.form['comment']

        # Validate data
        if not is_valid_rating(stars):
            return {'error': 'Invalid star rating'}, 400

        # Insert event into database
        newDriverRating = DriverRatingTable(rater=rater, ratee=ratee, stars=stars, comment=comment)

        try:
            # Try to insert into database
            with db_session.begin_nested():
                db_session.add(newDriverRating)
                db_session.flush()
        except IntegrityError:
            return {'error': 'Driver rating already exists.'}, 400

        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/driver', methods=['POST'])
def DriverAdd():
    db_session = Session(engine)
    if request.method == 'POST':
        # Get request data
        username = request.form['username']
        vehicle = request.form['vehicle']
        vehicle_image_data = request.form['vehicle_image']

        # Check if user exists
        query = db_session.query(UserTable).filter_by(username=username).first()
        if not query:
            return {'error': 'User does not exist'}, 400

        # Generate vehicle image filename
        vehicle_image = '{}.jpg'.format(uuid4())

        # Insert driver data into database
        data = DriverTable(username=username, vehicle=vehicle, vehicle_image=vehicle_image)
        try:
            # Try to insert into database
            with db_session.begin_nested():
                db_session.add(data)
                db_session.flush()
        except IntegrityError:
            return {'error': 'User is already a driver'}, 400

        # Save vehicle image
        save_image(vehicle_image_data, os.path.join(VEHICLE_DIR, vehicle_image))

        db_session.commit()
        return {'status': 'success'}, 200


@app.route('/api/driver/<string:username>', methods=['PUT', 'GET', 'DELETE'])
def Driver(username):
    db_session = Session(engine)
    if request.method == 'PUT':
        driver = db_session.query(DriverTable).filter_by(username=username).first()
        if not driver:
            return {'error': 'Driver does not exist'}, 404

        # Update driver data
        if request.form:
            if 'vehicle' in request.form:
                driver.vehicle = request.form['vehicle']
            if 'vehicle_image' in request.form:
                driver.vehicle_image = '{}.jpg'.format(uuid4())
                save_image(request.form['vehicle_image'], os.path.join(VEHICLE_DIR, driver.vehicle_image))
            db_session.commit()
        return {'status': 'success'}, 200
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