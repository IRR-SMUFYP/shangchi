from distutils.command.upload import upload
from pdb import lasti2lineno
from typing import ItemsView, Match
from urllib import response
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from datetime import datetime

import os
import sys
from os import environ
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fyptest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

uploads_dir = os.path.join('../assets/img/donations')


class CarouselItem(db.Model):
    __tablename__ = 'carousel'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    itemName = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    donorName = db.Column(db.String(50), nullable=False)
    donorAddr = db.Column(db.String(300), nullable=False)
    contactNo = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    requireDelivery = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(20), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.Integer, nullable=False)
    fileName = db.Column(db.String(200), nullable=False)

    def __init__(self, id, itemName, description, donorName, donorAddr, contactNo, category, quantity, requireDelivery, region, timeSubmitted, itemStatus, fileName):
        self.id = id
        self.itemName = itemName
        self.description = description
        self.donorName = donorName
        self.donorAddr = donorAddr
        self.contactNo = contactNo
        self.category = category
        self.quantity = quantity
        self.requireDelivery = requireDelivery
        self.region = region
        self.timeSubmitted = timeSubmitted
        self.itemStatus = itemStatus
        self.fileName = fileName

    def json(self):
        return {"id": self.id, "itemName": self.itemName, "description": self.description, "donorName": self.donorName, "donorAddr": self.donorAddr, 
                "contactNo": self.contactNo, "category": self.category, "quantity": self.quantity, "requireDelivery": self.requireDelivery, 
                "region": self.region, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus, "fileName": self.fileName}

class NewCarousel(db.Model):
    __tablename__ = 'newcarousel'
    
    carouselID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donorID = db.Column(db.Integer)
    submissionID = db.Column(db.String(30), nullable=False)
    itemName = db.Column(db.String(50), nullable=False)
    itemCategory = db.Column(db.String(50), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"carouselID": self.carouselID, "donorID": self.donorID, "submissionID": self.submissionID, "itemName": self.itemName, "itemCategory": self.itemCategory, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}


# get column headers
@app.route("/getCarouselItemColumns")
def getCarouselItemColumns():
    return jsonify(
        {
            "code": 200,
            "data": {
                "columns": CarouselItem.metadata.tables["carousel"].columns.keys()
            }
        }
    )

# get all items submitted by donors where timeSubmitted > 0 and timeSubmitted <= 24 (time logic not done)
@app.route("/getAllItems")
def getAllItems():
    carouselList = CarouselItem.query.all()
    if len(carouselList):
        # result = []
        # columnNames = dir(CarouselItem)
        # print(type(columnNames))
        # for item in carouselList:
        #     for colName in columnNames:
        #         result.append({ colName: item[colName] })
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

# get specific item in carousel
@app.route("/getItem/<int:id>")
def getItemByID(id):
    carouselItem = CarouselItem.query.filter_by(id=id).first()
    if carouselItem:
        return jsonify(
            {
                "code": 200,
                "data": carouselItem.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Item cannot be found for this ID."
        }
    ), 404

# edit donated (carousel) item in table
@app.route("/updateItem/<int:itemID>", methods=["PUT"])
def updateItem(itemID):
    item = CarouselItem.query.filter_by(id=itemID).first()
    data = request.get_json()
    if (item is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This item ID is not found in the database."
            }
        )
    else:
        # for col in data:
        #     item.col = data[col]
        item.itemName = data['itemName']
        item.description = data['description']
        item.donorName = data['donorName']
        item.donorAddr = data['donorAddr']
        item.contactNo = data['contactNo']
        item.category = data['category']
        item.quantity = data['quantity']
        item.requireDelivery = data['requireDelivery']
        item.region = data['region']
        item.itemStatus = data['itemStatus']
        db.session.add(item)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Item successfully updated."
            }
        )

