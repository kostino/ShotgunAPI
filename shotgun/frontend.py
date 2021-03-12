from flask import Flask, render_template, request, session, send_from_directory, url_for, redirect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from base64 import b64encode
import requests

from utils import *
from config import *
from app import app

CONFIG_DIR = './config.ini'
config = ShotgunConfig(CONFIG_DIR)

DATA_ROOT = config.data_root
PROFILE_DIR = os.path.join(DATA_ROOT, 'profile')
VEHICLE_DIR = os.path.join(DATA_ROOT, 'vehicle')
DOCS_DIR = os.path.join(DATA_ROOT, 'docs')
EVENT_PICS_DIR = os.path.join(DATA_ROOT, config.event_pics_dir)


@app.route('/', methods=['GET'])
def Index():
    if request.method == 'GET':

        # Get future events and then their info via API call
        response = requests.get(url_for('EventAddList', _external=True)).json()
        if 'events' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        events = response['events']

        return render_template("home.html", events=events)


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
            if request.form['lat'] and request.form['lat'] != '':
                session['latitude'] = str(request.form['lat'])
            if request.form['long'] and request.form['long'] != '':
                session['longitude'] = str(request.form['long'])

            #add driver check in session
            response = requests.get(url_for('Driver', username=session['username'], _external=True))
            session['driver'] = 'error' not in response.json()
            # Load profile picture filename to session
            session['profile_picture'] = user['profile_picture']

            # Redirect to user profile route (yet to be implemented) and render profile page
            return redirect(url_for("Index", _external=True))
        else:
            # Render error page
            return render_template("systemMessage.html", messageTitle="Login Failed",
                                   message="The provided credentials don't match a user in our database",
                                   context={
                                       'button_text': 'Back to Login',
                                       'redirect_link': url_for('Login', _external=True)
                                   })

    # Browser login page
    elif request.method == 'GET':
        if 'username' in session:
            return redirect(url_for("Index", _external=True))
        else:
            return render_template("login.html")


