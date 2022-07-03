import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import uuid
from datetime import datetime

application = Flask(__name__)

application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(application)
db = mongo.db

@application.route('/')
def defaultpage():
    return jsonify(
        status=True,
        message="working"
    )

@application.route('/v1/orders/<idx>')
def read(idx):
    data = db.orders.find({ "orderid" : idx})

    results = list(data)

    if len(results) > 0:
        return jsonify(
            status=True,
            message=data
        )

    else:
        return jsonify(
            status=True,
            message="Not found!"
        )



@application.route('/v1/orders', methods=['POST'])
def create():

    item = {
        'orderid' : str(uuid.uuid4().hex),
        'time' : datetime.now(),
        'products': request.form['products'],
        'price' : request.form['price'],
        'user' : request.form ['userid']
    }
    db.orders.insert_one(item)

    return jsonify(
        status=True,
        message='Saved successfully!'
    ), 201

@application.route('/v1/orders/<idx>', methods=['PUT'])
def update(idx):

    myquery = {"orderid" :idx}
    newvalues = {"$set": {'products': request.form['products'],
        'price' : request.form['price'],
        'user' : request.form ['userid']}}

    db.orders.update_one(myquery,newvalues)

    return jsonify(
        status=True,
        message='Updated'
    ), 201

@application.route('/v1/orders/<idx>', methods=['DELETE'])
def deleteone(idx):
    myquery = {"orderid" :idx}
    db.orders.delete_one(myquery)

    return jsonify(
        status=True,
        message= idx + ' Deleted successfully!'
    ), 201

@application.route('/v1/orders', methods=['DELETE'])
def deleteall():

    x =  db.orders.delete_many({})

    return jsonify(
        status=True,
        message='Deleted' + str(x.deleted_count) + 'orders!'
    ), 201

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)