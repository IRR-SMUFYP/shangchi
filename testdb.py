from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os
import sys
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fyptest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)


class CarouselItem(db.Model):
    __tablename__ = 'carousel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    donorName = db.Column(db.String(50), nullable=False)
    donorAdd = db.Column(db.String(300), nullable=False)
    contactNo = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer(50), nullable=False)
    requireDelivery = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(20), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.Integer, nullable=False),

    def __init__(self, name, description, donorName, donorAdd, contactNo, category, quantity, requireDelivery, region, timeSubmitted, itemStatus):
        self.name = name
        self.description = description
        self.donorName = donorName
        self.donorAdd = donorAdd
        self.contactNo = contactNo
        self.category = category
        self.quantity = quantity
        self.requireDelivery = requireDelivery
        self.region = region
        self.timeSubmitted = timeSubmitted
        self.itemStatus = itemStatus

    def json(self):
        return {"name": self.name, "description": self.description, "donorName": self.donorName, "donorAdd": self.donorAdd, "contactNo": self.contactNo, "category": self.category, "quantity": self.quantity, "requireDelivery": self.requireDelivery, "region": self.region, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

class WishList(db.Model):
    __tablename__ = 'wishlist'

# get all items submitted by donors where timeSubmitted > 0 and timeSubmitted <= 24 (time logic not done)
@app.route("/getItems")
def getAllItems():
    carouselList = CarouselItem.query.all()
    if len(carouselList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [carouselItem.json() for carouselItem in carouselList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no donations at the moment."
        }
    ), 404


# get all items submitted by donors where timeSubmitted > 0 and timeSubmitted <= 24 and filtered by category (time logic not done)
@app.route("/getItem/<Cat>")
def getItemsByCategory(Cat):
    itemList = CarouselItem.query.filter_by(category=Cat)
    if len(itemList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "itemsByCat": [carouselItem.json() for carouselItem in itemList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items listed under this category."
        }
    ), 404



if __name__ == "__main__":
    app.run(port="5004", debug=True)