@app.route('/logout', methods=['GET'])
def Logout():
    if 'username' in session:
        session.pop('username', None)
    if 'latitude' in session:
        session.pop('latitude', None)
    if 'longitude' in session:
        session.pop('longitude', None)
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
        email = request.form['email']
        first_name = request.form['first_name']
        surname = request.form['surname']

        # Encode profile picture
        profile_picture = None
        f = request.files['profile_picture']
        if f.filename != '':
            if not check_image_ext(f.filename):
                return render_template('systemMessage.html', messageTitle='Invalid image format',
                                       message='The profile picture must be a JPEG image.',
                                       context={
                                           'button_text': 'Back to Register',
                                           'redirect_link': url_for('Register', _external=True)
                                       })
            profile_picture = b64encode(f.read()).decode('ascii')

        # Insert user into database by posting on /api/user
        requestData = {'username': username, 'password': password, 'email': email, 'first_name': first_name,
                       'surname': surname, 'profile_picture': profile_picture}
        response = requests.post(url_for('UserListAdd', _external=True), data=requestData).json()
        if 'error' not in response:
            return render_template('systemMessage.html', messageTitle='Success',
                                   message='Registration completed successfully!',
                                   context={
                                       'button_text': 'Homepage',
                                       'redirect_link': url_for('Index', _external=True)
                                   })
        else:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'],
                                   context={
                                       'button_text': 'Back to Register',
                                       'redirect_link': url_for('Register', _external=True)
                                   })


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
                                   message="You are already a driver and do not need to apply for certification.",
                                   context={
                                       'button_text': 'Back to Homepage',
                                       'redirect_link': url_for('Index', _external=True)
                                   })

        # Check if user has already applied
        response = requests.get(url_for('UserVerify', username=session['username'], _external=True))
        if 'error' not in response.json():
            return render_template("systemMessage.html", messageTitle="Already applied",
                                   message="You have already applied to be a driver, please wait until we review your application.",
                                   context={
                                       'button_text': 'Back to Homepage',
                                       'redirect_link': url_for('Index', _external=True)
                                   })

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
                                       message='The required documents must be JPEG images.',
                                       context={
                                           'button_text': 'Back to DriverCertification',
                                           'redirect_link': url_for('DriverCertification', _external=True)
                                       })
            requestData[field] = b64encode(f.read()).decode('ascii')

        # Pass request to the API endpoint
        response = requests.post(url_for('UserVerify', username=session['username'], _external=True),
                                 data=requestData).json()
        if 'error' not in response:
            return render_template('systemMessage.html', messageTitle='Application Submitted Successfully',
                                   message='Your application to be a driver has been submitted, please wait until we review your application.',
                                   context={
                                       'button_text': 'Back to Homepage',
                                       'redirect_link': url_for('Index', _external=True)
                                   })
        else:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'],
                                   context={
                                       'button_text': 'Back to DriverCertification',
                                       'redirect_link': url_for('DriverCertification', _external=True)
                                   })


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
            return render_template('systemMessage.html', messageTitle='Error', message=userData['error'],
                                   context={
                                       'button_text': 'Back to Homepage',
                                       'redirect_link': url_for('Index', _external=True)
                                   })

        # Get user ratings
        userRatings = requests.get(url_for('UserRating', username=username, _external=True)).json()
        if 'ratings' not in userRatings:
            return render_template('systemMessage.html', messageTitle='Error', message=userRatings['error'],
                                   context={
                                       'button_text': 'Back to Hompage',
                                       'redirect_link': url_for('Index', _external=True)
                                   })

        # Check if user is a driver
        response = requests.get(url_for('Driver', username=username, _external=True))
        driverData = response.json()
        if 'error' not in driverData:
            driverFlag = True

            # Get driver ratings
            driverRatings = requests.get(url_for('DriverRating', username=username, _external=True)).json()
            if 'ratings' not in driverRatings:
                return render_template('systemMessage.html', messageTitle='Error', message=userRatings['error'],
                                       context={
                                           'button_text': 'Back to Homepage',
                                           'redirect_link': url_for('Index', _external=True)
                                       })

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
                return render_template('systemMessage.html', messageTitle='Error', message=userData['error'],
                                       context={
                                           'button_text': 'Back to Profile',
                                           'redirect_link': url_for('UserProfile', username=session['username'], _external=True)
                                       })

            # Check if user is a driver and get data
            driverData = requests.get(url_for('Driver', username=username, _external=True)).json()
            driverFlag = 'error' not in driverData

            return render_template("editUserProfile.html", userData=userData, driverFlag=driverFlag,
                                   driverData=driverData)
        else:
            return render_template("systemMessage.html", messageTitle="Edit user profile error",
                                   message="You tried to edit someone else's profile. Let's edit yours.",
                                   context={
                                       'button_text': 'Edit your Profile',
                                       'redirect_link': url_for("EditUserProfile", username=session['username'], _external=True)
                                   })

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
                return render_template('systemMessage.html', messageTitle='Error', message=user['error'],
                                       context={
                                           'button_text': 'Back to Edit',
                                           'redirect_link': url_for('EditUserProfile', username=session['username'], _external=True)
                                       })

            # If a new profile picture is added, update the existing one
            f = request.files['profile_picture']
            if f.filename != '':
                if not check_image_ext(f.filename):
                    return render_template('systemMessage.html', messageTitle='Invalid image format',
                                           message='The profile picture must be a JPEG image.',
                                           context={
                                               'button_text': 'Back to Edit',
                                               'redirect_link': url_for('EditUserProfile', username=session['username'], _external=True)
                                           })
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
                                   message="User does not exist or unauthorized edit was attempted.",
                                   context={
                                       'button_text': 'Back to Edit',
                                       'redirect_link': url_for('EditUserProfile', username=session['username'], _external=True)
                                   })


