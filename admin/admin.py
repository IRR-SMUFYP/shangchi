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


class NewCarousel(db.Model):
    __tablename__ = 'newcarousel'
    
    donorID = db.Column(db.Integer, primary_key=True)
    carouselID = db.Column(db.String(30), nullable=False)
    itemID = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"donorID": self.donorID, "carouselID": self.carouselID, "itemID": self.itemID, 
                "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

class CategoryItem(db.Model):
    __tablename__ = 'categoryitem'
    
    itemID = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subCat = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"itemID": self.itemID, "itemName": self.itemName, "category": self.category, "subCat": self.subCat}

class NewRequest(db.Model):
    __tablename__ = 'newrequest'

    reqID = db.Column(db.Integer, primary_key=True, nullable=False)
    migrantID = db.Column(db.Integer, nullable=False)
    deliveryLocation = db.Column(db.String(300), nullable=False)
    carouselID = db.Column(db.String(50), nullable=False)
    requestQty = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)

    def __init__(self, reqID, migrantID, deliveryLocation, carouselID, requestQty, timeSubmitted):
        self.reqID = reqID
        self.migrantID = migrantID
        self.deliveryLocation = deliveryLocation
        self.carouselID = carouselID
        self.requestyQty = requestQty
        self.timeSubmitted = timeSubmitted

    def json(self):
        return {"reqID": self.reqID, "migrantID": self.migrantID, "deliveryLocation": self.deliveryLocation, 
                "carouselID": self.carouselID, "requestQty": self.requestQty, "timeSubmitted": self.timeSubmitted}

# get all requests submitted by migrant workers
@app.route("/getRequests")
def getAllRequests():
    requestList = NewRequest.query.all()
    data = []
    for request in requestList:
        row = {}
        carouselID = request.carouselID
        carouselItem = NewCarousel.query.filter_by(carouselID=carouselID).first()
        itemID = carouselItem.itemID
        itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
        row["itemName"] = itemName
        row.update(carouselItem.json())
        row.update(request.json())
        row.pop('itemID')
        row.pop('carouselID')
        data.append(row)
    columns = list(data[0].keys())
    if len(requestList):
        return jsonify(
            {
                "code": 200,
                "columnHeaders": columns,
                "data": data
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no requests at the moment."
        }
    ), 404

# get specific request by reqID
@app.route("/getRequests/<reqID>")
def getRequestByID(reqID):
    request = NewRequest.query.filter_by(reqID=reqID).first()
    carouselID = request.carouselID
    carouselItem = NewCarousel.query.filter_by(carouselID=carouselID).first()
    itemID = carouselItem.itemID
    itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
    data = {}
    data["itemName"] = itemName
    data.update(request.json())
    data.update(carouselItem.json())
    data.pop("itemID")
    data.pop("carouselID")
    fieldNames = {}
    columns = sorted(list(data.keys()))
    for i in range(len(columns)):
        fieldNames[i] = columns[i]
    if request:
        return jsonify(
            {
                "code": 200,
                "columnHeaders": fieldNames,
                "data": data
                # "columnHeaders": NewRequest.metadata.tables["newrequest"].columns.keys(),
                # "data": request
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Request cannot be found for this ID."
        }
    ), 404

# get requests submitted for specific item
# @app.route("/getRequestsByItem/<reqID>")
# def getRequestByItemID(reqID):
#     requests = NewRequest.query.filter_by(reqID=reqID)
#     if requests:
#         return jsonify(
#             {
#                 "code": 200,
#                 "columnHeaders": NewRequest.metadata.tables["newrequest"].columns.keys(),
#                 "data": [request.json() for request in requests]
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "Requests cannot be found for this item ID."
#         }
#     ), 404

# edit request in table
@app.route("/updateRequest/<reqID>", methods=["PUT"])
def updateRequest(reqID):
    requested = NewRequest.query.filter_by(reqID=reqID).first()
    data = request.get_json()
    if (requested is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This reqID is not found in the database."
            }
        )
    else:
        requested.deliveryLocation = data['deliveryLocation']
        requested.requestQty = data['requestQty']
        requested.migrantID = data['migrantID']
        db.session.add(requested)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Request successfully updated."
            }
        )

class Matches(db.Model):
    __tablename__ = 'matches'

    matchID = db.Column(db.Integer, primary_key=True, nullable=False)
    reqID = db.Column(db.Integer, nullable=False)
    migrantID = db.Column(db.Integer, nullable=False)
    donorID = db.Column(db.Integer, nullable=False)
    matchDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, matchID, reqID, migrantID, donorID, matchDate):
        self.matchID = matchID
        self.reqID = reqID
        self.migrantID = migrantID
        self.donorID = donorID
        self.matchDate = matchDate

    def json(self):
        return { "matchID": self.matchID, "reqID": self.reqID, "migrantID": self.migrantID, 
                "donorID": self.donorID, "matchDate": self.matchDate }

