from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from flask import Flask, render_template, request, session, url_for, redirect, json, jsonify

import requests

# Initialize SQL Alchemy
engine = create_engine('mysql://admin@localhost/shotgundb?charset=utf8mb4')
Base = automap_base()
Base.prepare(engine, reflect=True)

# Shortcuts to database tables
UserTable = Base.classes.user

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
        return {'status':'success'}, 200
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


@app.route('/api/user/<string:username>/verify', methods=['POST'])
def UserVerify(username):
    if request.method == 'POST':
        # get verification application data from request
        # add to database
        return


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
        return


@app.route('/api/event/<int:event_id>', methods=['PUT', 'GET', 'DELETE'])
def Event(event_id):
    if request.method == 'PUT':
        # edit event data
        # add event to base
        return
    elif request.method == 'GET':
        # return an event's data
        return
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
        return
    elif request.method == 'DELETE':
        # delete a driver's data
        return

''' 
    Begin of GUI related routes
'''

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
