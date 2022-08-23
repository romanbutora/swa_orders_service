import json
import os
import logging
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import uuid
from datetime import datetime

application = Flask(__name__)

application.config["MONGO_URI"] = os.environ['MONGO_URI']
# application.config["MONGO_URI"] = "mongodb://localhost:27017/users-service"
mongo = PyMongo(application)
db = mongo.db

@application.route('/v1/orders/test', methods=['GET'])
def defaultpage():
    logging.info("Healthcheck successful!")
    return jsonify(
            status=True,
            message="Working!"
        )

@application.route('/v1/orders/<idx>', methods=['GET'])
def read(idx):
    data = db.orders.find_one({ "orderid" : idx})

    if data is not None:
        logging.info(idx + " was returned!")
        return json.loads(json_util.dumps(data))

    else:
        logging.info(idx + " order not found!")
        return jsonify(
            status=True,
            message="Not found!"
        )



@application.route('/v1/orders', methods=['POST'])
def create():
    neworderid = str(uuid.uuid4().hex)

    item = {
        'orderid' : neworderid,
        'time' : datetime.now(),
        'products': request.form['products'],
        'price' : request.form['price'],
        'user' : request.form ['userid']
    }
    db.orders.insert_one(item)

    logging.info(neworderid + " was created!")
    return jsonify(
        status=True,
        user = request.form ['userid'],
        products=request.form['products'],
        price=request.form['price'],
        orderid=neworderid,
        message='Saved successfully!'
    ), 201

@application.route('/v1/orders/<idx>', methods=['PUT'])
def update(idx):
    myquery = {"orderid" :idx}
    newvalues = {"$set": {'products': request.form['products'],
        'price' : request.form['price'],
        'user' : request.form ['userid']}}

    db.orders.update_one(myquery,newvalues)
    logging.info(idx + " was updated!")
    return jsonify(
        status=True,
        user=request.form['userid'],
        products=request.form['products'],
        price=request.form['price'],
        message='Updated'
    ), 201

@application.route('/v1/orders/<idx>', methods=['DELETE'])
def deleteone(idx):
    myquery = {"orderid" :idx}
    data = db.orders.find_one({"orderid": idx})
    db.orders.delete_one(myquery)

    if data is not None:
        logging.info(idx + " deleted successfully!")
        return jsonify(
            status=True,
            message=idx + ' deleted successfully!'
        ), 201

    else:
        logging.info(idx + " was not found, so deleted anyway!")
        return jsonify(
            status=True,
            message='Nothing deleted!'
        ), 201

@application.route('/v1/orders', methods=['DELETE'])
def deleteall():

    x =  db.orders.delete_many({})
    logging.warning("All orders deleted!")
    return jsonify(
        status=True,
        message='Deleted' + str(x.deleted_count) + 'orders!'
    ), 201

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)