# get all successful matches 
@app.route("/getSuccessfulMatches")
def getAllSuccessfulMatches():
    matches = Matches.query.all()
    data = []
    for match in matches:
        row = {}
        reqID = match.reqID
        request = NewRequest.query.filter_by(reqID=reqID).first()
        carouselID = request.carouselID
        carouselItem = NewCarousel.query.filter_by(carouselID=carouselID).first()
        itemID = carouselItem.itemID
        itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
        row["itemName"] = itemName
        row.update(match.json())
        row.update(request.json())
        row.update(carouselItem.json())
        row.pop('carouselID')
        row.pop('reqID')
        row.pop('itemID')
        data.append(row)
    columns = list(data[0].keys())
    if len(matches):
        return jsonify(
            {
                "code": 200,
                "columnHeaders": columns,
                "data": data
                # "data": [match.json() for match in matches], 
                # "columnHeaders": Matches.metadata.tables["matches"].columns.keys()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no successful matches at the moment."
        }
    ), 404

# get specific successful match 
@app.route("/getSuccessfulMatches/<matchID>")
def getSuccessfulMatch(matchID):
    data = {}
    match = Matches.query.filter_by(matchID=matchID).first()
    reqID = match.reqID
    request = NewRequest.query.filter_by(reqID=reqID).first()
    carouselID = request.carouselID
    carouselItem = NewCarousel.query.filter_by(carouselID=carouselID).first()
    itemID = carouselItem.itemID
    itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
    data = {}
    data["itemName"] = itemName
    data.update(request.json())
    data.update(carouselItem.json())
    data.pop("itemID")
    data.pop("carouselID")
    data.pop("reqID")
    columns = list(data.keys())
    if match:
        return jsonify(
            {
                "code": 200,
                "columnHeaders": columns,
                "data": data
                # "columnHeaders": Matches.metadata.tables["matches"].columns.keys(),
                # "data": match
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
    reqID = match.reqID
    req = NewRequest.query.filter_by(reqID=reqID).first()
    carouselID = req.carouselID
    carouselItem = NewCarousel.query.filter_by(carouselID=carouselID).first()
    data = request.get_json()
    print(data)
    if (match is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This matchID is not found in the database."
            }
        )
    else:
        match.donorID = data['donorID']
        db.session.add(match)
        db.session.commit()
        req.deliveryLocation = data['deliveryLocation']
        req.requestQty = data['requestQty']
        db.session.add(req)
        db.session.commit()
        carouselItem.itemStatus = data['itemStatus']
        carouselItem.donorID = data['donorID']
        db.session.add(carouselItem)
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

    wishlistID = db.Column(db.Integer, nullable=False, primary_key=True)
    migrantID = db.Column(db.Integer, nullable=False)
    itemID = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.DateTime, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)

    def __init__(self, wishlistID, migrantID, itemID, timeSubmitted, itemStatus):
        self.wishlistID = wishlistID
        self.migrantID = migrantID
        self.itemID = itemID
        self.timeSubmitted = timeSubmitted
        self.itemStatus = itemStatus

    def json(self):
        return {"wishlistID": self.wishlistID, "migrantID": self.migrantID, "itemID": self.itemID,
                "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}


# get all form answers for any form
@app.route("/getFormAnswers/<formName>")
def getFormAnswers(formName):
    formFields = FormBuilder.query.filter_by(formName=formName)
    if formName == "carousel":
        tableFields = NewCarousel.metadata.tables["newcarousel"].columns.keys()
    elif formName == "wishlist":
        tableFields = NewWishlist.metadata.tables["newwishlist"].columns.keys()
    fieldNames = {}
    for field in formFields:
        fieldNames[field.fieldID] = field.fieldName
    for field in tableFields:
        if field == "itemID":
            fieldNames[len(fieldNames) + 1] = "itemName"
        else:
            fieldNames[len(fieldNames) + 1] = field
    data = []
    if formName == "carousel":
        submissionIDList = NewCarousel.query.with_entities(NewCarousel.carouselID).distinct()
    elif formName == "wishlist":
        submissionIDList = NewWishlist.query.with_entities(NewWishlist.wishlistID).distinct()
    for subID in submissionIDList:
        row = {}
        if formName == "carousel":
            submission = NewCarousel.query.filter_by(carouselID=subID[0]).first().json()
        elif formName == "wishlist":
            submission = NewWishlist.query.filter_by(wishlistID=subID[0]).first().json()
        itemID = submission['itemID']
        row["itemName"] = CategoryItem.query.filter_by(itemID=itemID).first().itemName
        row.update(submission)
        row.pop("itemID")
        formAnswers = FormAnswers.query.filter_by(formName=formName).filter_by(submissionID=subID[0])
        for ans in formAnswers:
            row[fieldNames[ans.fieldID]] = ans.answer
        data.append(row)
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


# get all form answers for specific forms (carousel & wishlist items)
@app.route("/getFormAnswers/<formName>/<submissionID>")
def getSpecificFormAnswers(formName, submissionID):
    formAnswers = FormAnswers.query.filter_by(submissionID=submissionID)
    formFields = FormBuilder.query.filter_by(formName=formName)
    if formName == "carousel":
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
        data[fieldNames[ans.fieldID]] = ans.answer
        if formName == "carousel":
            item = NewCarousel.query.filter_by(carouselID=submissionID).first()
        elif formName == "wishlist":
            item = NewWishlist.query.filter_by(wishlistID=submissionID).first()
        data.update(item.json())
        # data.pop('itemName')
    # data.pop('timeSubmitted')
    # data.pop('itemID')
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
    if formName == "carousel":
        otherFormFields = NewCarousel.query.filter_by(carouselID=submissionID).first()
    elif formName == "wishlist":
        otherFormFields = NewWishlist.query.filter_by(wishlistID=submissionID).first()
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
        if formName == "carousel":
            otherFormFields.donorID = data["donorID"]
            otherFormFields.carouselID = data["carouselID"]
        elif formName == "wishlist":
            otherFormFields.wishlistID = data["wishlistID"]
            otherFormFields.migrantID = data["migrantID"]
        # otherFormFields.submissionID = data["submissionID"]
        # otherFormFields.itemName = data["itemName"]
        # otherFormFields.itemCategory = data["itemCategory"]
        otherFormFields.itemStatus = data["itemStatus"]
        db.session.add(otherFormFields)
        db.session.commit()
        for d in data:
            dataDict[d] = data[d]
        for ans in formAnswers:
            if ans.fieldID != 4:
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
        formField = FormBuilder.query.filter_by(formName="carousel").filter_by(fieldName="Item Photo").first()
        fieldID = formField.fieldID
        formAnswer = FormAnswers.query.filter_by(submissionID=submissionID).filter_by(fieldID=fieldID).first()
        # save file
        fileName = secure_filename(imgFile.filename.replace(" ", ""))
        # print(formDict)
        imgFile.save(os.path.join(uploads_dir, fileName))
        # os.open(uploads_dir+secure_filename(fileName), os.O_RDWR | os.O_CREAT, 0o666)
        file = formDict['itemImg']

        # delete old photo file
        oldFile = formAnswer.answer
        os.remove(os.path.join(uploads_dir, oldFile))
        
        try:
            formAnswer.answer = file
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
@app.route("/getRankByReqHistory/<carouselID>")
def getRankByReqHistory(carouselID):
    requests = NewRequest.query.filter_by(carouselID=carouselID)
    if requests:
        reqHist = {}
        for req in requests:
            migrantWorkerCount = Matches.query.filter_by(migrantID=req.migrantID).count()
            if migrantWorkerCount in reqHist.keys():
                reqHist[migrantWorkerCount] += [req.migrantID]
            else:
                reqHist[migrantWorkerCount] = [req.migrantID]
        allKeys = reqHist.keys()
        minValue = min(allKeys, default="EMPTY")
        priorityMW = reqHist[minValue]
        mwPoints = {}
        # check whether item requires delivery
        deliveryFieldID = FormBuilder.query.filter_by(fieldName="Delivery Method").first()
        deliveryOption = FormAnswers.query.filter_by(submissionID=carouselID).filter_by(fieldID=deliveryFieldID).first()
        # if deliveryOption == "Self Pick-Up":
            # find migrant worker(s) w shortest distance 
        
        # else: 
        # check for the list of MWs, how long since each of them have gotten an item
        # i only wrote down the logic... the code below doesn't work yet HAHAHA
        if minValue != 0:      
            timeNow = datetime.now()
            for mwNum in priorityMW:
                mw = Matches.query.filter_by(migrantID=mwNum).first()
                lastItemTime = mw.matchDate
                days = timeNow - lastItemTime # convert difference into no. of days
                if 0 <= days < 14:
                    mwPoints[mwNum] = 0
                elif 14 <= days < 28:
                    mwPoints[mwNum] = 1
                elif 28 <= days < 42:
                    mwPoints[mwNum] = 2
                elif 42 <= days < 56:
                    mwPoints[mwNum] = 4
                else:
                    mwPoints[mwNum] = 6
            # if mw.lastItemTime in lastItem.keys():
            #     lastItem[mw.lastItemTime] += [mw.contactNo]
            # else:
            #     lastItem[mw.lastItemTime] = [mw.contactNo]
        # allKeys = lastItem.keys()
        # minValue = min(allKeys)
        # priorityMW = lastItem[minValue]
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
