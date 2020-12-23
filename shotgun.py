from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from flask import Flask, render_template, request, json

# Example from personal project on sqlalchemy orm
'''
engine = create_engine('mysql://root@localhost/shisha_skg?charset=utf8mb4')
Base = automap_base()
Base.prepare(engine, reflect=True)
Package = Base.classes.product_packages
Price = Base.classes.prices
Product = Base.classes.products
Order = Base.classes.orders
OrderItem = Base.classes.order_items
session = Session(engine)
'''
app = Flask(__name__)


@app.route('/api/user', methods=['POST', 'GET'])
def UserListAdd():
    if request.method == 'POST':
        # get user data from request.json
        # add user to base
        return
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
        return
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
def UserPaymentInfo(username, payment_id):
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