# edit donated (carousel) photo in table
# @app.route("/updatePhoto/<int:itemID>", methods=["POST"])
# def updatePhoto(itemID):
#     item = CarouselItem.query.filter_by(id=itemID).first()
#     data = request.to_dict()
#     if (item is None):
#         return jsonify( 
#             {
#                 "code": 404,
#                 "message": "This item ID is not found in the database."
#             }
#         )
#     else:
#         imgFile = request.files['file']
#         fileName = secure_filename(imgFile.filename)
#         imgFile.save(os.path.join(uploads_dir, fileName))
#         item.fileName = data['itemImg']
#         db.session.commit()
#         return jsonify(
#             {
#                 "code": 200,
#                 "message": "Item successfully updated."
#             }
#         )


class Request(db.Model):
    __tablename__ = 'request'

    reqID = db.Column(db.Integer, primary_key=True, nullable=False)
    requestorContactNo = db.Column(db.String(50), nullable=False)
    deliveryLocation = db.Column(db.String(300), nullable=False)
    itemCategory = db.Column(db.String(50), nullable=False)
    requestQty = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)

    def __init__(self, reqID, requestorContactNo, deliveryLocation, itemCategory, requestQty, timeSubmitted):
        self.reqID = reqID
        self.requestorContactNo = requestorContactNo
        self.deliveryLocation = deliveryLocation
        self.itemCategory = itemCategory
        self.requestyQty = requestQty
        self.timeSubmitted = timeSubmitted

    def json(self):
        return {"reqID": self.reqID, "requestorContactNo": self.requestorContactNo, "deliveryLocation": self.deliveryLocation, 
                "itemCategory": self.itemCategory, "requestQty": self.requestQty, "timeSubmitted": self.timeSubmitted}

# get all requests submitted by migrant workers
@app.route("/getRequests")
def getAllRequests():
    requestList = Request.query.all()
    if len(requestList):
        return jsonify(
            {
                "code": 200,
                "columnHeaders": Request.metadata.tables["request"].columns.keys(),
                "data": [request.json() for request in requestList]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no requests at the moment."
        }
    ), 404

# get specific request submitted by migrant workers
@app.route("/getRequests/<int:id>")
def getRequestByID(id):
    request = Request.query.filter_by(reqid=id).first()
    if request:
        return jsonify(
            {
                "code": 200,
                "columnHeaders": Request.metadata.tables["request"].columns.keys(),
                "data": request.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Request cannot be found for this ID."
        }
    ), 404

# get requests submitted for specific item
@app.route("/getRequestsByItem/<itemID>")
def getRequestByItemID(itemID):
    requests = Request.query.filter_by(itemID=itemID)
    if requests:
        return jsonify(
            {
                "code": 200,
                "columnHeaders": Request.metadata.tables["request"].columns.keys(),
                "data": [request.json() for request in requests]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Requests cannot be found for this item ID."
        }
    ), 404

# get list of migrant workers that requested specific item
@app.route("/getMigrantWorkersListByItem/<itemID>")
def getMigrantWorkersListByItemID(itemID):
    requests = Request.query.filter_by(itemID=itemID)
    mwList = []
    if requests:
        for req in requests:
            mwList.append(req.requestorContactNo)
        return jsonify(
            {
                "code": 200,
                "data": mwList
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No migrant workers requested for this item ID."
        }
    ), 404


# edit request in table
@app.route("/updateRequest/<int:id>", methods=["PUT"])
def updateRequest(id):
    requested = Request.query.filter_by(reqid=id).first()
    data = request.get_json()
    if (requested is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This ID is not found in the database."
            }
        )
    else:
        requested.deliveryLocation = data['deliveryLocation']
        requested.itemCategory = data['itemCategory']
        requested.requestQty = data['requestQty']
        db.session.add(requested)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Request successfully updated."
            }
        )

