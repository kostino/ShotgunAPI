from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from flask import Flask, render_template, request, session, url_for, redirect, json, jsonify

import requests

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
FutureEventView = Table("future_events", metadata, autoload=True, autoload_with=engine)

# Start
db_session = Session(engine)
app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5rt2L"F4xFz\n\xec]/'


@app.route('/api/user', methods=['POST', 'GET'])
def UserListAdd():
    if request.method == 'POST':
        # get user data from request.json
        # add user to base
        # Insert user into database
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        surname = request.form['surname']
        profile_picture = request.form['profile_picture']

        newUser = UserTable(username=username, password=password,
                            first_name=first_name, surname=surname, profile_picture=profile_picture)
        db_session.add(newUser)
        db_session.commit()
        return {'status': 'success'}, 200
    elif request.method == 'GET':
        # return a user list, maybe a json. This endpoint probably handles like an api
        # Maybe do a /api/sth for endpoints not returning html
        return


@app.route('/api/user/<string:username>', methods=['PUT', 'GET', 'DELETE'])
def User(username):
    if request.method == 'PUT':
        # edit user data
        # add user to base
        return
    elif request.method == 'GET':
        # return a user data
        # Maybe do a /api/sth for data as json and a /sth for frontend
        # Maybe /api/user/<user_id> returns json user data and /user loads a user profile and calls
        # multiple api endpoints like /api/rating/ or /api/driver/
        try:
            userQuery = db_session.query(UserTable).filter(UserTable.username == username).one()
            userDict = {'username': userQuery.username,
                        'password': userQuery.password,
                        'first_name': userQuery.first_name,
                        'surname': userQuery.surname,
                        'profile_picture': userQuery.profile_picture}
            return userDict
        except NoResultFound:
            return {'error': 'User with provided credentials does not exist in the database'}
        except Exception as e:
            return {'error': str(e)}

    elif request.method == 'DELETE':
        # return a user data
        # Maybe do a /api/sth for data as json and a /sth for frontend
        # Maybe /api/user/<user_id> returns json user data and /user loads a user profile and calls
        # multiple api endpoints like /api/rating/ or /api/driver/
        return


@app.route('/api/user/<string:username>/verify', methods=['GET', 'POST'])
def UserVerify(username):
    if request.method == 'POST':
        # get verification application data from request
        # add to database
        driver_license = request.form['license']
        registration = request.form['registration']
        vehicle = request.form['vehicle']
        vehicle_image = request.form['vehicle_image']
        identification_document = request.form['identification_document']

        newApplication = DriverCertificationTable(username=username, license=driver_license, registration=registration,
                                                  vehicle=vehicle, vehicle_image=vehicle_image,
                                                  identification_document=identification_document)
        db_session.add(newApplication)
        db_session.commit()
        return {'status': 'success'}, 200
    elif request.method == 'GET':
        try:
            applicationQuery = db_session.query(DriverCertificationTable).filter(DriverCertificationTable.username == username).one()
            driverApplicationDict = {'username': applicationQuery.username,
                        'license': applicationQuery.license,
                        'registration': applicationQuery.registration,
                        'vehicle': applicationQuery.vehicle,
                        'vehicle_image': applicationQuery.vehicle_image,
                        'identification_document': applicationQuery.identification_document}
            return driverApplicationDict
        except NoResultFound:
            return {'error': 'User doesn\'t have an active driver certification application in the database.'}
        except Exception as e:
            return {'error': str(e)}


@app.route('/api/user/<string:username>/payment_info', methods=['GET', 'POST', 'PUT'])
def UserPaymentInfo(username):
    if request.method == 'POST':
        # add new payment info for user
        # add to database
        return
    elif request.method == 'GET':
        # get a list of users payment info
        # return json
        return


@app.route('/api/user/<string:username>/payment_info/<int:payment_id>', methods=['PUT'])
def EditUserPaymentInfo(username, payment_id):
    if request.method == 'PUT':
        # edit user payment info
        # add to database
        return


@app.route('/api/user/<string:username>/rides', methods=['GET'])
def UserRides(username):
    if request.method == 'GET':
        # get ride data that user participates in for a preview list
        # return json
        return


@app.route('/api/event', methods=['POST', 'GET'])
def EventAddList():
    if request.method == 'POST':
        # get event data from request.json
        # add event to base
        return
    if request.method == 'GET':
        # get list of future events
        # here maybe also use query params for search like type etc and general filters
        try:
            eventQuery = db_session.query(FutureEventView).all()
            eventDict = {'events': [
                            {
                                'event_id': e.event_id,
                                'title': e.title
                            } for e in eventQuery]
                        }
            return eventDict
        except NoResultFound:
            return {'error': 'No future events exist in the database', 'events': []}
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
        # remove an event from db
        return


@app.route('/api/event/<int:event_id>/rides', methods=['GET'])
def EventRides(event_id):
    if request.method == 'GET':
        # get ride data for a preview list
        # return json
        return


@app.route('/api/ride', methods=['POST'])
def RideAdd():
    if request.method == 'POST':
        # get ride data from request.json
        # add ride to base
        return


