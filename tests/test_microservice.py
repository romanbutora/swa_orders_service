"""
test_microservice.py
~~~~~~~~~~~~~~~~~~~~

Tests the the service returns the expected responses .
"""

import json
import unittest
from flask_pymongo import PyMongo
from app.app import application
import logging

class TestMicroserviceAPI(unittest.TestCase):
    def setUp(self):
        self.client = application.test_client()

    def test_post_order(self):
        # arrange
        uri = '/v1/orders'
        mockproduct = "phone"
        mockprice = "129"
        mockuserid = "honza"
        mydata = dict(products=mockproduct, price=mockprice, userid=mockuserid)

        # act
        response = self.client.post(uri, data = mydata)
        jsonresp = response.get_json()

        # assert
        self.assertEqual(str(jsonresp["products"]), mockproduct)
        self.assertEqual(str(jsonresp["price"]), mockprice)
        self.assertEqual(str(jsonresp["user"]), mockuserid)


    def test_get_order(self):
        # arrange
        uri = '/v1/orders'
        mockproduct = "macbook"
        mockprice = "229"
        mockuserid = "rasto"
        mydata = dict(products=mockproduct, price=mockprice, userid=mockuserid)
        response = self.client.post(uri, data = mydata)
        jsonresp = response.get_json()
        orderid = str(jsonresp["orderid"])

        # act
        response2 = self.client.get(uri + "/" + orderid)
        jsonresp2 = response2.get_json()

        # assert
        self.assertEqual(str(jsonresp2["products"]), mockproduct)
        self.assertEqual(str(jsonresp2["price"]), mockprice)
        self.assertEqual(str(jsonresp2["user"]), mockuserid)

    def test_update_order(self):
        # arrange
        uri = '/v1/orders'
        mockproduct = "ipod"
        mockprice = "829"
        mockuserid = "jirka"
        mockproduct_changed = "ipod2"
        mockprice_changed = "929"
        mockuserid_changed = "jirka2"
        mydata = dict(products=mockproduct, price=mockprice, userid=mockuserid)
        response = self.client.post(uri, data = mydata)
        jsonresp = response.get_json()
        orderid = str(jsonresp["orderid"])
        mydata2 = dict(products=mockproduct_changed, price=mockprice_changed, userid=mockuserid_changed)

        # act
        response2 = self.client.put(uri + "/" + orderid, data=mydata2)
        jsonresp2 = response2.get_json()

        # assert
        self.assertEqual(str(jsonresp2["products"]), mockproduct_changed)
        self.assertEqual(str(jsonresp2["price"]), mockprice_changed)
        self.assertEqual(str(jsonresp2["user"]), mockuserid_changed)

    def test_delete_order(self):
        # arrange
        uri = '/v1/orders'
        mockproduct = "macbook"
        mockprice = "229"
        mockuserid = "rasto"
        mydata = dict(products=mockproduct, price=mockprice, userid=mockuserid)
        response = self.client.post(uri, data = mydata)
        jsonresp = response.get_json()
        orderid = str(jsonresp["orderid"])

        # act
        response2 = self.client.delete(uri + "/" + orderid)
        jsonresp2 = response2.get_json()
        response3 = self.client.get(uri + "/" + orderid)
        jsonresp3 = response3.get_json()

        # assert
        self.assertEqual(str(jsonresp2["message"]), orderid + " deleted successfully!")
        self.assertEqual(str(jsonresp3["message"]), "Not found!")




if __name__ == '__main__':
    unittest.main()