class MigrantWorker(db.Model):
    __tablename__ = 'migrantworker'

    contactNo = db.Column(db.Integer, primary_key=True, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    reqHistory = db.Column(db.Integer, nullable=False)

    def __init__(self, contactNo, address, reqHistory):
        self.contactNo = contactNo
        self.address = address
        self.reqHistory = reqHistory

    def json(self):
        return {"contactNo": self.contactNo, "address": self.address, "reqHistory": self.reqHistory}

# get all migrant workers details
@app.route("/getAllMigrantWorkers")
def getAllMigrantWorkers():
    migrantWorkers = MigrantWorker.query.all()
    if migrantWorkers:
        return jsonify(
            {
                "code": 200,
                "data": [mw.json() for mw in migrantWorkers]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No migrant workers requested for this item ID."
        }
    ), 404

# get reqHistory for specific migrant worker
@app.route("/getReqHistory/<contactNo>")
def getReqHistory(contactNo):
    migrantWorker = MigrantWorker.query.filter_by(contactNo=contactNo).first()
    if migrantWorker:
        return jsonify(
            {
                "code": 200,
                "data": { migrantWorker.contactNo: migrantWorker.reqHistory }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No migrant workers requested for this item ID."
        }
    ), 404


# check for the list of MWs, how long since each of them have gotten an item
@app.route("/getMWLastItemWeeks/<itemID>")
def getMWLastItemWeeks(itemID):
    requests = Request.query.filter_by(itemID=itemID)
    if requests:
        mwList = []
        reqHist = {}
        for req in requests:
            mwList.append(req.requestorContactNo)
        for num in mwList:
            migrantWorker = MigrantWorker.query.filter_by(contactNo=num).first()
            if migrantWorker.reqHistory in reqHist.keys():
                reqHist[migrantWorker.reqHistory] += [migrantWorker.contactNo]
            else:
                reqHist[migrantWorker.reqHistory] = [migrantWorker.contactNo]
        allKeys = reqHist.keys()
        minValue = min(allKeys)
        priorityMW = reqHist[minValue]
        return jsonify(
            {
                "code": 200,
                "data": priorityMW,
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No migrant workers requested for this item ID."
        }
    ), 404


class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    itemName = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.Integer, nullable=False)

    def __init__(self, id, itemName, remarks, category, timeSubmitted, itemStatus):
        self.id = id
        self.itemName = itemName
        self.remarks = remarks
        self.category = category
        self.timeSubmitted = timeSubmitted
        self.itemStauts = itemStatus

    def json(self):
        return {"id": self.id, "itemName": self.itemName, "remarks": self.remarks, "category": self.category, 
                "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

# get all wishlist submitted by migrant workers
# @app.route("/getWishlist")
# def getWishlist():
#     wishlist = Wishlist.query.all()
#     if len(wishlist):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": [wish.json() for wish in wishlist]
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are no requests at the moment."
#         }
#     ), 404

# get specific wishlist submitted by migrant workers by wishlist ID
# @app.route("/getWishlist/<int:id>")
# def getWishlistByID(id):
#     wishlist = Wishlist.query.filter_by(id=id).first()
#     if wishlist:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": wishlist.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "Wishlist cannot be found for this ID."
#         }
#     ), 404

# edit wishlist in table
# @app.route("/updateWishlist/<int:id>", methods=["PUT"])
# def updateWishlist(id):
#     wishlistItem = Wishlist.query.filter_by(id=id).first()
#     data = request.get_json()
#     if (wishlistItem is None):
#         return jsonify( 
#             {
#                 "code": 404,
#                 "message": "This ID is not found in the database."
#             }
#         )
#     else:
#         wishlistItem.itemName = data['itemName']
#         wishlistItem.remarks = data['remarks']
#         wishlistItem.category = data['category']
#         wishlistItem.itemStatus = data['itemStatus']
#         db.session.add(wishlistItem)
#         db.session.commit()
#         return jsonify(
#             {
#                 "code": 200,
#                 "message": "Wishlist successfully updated."
#             }
#         )


class Matches(db.Model):
    __tablename__ = 'matches'

    matchID = db.Column(db.Integer, primary_key=True, nullable=False)
    reqID = db.Column(db.Integer, nullable=False)
    requestorContactNo = db.Column(db.String(50), nullable=False)
    donorContactNo = db.Column(db.String(50), nullable=False)
    requestedItem = db.Column(db.String(50), nullable=False)
    matchDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, matchID, reqID, requestorContactNo, donorContactNo, requestedItem, matchDate):
        self.matchID = matchID
        self.reqID = reqID
        self.requestorContactNo = requestorContactNo
        self.donorContactNo = donorContactNo
        self.requestedItem = requestedItem
        self.matchDate = matchDate

    def json(self):
        return { "matchID": self.matchID, "reqID": self.reqID, "requestorContactNo": self.requestorContactNo, 
                "donorContactNo": self.donorContactNo, "requestedItem": self.requestedItem, "matchDate": self.matchDate }