@app.route('/api/ride/<int:ride_id>', methods=['PUT', 'GET', 'DELETE'])
def Ride(ride_id):
    if request.method == 'PUT':
        # edit ride data
        # add ride to base
        return
    elif request.method == 'GET':
        # return a ride's data
        return
    elif request.method == 'DELETE':
        # remove a ride from db
        return


@app.route('/api/ride/<int:ride_id>/users', methods=['GET'])
def RideUsers(ride_id):
    if request.method == 'GET':
        # return a ride's list of users
        return


@app.route('/estimate_cost', methods=['GET'])
def EstimateCost():
    if request.method == 'GET':
        # get a cost estimation for a ride based on location and vehicle etc
        return


@app.route('/api/user/<string:username>/application', methods=['GET'])
def UserApplicationList(username):
    if request.method == 'GET':
        # get list of user applications
        return


@app.route('/api/ride/<int:ride_id>/application', methods=['GET', 'POST', 'PUT', 'DELETE'])
def RideApplication(ride_id):
    if request.method == 'GET':
        # get list of ride applications
        return
    elif request.method == 'POST':
        # post new application for ride and user
        return
    elif request.method == 'PUT':
        # edit application for ride and user
        return
    elif request.method == 'DELETE':
        # delete application for ride and user
        return


@app.route('/api/user/<string:username>/userrating', methods=['GET', 'POST', 'DELETE'])
def UserRating(username):
    if request.method == 'GET':
        # get list of user ratings for user
        return
    elif request.method == 'POST':
        # post new user rating for user
        return
    elif request.method == 'DELETE':
        # delete user rating for user
        return


@app.route('/api/user/<string:username>/driverrating', methods=['GET', 'POST', 'DELETE'])
def DriverRating(username):
    if request.method == 'GET':
        # get list of driver ratings for user
        return
    elif request.method == 'POST':
        # post new driver rating for user
        return
    elif request.method == 'DELETE':
        # delete driver rating for user
        return


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
        # delete a driver's data
        return

''' 
    Begin of Front End related routes
'''

@app.route('/', methods=['GET'])
def Login():
    if request.method == 'GET':
        if 'username' in session:
            return render_template("profile.html", username=session['username'])
        else:
            return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        # Validate credentials and redirect accordingly
        username = request.form['username']
        password = request.form['password']

        # Request user info via API call
        response = requests.get("http://127.0.0.1:5000" + url_for('User', username=username))
        user = response.json()

        # Authenticate user
        if ('error' not in user) and (user['password'] == password):
            session['username'] = str(username)
            # Redirect to user profile route (yet to be implemented) and render profile page
            return render_template("profile.html", username=username)
        else:
            # Render error page
            return render_template("systemMessage.html", messageTitle="Login Failed",
                                   message="The provided credentials don't match a user in our database")

    # Browser login page
    elif request.method == 'GET':
        if 'username' in session:
            return render_template("profile.html", username=session['username'])
        else:
            return render_template("login.html")


@app.route('/logout', methods=['GET'])
def Logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('Login'))

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
        profile_picture = request.form['profile_picture']

        # Request user info via API call to check if user already exists
        response = requests.get("http://127.0.0.1:5000" + url_for('User', username=username))
        user = response.json()

        if 'username' in user:
            # User already exists
            return render_template("systemMessage.html", messageTitle="User already exists",
                                   message="A user with this username already exists. If this is your username you can login.")
        else:
            # Insert user into database by posting on /api/user
            requestData = {'username':username, 'password':password, 'first_name':first_name, 'surname':surname,
                           'profile_picture':profile_picture}
            internalResponse = requests.post("http://127.0.0.1:5000" + url_for('UserListAdd'), data=requestData)
            if internalResponse.json()['status'] != 'error':
                return render_template("systemMessage.html", messageTitle="Success",
                                       message="Registration completed successfully!")
            else:
                return render_template("systemMessage.html", messageTitle="Error",
                                       message="An error occurred during registration")

@app.route('/driverCertification', methods=['GET', 'POST'])
def DriverCertification():
    if request.method == 'GET':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Check if user is already a driver
        response = requests.get("http://127.0.0.1:5000" + url_for('Driver', username=session['username']))
        if 'error' not in response.json():
            return render_template("systemMessage.html", messageTitle="Already a driver",
                                   message="You are already a driver and do not need to apply for certification.")

        # Check if user has already applied
        response = requests.get("http://127.0.0.1:5000" + url_for('UserVerify', username=session['username']))
        if 'error' not in response.json():
            return render_template("systemMessage.html", messageTitle="Already applied",
                                   message="You have already applied to be a driver, please wait until we review your application.")

        # If none of the above hold, present the driver certification application form
        return render_template("driverCertification.html")

    elif request.method == 'POST':

        # Get verification application data from request and pass on the request to the API endpoint
        driver_license = request.form['license']
        registration = request.form['registration']
        vehicle = request.form['vehicle']
        vehicle_image = request.form['vehicle_image']
        identification_document = request.form['identification_document']

        requestData = dict(license=driver_license, registration=registration,
                           vehicle=vehicle, vehicle_image=vehicle_image,
                           identification_document=identification_document)

        response = requests.post("http://127.0.0.1:5000" + url_for('UserVerify', username=session['username']), data=requestData)

        return render_template("systemMessage.html", messageTitle="Application Submitted Successfully",
                               message="Your application to be a driver has been submitted, please wait until we review your application.")