@app.route('/paymentmethods', methods=['GET'])
def PaymentMethods():
    if request.method == 'GET':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Get payment methods
        username = session['username']
        response = requests.get(url_for('PaymentInfoList', username=username, _external=True)).json()
        if 'credit_cards' not in response or 'paypal_accounts' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'],
                                   context={
                                       'button_text': 'Back to Homepage',
                                       'redirect_link': url_for('Index',_external=True)
                                   })

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
                                   message="An error occurred while setting the primary payment method.",
                                   context={
                                       'button_text': 'Back to PaymentMethods',
                                       'redirect_link': url_for('PaymentMethods', _external=True)
                                   })

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
        response = requests.post(url_for('PaymentInfoList', username=session['username'], _external=True),
                                 data=requestData).json()
        if 'error' not in response:
            return redirect(url_for('PaymentMethods'))
        else:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'],
                                   context={
                                       'button_text': 'Back to PaymentMethods',
                                       'redirect_link': url_for('PaymentMethods', _external=True)
                                   })


@app.route('/deletepaymentmethod', methods=['POST'])
def DeletePaymentMethod():
    if request.method == 'POST':
        # Check if user logged in
        if 'username' not in session:
            return redirect(url_for('Login'))

        username = session['username']
        payment_id = request.form['payment_id']

        # Pass request to the API endpoint
        response = requests.delete(
            url_for('PaymentInfo', username=username, payment_id=payment_id, _external=True)).json()
        if 'error' not in response:
            return redirect(url_for('PaymentMethods'))
        else:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'],
                                   context={
                                       'button_text': 'Back to PaymentMethods',
                                       'redirect_link': url_for('PaymentMethods', _external=True)
                                   })


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
        return render_template("createEvent.html", event_types=config.event_types)
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
        response = requests.post(url_for('EventAddList', _external=True), data=requestData).json()
        if 'error' in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'],
                                   context={
                                       'button_text': 'Go Back',
                                       'redirect_link': url_for('CreateEvent', _external=True)
                                   })
        else:
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
        events = [event for event in response['events'] if event['status'] != 'pending']

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


@app.route('/data/event_pics/<event_type>')
def EventPictures(event_type):
    filename = secure_filename('{}.jpg'.format(event_type))
    return send_from_directory(EVENT_PICS_DIR, filename)


@app.route('/data/docs/<userdir>/<filename>')
def Documents(userdir, filename):
    userdir = secure_filename(userdir)
    filename = secure_filename(filename)
    return send_from_directory(DOCS_DIR, os.path.join(userdir, filename))


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

        location_in_session = 'longitude' in session and 'latitude' in session
        location_valid = session['longitude'] != '' and session['latitude'] != '' if location_in_session else False
        if location_valid:
            rides = sorted(rides, key=lambda r: haversine(
                float(session['longitude']), float(session['latitude']),
                float(r['longitude']), float(r['latitude'])
            )
                           )

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
        response = requests.get(url_for('RideList', _external=True)).json()
        if 'rides' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        past_rides = [r['ride_id'] for r in response['rides'] if is_past_date(r['start_datetime'][:16])]

        # converting a large list to a set speeds up the program tremendously
        my_past_rides = [ride for ride in my_rides if ride in set(past_rides)]
        to_rate_by_ride = []
        for r in my_past_rides:

            # Get people on ride
            rate_data = requests.get(url_for('PeopleToRate', username=username, ride_id=r, _external=True)).json()

            # Add ride id
            rate_data['ride_id'] = r

            # Get ride info
            rideInfo = requests.get(url_for('Ride', ride_id=r, _external=True)).json()
            rate_data['driver'] = rideInfo['driver_username']
            if 'error' in rideInfo:
                continue
            rate_data['event_id'] = rideInfo['event_id']

            # Get event info
            eventInfo = requests.get(url_for('Event', event_id=rate_data['event_id'], _external=True)).json()
            if 'error' in eventInfo:
                continue
            rate_data['event_title'] = eventInfo['title']

            to_rate_by_ride.append(rate_data)

        # Get users to be rated information
        usernames = []
        for ride in to_rate_by_ride:
            usernames.append(ride['driver'])
            usernames = usernames + ride['users']
        usernames = set(usernames)
        users = {}
        for username in usernames:
            response = requests.get(url_for("User", username=username, _external=True)).json()
            users[username] = {
                'first_name': response['first_name'],
                'surname': response['surname'],
                'profile_picture': response['profile_picture']
            }

        # TODO: Here render_template and provide to_rate_by_ride as context
        return render_template('ratePastRides.html', rides=to_rate_by_ride, users=users)

    if request.method == 'POST':
        # Submit rating POST

        ratee = request.form['ratee']
        comment = request.form['comment']
        rating = int(request.form['rating'])
        ratingType = request.form['type']

        postData = {
            'rater': session['username'],
            'ratee': ratee,
            'stars': rating,
            'comment':comment
        }

        if ratingType == 'Passenger':
            response = requests.post(url_for("UserRating", username=ratee, _external=True), data=postData).json()
        elif ratingType == 'Driver':
            response = requests.post(url_for("DriverRating", username=ratee, _external=True), data=postData).json()
        else:
            return render_template("systemMessage.html", messageTitle="Error Submitting",
                                   message="There was an error submitting your rating. Please try again later.",
                                   context={
                                       'button_text': 'Go Back',
                                       'redirect_link': url_for("RateRides", _external=True)
                                   })

        if 'error' in response:
            return render_template("systemMessage.html", messageTitle="Error Submitting", message=response['error'],
                                   context={
                                       'button_text': 'Go Back',
                                       'redirect_link': url_for("RateRides", _external=True)
                                   })

        return redirect(url_for("RateRides", _external=True))