# get all successful matches 
@app.route("/getSuccessfulMatches")
def getAllSuccessfulMatches():
    matches = Matches.query.all()
    if len(matches):
        return jsonify(
            {
                "code": 200,
                "data": [match.json() for match in matches], 
                "columnHeaders": Matches.metadata.tables["matches"].columns.keys()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no successful matches at the moment."
        }
    ), 404

# get specific successful match (without matchDate)
@app.route("/getSuccessfulMatches/<matchID>")
def getSuccessfulMatch(matchID):
    match = Matches.query.filter_by(matchID=matchID).first().json()
    match.pop('matchDate')
    if match:
        return jsonify(
            {
                "code": 200,
                "columnHeaders": Matches.metadata.tables["matches"].columns.keys(),
                "data": match
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no successful matches at the moment."
        }
    ), 404

# edit SuccessfulMatch in table
@app.route("/updateSuccessfulMatches/<matchID>", methods=["PUT"])
def updateSuccessfulMatches(matchID):
    match = Matches.query.filter_by(matchID=matchID).first()
    data = request.get_json()
    olddata = data
    if (match is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This matchID is not found in the database."
            }
        )
    else:
        match.matchID = data['matchID']
        match.reqID = data['reqID']
        match.requestorContactNo = data['requestorContactNo']
        match.donorContactNo = data['donorContactNo']
        match.requestedItem = data['requestedItem']
        db.session.add(match)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Match successfully updated.",
                "match": match.json(),
                "data": data,
                "olddata": data
            }
        )



class FormBuilder(db.Model):
    __tablename__ = 'formbuilder'

    fieldID = db.Column(db.Integer, primary_key=True, nullable=False)
    formName = db.Column(db.String(15), nullable=False)
    fieldName = db.Column(db.String(50), nullable=False)
    fieldType = db.Column(db.String(15), nullable=False)
    placeholder = db.Column(db.String(50), nullable=False)
    options = db.Column(db.String(200), nullable=False)

    def __init__(self, fieldID, formName, fieldName, fieldType, placeholder, options):
        self.fieldID = fieldID
        self.formName = formName
        self.fieldType = fieldType
        self.placeholder = placeholder
        self.options = options

    def json(self):
        return { "fieldID": self.fieldID, "formName": self.formName, "fieldName": self.fieldName, "placeholder": self.placeholder, 
                "options": self.options }

# get form fields
@app.route("/getFormFields/<formName>")
def getForms(formName):
    formFields = FormBuilder.query.filter_by(formName=formName)
    fieldNames = {}
    for field in formFields:
        # fieldNames.append(field.fieldName)
        fieldNames[field.fieldID] = field.fieldName
    if (formFields):
        return jsonify( 
            {
                "code": 404,
                "data": fieldNames
            }
        )

class FormAnswers(db.Model):
    __tablename__ = 'formanswers'

    answerID = db.Column(db.Integer, primary_key=True, nullable=False)
    submissionID = db.Column(db.String(30), nullable=False)
    formName = db.Column(db.String(15), nullable=False)
    fieldID = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(50), nullable=False)

    def __init__(self, answerID, submissionID, formName, fieldID, answer):
        self.answerID = answerID
        self.submissionID = submissionID
        self.formName = formName
        self.fieldID = fieldID
        self.answer = answer

    def json(self):
        return { "answerID": self.answerID, "submissionID": self.submissionID, 
                "formName": self.formName, "fieldID": self.fieldID, "answer": self.answer }