@app.route('/my_rides', methods=['GET', 'POST'])
def ManageMyRides():
    if request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('Login'))

        # Get future rides
        username = session['username']
        response = requests.get(url_for('UserRides', username=username, _external=True)).json()
        if 'rides' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        not_expired_rides = [r for r in response['rides'] if not is_past_date(r['start_datetime'][:16])]

        rides = []
        users = {}
        for r in not_expired_rides:
            # Get event info
            eventInfo = requests.get(url_for('Event', event_id=r['event_id'], _external=True)).json()
            if 'error' in eventInfo:
                continue
            r['event_title'] = eventInfo['title']

            # Get ride applications
            response = requests.get(url_for('RideApplication', ride_id=r['ride_id'], _external=True)).json()
            if 'applications' not in response:
                continue
            r['applications'] = response['applications']

            # Get users that applied
            for application in r['applications']:
                app_username = application['username']
                userInfo = requests.get(url_for('User', username=app_username, _external=True)).json()
                if 'error' in userInfo:
                    return render_template('systemMessage.html', messageTitle='Error', message=userInfo['error'])
                users[app_username] = userInfo

            rides.append(r)
        return render_template('manageRides.html', rides=rides, users=users)

    elif request.method == 'POST':
        # TODO: Add extra validation (can this driver do this, seat limitations etc) to POST requests possibly in the API route

        # Get request data
        ride_id = request.form['ride_id']
        username = request.form['username']

        # Call API
        if request.form['status'] == 'accepted':
            response = requests.post(url_for('ApplicationAccept', ride_id=ride_id, username=username, _external=True)).json()
        elif request.form['status'] == 'rejected':
            response = requests.post(url_for('ApplicationReject', ride_id=ride_id, username=username, _external=True)).json()
        else:
            return render_template('systemMessage.html', messageTitle='Error', message='Invalid data')

        if 'error' in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        else:
            return redirect(url_for('ManageMyRides'))