class NewWishlist(db.Model):
    __tablename__ = 'newwishlist'

    submissionID = db.Column(db.Integer, nullable=False, primary_key=True)
    migrantID = db.Column(db.Integer, nullable=False)
    itemName = db.Column(db.String(30), nullable=False)
    itemCategory = db.Column(db.String(20), nullable=False)
    timeSubmitted = db.Column(db.DateTime, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)

    def __init__(self, submissionID, migrantID, itemName, itemCategory, timeSubmitted, itemStatus):
        self.submissionID = submissionID
        self.migrantID = migrantID
        self.itemName = itemName
        self.itemCategory = itemCategory
        self.timeSubmitted = timeSubmitted
        self.itemStatus = itemStatus

    def json(self):
        return {"submissionID": self.submissionID, "migrantID": self.migrantID, "itemCategory": self.itemCategory,
                "itemName": self.itemName, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}


# get all form answers for any form
@app.route("/getFormAnswers/<formName>")
def getFormAnswersDonate(formName):
    formFields = FormBuilder.query.filter_by(formName=formName)
    formAnswers = FormAnswers.query.filter_by(formName=formName)
    if formName == "donate":
        tableFields = NewCarousel.metadata.tables["newcarousel"].columns.keys()
    elif formName == "wishlist":
        tableFields = NewWishlist.metadata.tables["newwishlist"].columns.keys()
    fieldNames = {}
    for field in formFields:
        fieldNames[field.fieldID] = field.fieldName
    for field in tableFields:
        fieldNames[len(fieldNames) + 1] = field
    data = []
    row = {}
    submissionID = ""
    for ans in formAnswers:
        if ans.submissionID != submissionID:
            data.append(row)
            submissionID = ans.submissionID
            row["submissionID"] = submissionID
            if formName == "donate":
                submissions = NewCarousel.query.filter_by(submissionID=submissionID)
            elif formName == "wishlist":
                submissions = NewWishlist.query.filter_by(submissionID=submissionID)
            for s in submissions:
                row.update(s.json())
        row[fieldNames[ans.fieldID]] = ans.answer
    if len(data) > 0:
        return jsonify( 
            {
                "code": 200,
                "columnHeaders": fieldNames,
                "data": data
            }
        )
    else:
        return jsonify( 
            {
                "code": 404,
                "message": "No form answers can be found for this form."
            }
        )


# get all form answers for specific forms (carousel & wishlist items) (without timeSubmitted & Item Photo)
@app.route("/getFormAnswers/<formName>/<submissionID>")
def getSpecificFormAnswers(formName, submissionID):
    formAnswers = FormAnswers.query.filter_by(submissionID=submissionID)
    formFields = FormBuilder.query.filter_by(formName=formName)
    if formName == "donate":
        tableFields = NewCarousel.metadata.tables["newcarousel"].columns.keys()
    elif formName == "wishlist":
        tableFields = NewWishlist.metadata.tables["newwishlist"].columns.keys()
    fieldNames = {}
    for field in formFields:
        fieldNames[field.fieldID] = field.fieldName
    for field in tableFields:
        fieldNames[len(fieldNames) + 1] = field
    data = {}
    for ans in formAnswers:
        data["submissionID"] = submissionID
        if fieldNames[ans.fieldID] != "Item Photo":
            data[fieldNames[ans.fieldID]] = ans.answer
        if formName == "donate":
            item = NewCarousel.query.filter_by(submissionID=submissionID).first()
        elif formName == "wishlist":
            item = NewWishlist.query.filter_by(submissionID=submissionID).first()
        data.update(item.json())
        data.pop('timeSubmitted')
    if len(data) > 0:
        return jsonify( 
            {
                "code": 200,
                "columnHeaders": fieldNames,
                "data": data
            }
        )
    else:
        return jsonify( 
            {
                "code": 404,
                "message": "No form answers can be found for this submission ID."
            }
        )

# edit donated (carousel) item OR wishlist in table
@app.route("/updateFormAnswers/<formName>/<submissionID>", methods=["PUT"])
def updateDonatedItem(formName, submissionID):
    formAnswers = FormAnswers.query.filter_by(submissionID=submissionID)
    formFields = FormBuilder.query.filter_by(formName=formName)
    if formName == "donate":
        otherFormFields = NewCarousel.query.filter_by(submissionID=submissionID).first()
    elif formName == "wishlist":
        otherFormFields = NewWishlist.query.filter_by(submissionID=submissionID).first()
    fieldNames = {}
    for field in formFields:
        fieldNames[field.fieldID] = field.fieldName
    data = request.get_json()
    if (formAnswers is None):
        return jsonify( 
            {
                "code": 404,
                "message": "There is no submission for this submission ID in the database."
            }
        )
    else:
        dataDict = {}
        if formName == "donate":
            otherFormFields.carouselID = data["carouselID"]
            otherFormFields.donorID = data["donorID"]
        elif formName == "wishlist":
            otherFormFields.submissionID = data["submissionID"]
            otherFormFields.migrantID = data["migrantID"]
        otherFormFields.submissionID = data["submissionID"]
        otherFormFields.itemName = data["itemName"]
        otherFormFields.itemCategory = data["itemCategory"]
        otherFormFields.itemStatus = data["itemStatus"]
        db.session.add(otherFormFields)
        db.session.commit()
        for d in data:
            dataDict[d] = data[d]
        for ans in formAnswers:
            fieldID = ans.fieldID
            ans.answer = dataDict[str(fieldID)]
            db.session.add(ans)
            db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Data successfully updated.",
                "formAns": [ans.json() for ans in formAnswers],
                "otherFormFields": otherFormFields.json()
            }
        )

# edit uploaded photo
@app.route("/updatePhoto/<submissionID>", methods=['POST'])
def updatePhoto(submissionID):
        formData = request.form
        formDict = formData.to_dict()
        imgFile = request.files['file']
        formField = FormBuilder.query.filter_by(formName="donate").filter_by(fieldName="Item Photo").first()
        fieldID = formField.fieldID
        formAnswer = FormAnswers.query.filter_by(submissionID=submissionID).filter_by(fieldID=fieldID).first()

        # save file
        fileName = secure_filename(imgFile.filename.replace(" ", ""))
        # print(formDict)
        imgFile.save(os.path.join(uploads_dir, fileName))
        # os.open(uploads_dir+secure_filename(fileName), os.O_RDWR | os.O_CREAT, 0o666)
        file = formDict['itemImg']

        # addtodb = CarouselItem(0, itemName, donorAddr, contactNo, category, subCat, quantity, requireDelivery, region, timeSubmitted, "open", file)
        
        try:
            formAnswer.answer = file
            print(formAnswer.answer)
            db.session.add(formAnswer)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Photo Successfully Updated"
                }
            )
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while updating the item photo, please try again later"
                }
            ), 500


# rank migrant workers according to reqHistory, get list of MWs who are prioritised
@app.route("/getRankByReqHistory/<itemID>")
def getRankByReqHistory(itemID):
    requests = Request.query.filter_by(itemID=itemID)
    if requests:
        reqHist = {}
        for req in requests:
            migrantWorkerCount = Matches.query.filter_by(requestorContactNo=req.requestorContactNo).count()
            if migrantWorkerCount in reqHist.keys():
                reqHist[migrantWorkerCount] += [req.requestorContactNo]
            else:
                reqHist[migrantWorkerCount] = [req.requestorContactNo]
        allKeys = reqHist.keys()
        minValue = min(allKeys)
        priorityMW = reqHist[minValue]
        lastItem = {}
        # check for the list of MWs, how long since each of them have gotten an item            
        for mwNum in priorityMW:
            mw = Matches.query.filter_by(contactNo=mwNum).first()
            # if mw.lastItemTime in lastItem.keys():
            #     lastItem[mw.lastItemTime] += [mw.contactNo]
            # else:
            #     lastItem[mw.lastItemTime] = [mw.contactNo]
        allKeys = lastItem.keys()
        minValue = min(allKeys)
        priorityMW = lastItem[minValue]
        return jsonify(
            {
                "code": 200,
                "data": priorityMW
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No migrant workers requested for this item ID."
        }
    ), 404


if __name__ == "__main__":
    app.run(port="5000", debug=True)