@app.route('/my_applications', methods=['GET'])
def MyRideApplications():
    if 'username' not in session:
        return redirect(url_for('Login'))

    username = session['username']

    # Get applications
    response = requests.get(url_for('UserApplicationList', username=username, _external=True)).json()
    if 'applications' not in response:
        return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
    applications = response['applications']

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
        app_driver = application['ride_driver']
        userInfo = requests.get(url_for("User", username=app_driver, _external=True)).json()
        if 'error' in userInfo:
            return render_template('systemMessage.html', messageTitle='Error', message=userInfo['error'])

        driverPictures[app_driver]['profile_picture'] = userInfo['profile_picture']
        driverPictures[app_driver]['first_name'] = userInfo['first_name']
        driverPictures[app_driver]['surname'] = userInfo['surname']

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


@app.route('/mod/events_to_approve', methods=['GET', 'POST'])
def ModEventsToApprove():
    if request.method == 'GET':
        # Get pending events
        response = requests.get(url_for('EventSearchAPI', _external=True), params={'old': 1, 'tag':''}).json()
        if 'events' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        events = [event for event in response['events'] if event['status'] == 'pending']

        return render_template('modApproveEvents.html', title='Approve Events', events=events)
    if request.method == 'POST':
        action = request.form['action']
        event_id = request.form['event_id']
        if action == 'accept':
            put_data = {'status': 'active'}
            response = requests.put(url_for('Event', event_id=event_id, _external=True), data=put_data).json()
            if 'error' in response:
                return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
            return redirect(url_for('ModEventsToApprove'))
        elif action == 'reject':
            response = requests.delete(url_for('Event', event_id=event_id, _external=True)).json()
            if 'error' in response:
                return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
            return redirect(url_for('ModEventsToApprove'))
        else:
            return render_template('systemMessage.html', messageTitle='Error', message='Wrong action')


@app.route('/mod/drivers_to_approve', methods=['GET', 'POST'])
def ModDriversToApprove():
    if request.method == 'GET':
        # Get driver verification applications
        response = requests.get(url_for('VerificationApplicationList', _external=True)).json()
        if 'applications' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        applications = response['applications']

        return render_template('modApproveDrivers.html', applications=applications)
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']

        if action == 'accept':
            response = requests.get(url_for('UserVerify', username=username, _external=True)).json()
            if 'error' in response:
                return render_template('systemMessage.html', messageTitle='Error', message=response['error'])

            vehicle_image_path = os.path.join(DOCS_DIR, response['vehicle_image'])
            with open(vehicle_image_path, 'rb') as f:
                vehicle_image_data = b64encode(f.read()).decode('ascii')

            driver_data = {
                'username': username,
                'vehicle': response['vehicle'],
                'vehicle_image': vehicle_image_data
            }
            response = requests.post(url_for('DriverAdd', _external=True), data=driver_data).json()
            if 'error' in response:
                return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
            return redirect(url_for('ModDriversToApprove'))
        elif action == 'reject':
            response = requests.delete(url_for('UserVerify', username=username, _external=True)).json()
            if 'error' in response:
                return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
            return redirect(url_for('ModDriversToApprove'))
        else:
            return render_template('systemMessage.html', messageTitle='Error', message='Wrong action')


@app.route('/mod/index', methods=['GET'])
def ModIndex():
    return render_template('modIndex.html')


@app.route('/events/nearby', methods=['GET'])
def NearbyEvents():
    if request.method == 'GET':
        # DEBUG default location LEFKOS PIRGOS
        if 'latitude' not in session.keys() or 'longitude' not in session.keys():
            session['latitude'] = '40.6234131'
            session['longitude'] = '22.9482666'
        # Get future events and then their info via API call
        response = requests.get(url_for('EventAddList', _external=True)).json()
        if 'events' not in response:
            return render_template('systemMessage.html', messageTitle='Error', message=response['error'])
        events = sorted(response['events'],
                        key=lambda event: haversine(
                            float(session['longitude']), float(session['latitude']),
                            float(event['longitude']), float(event['latitude'])
                        )
                        )[:10]

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
        return render_template("browseEvents.html", events=events, title="Nearby Events", driverFlag=driverFlag, userEventsWithRide=userEventsWithRide)


@app.route('/about', methods=['GET'])
def About():
    if request.method == 'GET':
        return render_template('about.html')
