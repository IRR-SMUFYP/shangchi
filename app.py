from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sklearn import random_projection
from sqlalchemy.orm import load_only
from flask_cors import CORS
from datetime import datetime
import xlsxwriter
import os
from os import environ
from werkzeug.utils import secure_filename
import bcrypt
import random
import requests
import json
import config
import uuid
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/imatch'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

uploads_dir = os.path.join('assets/img/donations')

db = SQLAlchemy(app)
CORS(app)

# region MODELS
class User(db.Model):
    __tablename__ = 'user'
    
    username = db.Column(db.Integer, primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    userType = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password, userType):
        self.username = username
        self.password = password
        self.userType = userType

    def json(self):
        return {"username": self.username, "password": self.password, "userType": self.userType}

class FormBuilder(db.Model):
    __tablename__ = 'formbuilder'

    fieldID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    formName = db.Column(db.String(15), nullable=False)
    fieldName = db.Column(db.String(50), nullable=False)
    fieldType = db.Column(db.String(15), nullable=False)
    placeholder = db.Column(db.String(50))
    options = db.Column(db.String(200))


    def json(self):
        return {"fieldID": self.fieldID, "formName": self.formName, "fieldName": self.fieldName, "fieldType": self.fieldType, "placeholder": self.placeholder, "options": self.options}

class CategoryItem(db.Model):
    __tablename__ = 'categoryitem'

    itemID = db.Column(db.Integer, nullable=False, primary_key=True)
    itemName = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    subCat = db.Column(db.String, nullable=False)


    def json(self):
        return {"itemID": self.itemID, "itemName": self.itemName, "category": self.category, "subCat": self.subCat}

class Donation(db.Model):
    __tablename__ = 'donation'
    
    donorID = db.Column(db.Integer)
    donationID = db.Column(db.String(30), nullable=False, primary_key=True)
    itemID = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"donorID": self.donorID, "donationID": self.donationID, "itemID": self.itemID, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    
    migrantID = db.Column(db.Integer)
    wishlistID = db.Column(db.String(30), nullable=False, primary_key=True)
    itemID = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"wishlistID": self.wishlistID, "migrantID": self.migrantID, "wishlistID": self.wishlistID, "itemID": self.itemID, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

class FormAnswers(db.Model):
    __tablename__ = 'formanswers'

    answerID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    submissionID = db.Column(db.String(30), nullable=False)
    # , db.ForeignKey(Learner.empID)
    formName = db.Column(db.String(15), nullable=False)
    fieldID = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(50), nullable=False)

    def json(self):
        return {"answerID": self.answerID, "submissionID": self.submissionID, "fieldID": self.fieldID, "formName": self.formName, "answer": self.answer}

class Request(db.Model):
    __tablename__ = 'request'
    
    reqID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    migrantID = db.Column(db.Integer, nullable=False)           #, ForeignKey('user.username')
    postalCode = db.Column(db.String(6), nullable=False)
    donationID = db.Column(db.String(30), nullable=False)       #, ForeignKey('donation.id')
    timeSubmitted = db.Column(db.Date, nullable=False)
        
    def json(self):
        return {"reqID": self.reqID, "migrantID": self.migrantID, "postalCode": self.postalCode, "donationID": self.donationID, "timeSubmitted": self.timeSubmitted}

class Matches(db.Model):
    __tablename__ = 'matches'

    matchID = db.Column(db.Integer, primary_key=True, nullable=False)
    reqID = db.Column(db.Integer, nullable=False)
    migrantID = db.Column(db.Integer, nullable=False)
    donorID = db.Column(db.Integer, nullable=False)
    matchDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def json(self):
        return { "matchID": self.matchID, "reqID": self.reqID, "migrantID": self.migrantID, 
                "donorID": self.donorID, "matchDate": self.matchDate }

class Delivery(db.Model):
    __tablename__ = 'delivery'

    matchID = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    driverID = db.Column(db.Integer, nullable=False)

    def json(self):
        return { "matchID": self.matchID, "status": self.status, "driverID": self.driverID }

class Faq(db.Model):
    __tablename__ = 'faq'

    faqID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.String(300), nullable=False)
    section = db.Column(db.String(10), nullable=False)

    def __init__(self, faqID, question, answer, section):
        self.faqID = faqID
        self.question = question
        self.answer = answer
        self.section = section

    def json(self):
        return {"faqID": self.faqID, "question": self.question, "answer": self.answer, "section": self.section}

#endregion


# region USER
# get user by username
@app.route("/getUser/<username>")
def getUser(username):
    user = User.query.filter_by(username=username).first()
    columnHeaders = User.metadata.tables["user"].columns.keys()
    return jsonify(
        {
        "code": 200,
        "columnHeaders": columnHeaders,
        "data": user.json()
    })

# get All Users
@app.route("/getAllUsers")
def getAllUsers():
    users = User.query.all()
    columnHeaders = User.metadata.tables["user"].columns.keys()
    return jsonify(
        {
        "code": 200,
        "columnHeaders": columnHeaders,
        "data": [user.json() for user in users]
    })

# Register MW 
@app.route("/registermw", methods=['POST'])
def registerMW():
        formData = request.form
        formDict = formData.to_dict()
        username = formDict['userName']
        pw = formDict['pw']
        hashedpw = bcrypt.hashpw(str(pw).encode('utf-8'), bcrypt.gensalt())

        addtodb = User(username, hashedpw, "worker")
        
        try:
            db.session.add(addtodb)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Worker account for " + username + " successfully created!"
                }
            )
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while registering user :" + str(e)
                }
            ), 500

# Register admin account
@app.route("/registeradmin", methods=['POST'])
def registerAdmin():
        formData = request.form
        formDict = formData.to_dict()
        username = formDict['userName']
        pw = formDict['pw']
        hashedpw = bcrypt.hashpw(str(pw).encode('utf-8'), bcrypt.gensalt())

        addtodb = User(username, hashedpw, "admin")
        
        try:
            db.session.add(addtodb)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Admin account for " + username + " successfully created!"
                }
            )
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while registering user :" + str(e)
                }
            ), 500

# Register Driver Account
@app.route("/registerDriver", methods=['POST'])
def registerDriver():
        formData = request.form
        formDict = formData.to_dict()
        username = formDict['userName']
        pw = formDict['pw']
        hashedpw = bcrypt.hashpw(str(pw).encode('utf-8'), bcrypt.gensalt())

        addtodb = User(username, hashedpw, "driver")
        
        try:
            db.session.add(addtodb)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Driver account for " + username + " successfully created!"
                }
            )
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while registering user :" + str(e)
                }
            ), 500


# edit Account in table
@app.route("/updateUser/<username>", methods=["PUT"])
def updateAccountInfo(username):
    user = User.query.filter_by(username=username).first()
    data = request.get_json()
    # print(data)
    if (user is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This username is not found in the database."
            }
        )
    else:
        user.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user.userType = data['userType']
        db.session.add(user)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Account info updated successfully.",
                "user": user.json(),
            }
        )

# delete account by username
@app.route("/deleteUser/<username>", methods=["DELETE"])
def deleteUser(username):
    user = User.query.filter_by(username=username).first()
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify (
            {
                "code": 200,
                "message": "Row deleted successfully!"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while deleting the data, please try again later"
            }
        ), 500

# Login function to check if user exists and if password is correct
@app.route("/login", methods=['POST'])
def checkLogin():
    formData = request.form
    formDict = formData.to_dict()
    uName = formDict["username"]
    pw = formDict["password"]

    user = User.query.filter_by(username=uName).first()
    if (user != None):
        if (bcrypt.checkpw(str(pw).encode('utf-8'), str(user.password).encode('utf-8'))):

            print("Password checks out, user", user.username, "logged in at ", datetime.now())

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "message": "Authentication success!",
                        "userType": user.json()
                    }
                }
            )
        elif (user.password != pw):
            return jsonify(
                {
                    "code": 401,
                    "message": "Password is incorrect"
                }
            )
    else:
        return jsonify(
            {
                "code": 404,
                "message": "User not found, please register and try again."
            }
        )
# endregion

# region FORMBUILDER
# get all fields by form
@app.route("/formbuilder/<string:formName>")
def getFieldsByForm(formName):
    fieldlist = FormBuilder.query.filter_by(formName=formName).all()
    if len(fieldlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [field.json() for field in fieldlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no fields for the current form."
        }
    ), 404

# get specific field
@app.route("/formbuilder/<int:fieldID>")
def getField(fieldID):
    field = FormBuilder.query.filter_by(fieldID=fieldID).first()
    if field:
        return jsonify(
            {
                "code": 200,
                "data":  field.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No field was found."
        }
    ), 404

# create new field
@app.route('/formbuilder', methods=['POST'])
def createField():
    data = request.get_json()
    item = FormBuilder(**data)
    if ( request.get_json() is not None ): 
        try:
            db.session.add(item)
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# edit existing field
@app.route('/formbuilder/<int:fieldID>', methods=['POST'])
def edit_field(fieldID):
    data = request.get_json()
    item = FormBuilder.query.filter_by(fieldID=fieldID).first()
    if ( item is not None ): 
        try:
            item.fieldName = data['fieldName']
            item.fieldType = data['fieldType']
            if 'placeholder' in data:
                item.placeholder = data['placeholder']
            if 'options' in data:
                item.options = data['options']
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# delete existing field
@app.route('/formbuilder/<int:fieldID>', methods=["DELETE"])
def delete_field(fieldID):
    item = FormBuilder.query.filter_by(fieldID=fieldID).first()
    ansList = FormAnswers.query.filter_by(fieldID=fieldID).all()
    if ( item is not None ): 
        try:
            # delete answers linked to field
            for ans in ansList:
                db.session.delete(ans)

            # delete field
            db.session.delete(item)
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception as e:
            print(e)
            return jsonify({
                "message": "Unable to commit to database."
            }), 500
#endregion

# region CATEGORYITEMS
@app.route("/getCatalog")
def retrieveCatalog():
    catalog = CategoryItem.query.all()
    
    if (catalog):
        return jsonify(
            {
                "code": 200,
                "items": [catalogitem.json() for catalogitem in catalog]
            }
        )
    else:
        return jsonify(
            {
                "code": 404,
                "message": "Catalog seems to be empty or the API file is not running"
            }
        )

# get all existing categories to be displayed in drop down fields
@app.route("/getCat")
def getAllCat():
    categoryList = CategoryItem.query.with_entities(
        CategoryItem.category).distinct()
    # print(categoryList)
    if (categoryList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    # No need for .json() because you are returning just one column's data
                    "categories": [category for category in categoryList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Please make sure the py file is being run to see category list"
        }
    ), 404

# get all existing subcategories to be displayed in drop down fields
@app.route("/getSubCat/<cat>")
def getSubCat(cat):
    subCats = CategoryItem.query.filter_by(category=cat)
    
    if (subCats):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "subcats": [subcat.json() for subcat in subCats]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Error retrieving Subcatogories."
        }
    ), 404

@app.route("/getItemNames/<cat>/<subcat>")
def getItemNames(cat, subcat):
    itemsInCategory = CategoryItem.query.filter_by(category=cat).filter_by(subCat=subcat).all()
    # print(itemsInCategory)

    if (itemsInCategory):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "itemsInCat": [item.json() for item in itemsInCategory]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Error retreiving Items in Subcategories."
        }
    ), 404

@app.route("/getItemById/<int:itemID>")
def getItem(itemID):
    item = CategoryItem.query.filter_by(itemID=itemID).first()
    if item:
        return jsonify(
            {
                "code": 200,
                "data": item.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No item was found."
        }
    ), 404
#endregion

# region FORMANSWERS + DONATION/WISHLIST
# get all form answers by donation/wishlist submission
def getFormAnswersBySubmission(submissionID):
    answerlist = FormAnswers.query.filter_by(submissionID=submissionID).all()

    # map answers to field names
    mappedAnswerlist = {}
    for answer in answerlist:
        field = FormBuilder.query.filter_by(fieldID=answer.fieldID).options(load_only('fieldName')).first()
        mappedAnswerlist[field.fieldName] = answer.answer
    
    return mappedAnswerlist

# get all details of a donation/wishlist submission
@app.route("/formanswers/<string:submissionID>")
def getAllDetailsBySubmission(submissionID):
    # check if submission from Donation or wishlist
    submission = Donation.query.filter_by(donationID=submissionID).first()
    if submission is None:
        submission = Wishlist.query.filter_by(wishlistID=submissionID).first()

    if submission is not None:
        formAnswersList = getFormAnswersBySubmission(submissionID)

        return jsonify(
            {
                "code": 200,
                "data": dict(**submission.json(), **formAnswersList)
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No submission was found."
        }
    ), 404

# Global UUID Name stored for future use
uuidGeneratedName = ""
fileExtension = ""

# create new submission
@app.route('/formanswers', methods=['POST'])
def createSubmission():
    try:
        formData = request.form
        formDict = formData.to_dict()
        print(formData)
        print(formDict)
        
        if '' in formDict.values():
            return jsonify({
                "message": "Please fill in missing form fields!"
            }), 400

        files = request.files
        userid = formDict['contactNo']
        formName =  formDict['formName']
        itemID = formDict['itemName']

        # calculate submissionID (datetime userID)
        now = datetime.now()
        currentDT = now.strftime("%Y-%m-%d %H:%M:%S")
        submissionID = currentDT + " " + userid

        # file uploading
        for fileId in files:
            file = files[fileId]
            formDict[fileId] = file.filename
            # save file
            # fileName = secure_filename(file.filename)
            # fileName = secure_filename(file.filename.replace(" ", ""))
            fileName = secure_filename(file.filename)
            index = fileName.index('.')
            fileExtension = fileName[index:]
            uuidGeneratedName = uuid.uuid4()
            file.save(os.path.join(uploads_dir, str(uuidGeneratedName) + str(fileExtension)))
    except Exception as e:
        print(e)
        return jsonify({
                "message": "Please fill in missing form fields!"
            }), 400

    # for answer in formDict:
    #     print(type(answer))
    #     print(answer + ": " +formDict[answer])

    # submit into donation/wishlist
    details = {"itemID": itemID, "timeSubmitted": currentDT, "itemStatus": "Available"}
    if formName == "wishlist":
        details["migrantID"] = userid
        details["wishlistID"] = submissionID
        submission = Wishlist(**details)
        try:
            db.session.add(submission)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({
                "message": "Unable to submit request to database.",
                "data" : submission.json()
            }), 500
    elif formName == "donation":
        details["donorID"] = userid
        details["donationID"] = submissionID
        submission = Donation(**details)
        try:
                db.session.add(submission)
                db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({
                "message": "Unable to submit donation to database.",
                "data" : submission.json()
            }), 500
    print(formDict)
    # formDict['3'] = formDict['3'].replace(" ", "")
    formDict['3'] = str(uuidGeneratedName) + str(fileExtension)

    # submit into formAnswers
    for id in formDict:
        print(id, formDict[id])
        answer = {"submissionID": submissionID, "formName": formName, "fieldID": id, "answer": formDict[id]}
        item = FormAnswers(**answer)
        if ( id.isdigit() ): 
            try:
                db.session.add(item)
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({
                    "message": "Unable to submit form answers to database.",
                    "data" : item.json()
                }), 500
    
    return jsonify({
                    "message": "Form submitted successfully."
                }), 201

# get all form answers for any form
@app.route("/getFormAnswers/<formName>")
def getFormAnswers(formName):
    formFields = FormBuilder.query.filter_by(formName=formName)
    if formName == "donation":
        tableFields = Donation.metadata.tables["donation"].columns.keys()
    elif formName == "wishlist":
        tableFields = Wishlist.metadata.tables["wishlist"].columns.keys()
    fieldNames = {}
    for field in formFields:
        fieldNames[field.fieldID] = field.fieldName
    for field in tableFields:
        lastKey = list(fieldNames.keys())[-1]
        if field == "itemID":
            fieldNames[lastKey + 1] = "itemName"
        else:
            fieldNames[lastKey + 1] = field
    data = []
    if formName == "donation":
        submissionIDList = Donation.query.with_entities(Donation.donationID).distinct()
    elif formName == "wishlist":
        submissionIDList = Wishlist.query.with_entities(Wishlist.wishlistID).distinct()
    for subID in submissionIDList:
        row = {}
        if formName == "donation":
            submission = Donation.query.filter_by(donationID=subID[0]).first().json()
        elif formName == "wishlist":
            submission = Wishlist.query.filter_by(wishlistID=subID[0]).first().json()
        row.update(submission)
        itemID = row['itemID']
        row["itemName"] = CategoryItem.query.filter_by(itemID=itemID).first().itemName
        row.pop("itemID")
        formAnswers = FormAnswers.query.filter_by(formName=formName).filter_by(submissionID=subID[0])
        ansFields = []
        for ans in formAnswers:
            ansFields.append(ans.fieldID)
            row[fieldNames[ans.fieldID]] = ans.answer
        if len(ansFields) < len(fieldNames):
            remainder = len(fieldNames) - len(ansFields)
            fieldIDList = list(fieldNames.keys())
            for i in range(1, remainder + 1):
                if fieldNames[fieldIDList[-i]] not in row.keys():
                    row[fieldNames[fieldIDList[-i]]] = ""
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

# get all form answers for specific forms (donation & wishlist items)
@app.route("/getFormAnswers/<formName>/<submissionID>")
def getSpecificFormAnswers(formName, submissionID):
    formAnswers = FormAnswers.query.filter_by(submissionID=submissionID)
    formFields = FormBuilder.query.filter_by(formName=formName)
    if formName == "donation":
        tableFields = Donation.metadata.tables["donation"].columns.keys()
    elif formName == "wishlist":
        tableFields = Wishlist.metadata.tables["wishlist"].columns.keys()
    fieldNames = {}
    for field in formFields:
        fieldNames[field.fieldID] = field.fieldName
    for field in tableFields:
        fieldNames[len(fieldNames) + 1] = field
    data = {}
    for ans in formAnswers:
        data["submissionID"] = submissionID
        data[fieldNames[ans.fieldID]] = ans.answer
        if formName == "donation":
            item = Donation.query.filter_by(donationID=submissionID).first()
        elif formName == "wishlist":
            item = Wishlist.query.filter_by(wishlistID=submissionID).first()
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

# edit donated (donation) item OR wishlist in table
@app.route("/updateFormAnswers/<formName>/<submissionID>", methods=["PUT"])
def updateFormAnswers(formName, submissionID):
    formAnswers = FormAnswers.query.filter_by(submissionID=submissionID)
    formFields = FormBuilder.query.filter_by(formName=formName)
    if formName == "donation":
        otherFormFields = Donation.query.filter_by(donationID=submissionID).first()
    elif formName == "wishlist":
        otherFormFields = Wishlist.query.filter_by(wishlistID=submissionID).first()
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
        if formName == "donation":
            otherFormFields.donorID = data["donorID"]
            otherFormFields.donationID = data["donationID"]
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
            if d not in ["donorID", "donationID", "wishlistID", "migrantID", "itemStatus"]:
                dataDict[d] = data[d]
        for ans in formAnswers:
            fieldName = FormBuilder.query.filter_by(fieldID=ans.fieldID).first().fieldName
            if ans.fieldID != 3:
                fieldName = FormBuilder.query.filter_by(fieldID=ans.fieldID).first().fieldName
                ans.answer = dataDict[fieldName]
                dataDict.pop(fieldName)
                db.session.add(ans)
                db.session.commit()
        for data in dataDict:
            if data.isdigit() == False:
                answer = {"submissionID": submissionID, "formName": formName, "fieldID": FormBuilder.query.filter_by(fieldName=data).first().fieldID, "answer": dataDict[data]}
                answer = FormAnswers(**answer)
                db.session.add(answer)
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
    formField = FormBuilder.query.filter_by(formName="donation").filter_by(fieldName="Item Photo").first()
    fieldID = formField.fieldID
    formAnswer = FormAnswers.query.filter_by(submissionID=submissionID).filter_by(fieldID=fieldID).first()
    # save file
    # fileName = secure_filename(imgFile.filename.replace(" ", ""))

    # Added lines to test uuid filename
    fileName = secure_filename(file.filename)
    index = fileName.index('.')
    fileExtension = fileName[index:]
    uuidGeneratedName = uuid.uuid4()
    file.save(os.path.join(uploads_dir, str(uuidGeneratedName) + str(fileExtension)))
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

# delete formAnswers + donation/wishlist
@app.route("/deleteRow/<formName>/<submissionID>", methods=["DELETE"])
def deleteRow(formName, submissionID):
    if formName == "donation":
        row = Donation.query.filter_by(donationID=submissionID).first()
        oldFile = FormAnswers.query.filter_by(submissionID=submissionID).filter_by(fieldID=3).first().answer
        print(oldFile)
    elif formName == "wishlist":
        row = Wishlist.query.filter_by(wishlistID=submissionID).first()
    formAnswers = FormAnswers.query.filter_by(submissionID=submissionID)
    try:
        db.session.delete(row)
        db.session.commit()
        for ans in formAnswers:
            db.session.delete(ans)
            db.session.commit()
        if formName == "donation":
            os.remove(os.path.join(uploads_dir, oldFile))
        return jsonify (
            {
                "code": 200,
                "message": "Row deleted successfully!"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while deleting the data, please try again later"
            }
        ), 500


# endregion

# region DONATION
# get all donation items
@app.route("/donation")
def getAllDonationItems():
    donationList = Donation.query.all()
    if len(donationList):
        itemList = []
        for donationItem in donationList:
            item = donationItem.json()
            formAnswers = getFormAnswersBySubmission(item["donationID"])
            itemDetails = getItem(item["itemID"]).get_json()["data"]
            itemDetails.pop("itemID")   # remove duplicate itemID

            itemList.append(dict(**item, **formAnswers, **itemDetails))
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": itemList
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no donations at the moment."
        }
    ), 404

# get specified donation item
@app.route("/donation/<string:donationID>")
def getDonationItem(donationID):
    donationItem = Donation.query.filter_by(donationID=donationID).first()
    if donationItem:
        formAnswers = getFormAnswersBySubmission(donationItem.donationID)
        itemDetails = getItem(donationItem.itemID).get_json()["data"]
        itemDetails.pop("itemID")   # remove duplicate itemID

        return jsonify(
            {
                "code": 200,
                "data": dict(**donationItem.json(), **formAnswers, **itemDetails)
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Donation does not exist."
        }
    ), 404

# API for search function
@app.route("/getItemsByCat/<string:cat>")
def getItemsByCategory(cat):
    catList = CategoryItem.query.filter_by(category=cat).all()
    catItemList = []
    for category in catList:
        itemList = Donation.query.filter_by(itemID=category.itemID).all()
        if (len(itemList)):
            categorydict = category.json()
            categorydict.pop("itemID")
            catList = [dict(**item.json(),**categorydict) for item in itemList]
            catItemList.extend(catList)
    if len(itemList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "itemsByCat": catItemList
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items listed under this category."
        }
    ), 404

@app.route("/getItemsBySubCat/<cat>/<subcat>")
def filterItems(cat, subcat):
    subcatList = CategoryItem.query.filter_by(category=cat).filter_by(subCat=subcat).all()
    subcatItemList = []
    for category in subcatList:
        itemList = Donation.query.filter_by(itemID=category.itemID).all()
        if (len(itemList)):
            categorydict = category.json()
            categorydict.pop("itemID")
            subcatDetailsList = []
            for item in itemList:
                formAns = getFormAnswersBySubmission(item.donationID)
                subcatDetailsList.append(dict(**item.json(),**categorydict, **formAns))
            subcatItemList.extend(subcatDetailsList)
    if (len(subcatItemList)):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": subcatItemList
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items donated under this Sub-category"
        }
    ), 404
    
# endregion

# region WISHLIST
# get all items in wishlist
@app.route("/wishlist")
def getAllWishListItems():
    wishList = Wishlist.query.all()
    if len(wishList):
        itemList = []
        for wishlistItem in wishList:
            item = wishlistItem.json()
            formAnswers = getFormAnswersBySubmission(item["wishlistID"])
            itemDetails = getItem(item["itemID"]).get_json()["data"]
            itemDetails.pop("itemID")   # remove duplicate itemID

            itemList.append(dict(**item, **formAnswers, **itemDetails))
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": itemList
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Wishlist is currently empty."
        }
    ), 404
# endregion

# region REQUEST
@app.route("/request/<string:contactNo>")
def getMwRequest(contactNo):
    itemReqList = Donation.query\
        .join(Request, Request.donationID==Donation.donationID)\
            .filter(Request.donationID==Donation.donationID)\
                .filter(Request.migrantID==contactNo)\
                    .distinct()

    itemIdArr = [id.json()['donationID'] for id in itemReqList]
    
    return jsonify(
        {
            "code": 200,
            "requestedItemIds": itemIdArr
        }
    )

@app.route("/request/excel")
def exportToExcel():
    itemReqList = Request.query.join(Donation, Request.donationID==Donation.donationID).join(CategoryItem, Donation.itemID==CategoryItem.itemID)\
                    .add_columns(Request.timeSubmitted,CategoryItem.category,CategoryItem.subCat,CategoryItem.itemName,Request.postalCode).distinct()

    postalCodeArea = {
        "North": [str(x) for x in (list(range(65,74)) + list(range(75,81)))],   # 65-80 exc.74
        "South": ['09', '10'],
        "East/Central": [str(x).zfill(2) for x in (list(range(1,9)) + list(range(14,24)) + list(range(28,58)))] + ['81','82'],  # 01-08,14-23,28-57,81-82
        "West": [str(x) for x in (list(range(11,14)) + list(range(24,28)) + list(range(58,65)))]    # 11-13,24-27,58-64
    }

    headers = {
        'area': 'Area',
        'date': 'Date',
        'category': 'Item Category',
        'itemName': 'Item Name',
        'subCat': 'Item Sub-Category',
    }

    dataList = []
    for item in itemReqList:
        reqDate = item.timeSubmitted.date().strftime("%d-%m-%Y")
        postalCode = item.postalCode
        area = None
        for region in postalCodeArea:
            # check first 2 numbers in postal code for area
            if postalCode[:2] in postalCodeArea[region]:
                area = region
        dataList.append({'area': area, 'date': reqDate, 'category': item.category, 'itemName': item.itemName, 'subCat': item.subCat})
        
    # Creating excel file
    filename = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    workbook = xlsxwriter.Workbook(f'BA/excel/{filename}.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_row(row=0, col=0, data=headers.values())
    header_keys = list(headers.keys())
    for index, item in enumerate(dataList):
        row = map(lambda field_id: item.get(field_id, ''), header_keys)
        worksheet.write_row(row=index + 1, col=0, data=row)
    workbook.close()

@app.route("/request", methods=['POST'])
def addNewRequest():
        formData = request.form
        formDict = formData.to_dict()
        addtodb = {}
        addtodb["donationID"] = formDict['id']
        addtodb["postalCode"] = formDict['destination']
        addtodb["migrantID"] = formDict['contact']

        # Get datetime of donation posting
        now = datetime.now()
        currentDT = now.strftime("%Y-%m-%d %H:%M:%S")
        timeSubmitted = currentDT

        addtodb["timeSubmitted"] = timeSubmitted

        item = Request(**addtodb)
        
        try:
            db.session.add(item)
            db.session.commit()
            return jsonify (
                {
                    "code": 200,
                    "message": "Request registered successfully!"
                }
            )
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while registering your request, please try again later"
                }
            ), 500

# get all requests submitted by migrant workers
@app.route("/getRequests")
def getAllRequests():
    requestList = Request.query.all()
    data = []
    for request in requestList:
        row = {}
        donationID = request.donationID
        donationItem = Donation.query.filter_by(donationID=donationID).first()
        itemID = donationItem.itemID
        itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
        row["itemName"] = itemName
        row.update(donationItem.json())
        row.update(request.json())
        row.pop('itemID')
        row.pop('donationID')
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
    request = Request.query.filter_by(reqID=reqID).first()
    donationID = request.donationID
    donationItem = Donation.query.filter_by(donationID=donationID).first()
    itemID = donationItem.itemID
    itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
    data = {}
    data["itemName"] = itemName
    data.update(request.json())
    data.update(donationItem.json())
    data.pop("itemID")
    data.pop("donationID")
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
                # "columnHeaders": NewRequest.metadata.tables["request"].columns.keys(),
                # "data": request
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Request cannot be found for this ID."
        }
    ), 404

# update request by reqID
@app.route("/updateRequest/<reqID>", methods=["PUT"])
def updateRequest(reqID):
    requested = Request.query.filter_by(reqID=reqID).first()
    donation = Donation.query.filter_by(donationID=requested.donationID).first()
    data = request.get_json()
    if (requested is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This reqID is not found in the database."
            }
        )
    else:
        requested.postalCode = data['postalCode']
        # requested.requestQty = data['requestQty']
        requested.migrantID = data['migrantID']
        db.session.add(requested)
        db.session.commit()
        donation.itemStatus = data['itemStatus']
        db.session.add(donation)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Request successfully updated."
            }
        )

# delete request by reqID
@app.route("/deleteRequest/<reqID>", methods=["DELETE"])
def deleteRequest(reqID):
    request = Request.query.filter_by(reqID=reqID).first()
    try:
        db.session.delete(request)
        db.session.commit()
        return jsonify (
            {
                "code": 200,
                "message": "Row deleted successfully!"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while deleting the data, please try again later"
            }
        ), 500

# endregion

# region MATCHES
# get all successful matches 
@app.route("/getSuccessfulMatches")
def getAllSuccessfulMatches():
    matches = Matches.query.all()
    data = []
    for match in matches:
        row = {}
        reqID = match.reqID
        request = Request.query.filter_by(reqID=reqID).first()
        donationID = request.donationID
        donationItem = Donation.query.filter_by(donationID=donationID).first()
        itemID = donationItem.itemID
        itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
        row["itemName"] = itemName
        row.update(match.json())
        row.update(request.json())
        row.update(donationItem.json())
        row.pop('donationID')
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
    request = Request.query.filter_by(reqID=reqID).first()
    donationID = request.donationID
    donationItem = Donation.query.filter_by(donationID=donationID).first()
    itemID = donationItem.itemID
    itemName = CategoryItem.query.filter_by(itemID=itemID).first().itemName
    data = {}
    data["itemName"] = itemName
    data.update(request.json())
    data.update(donationItem.json())
    data.pop("itemID")
    data.pop("donationID")
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
    req = Request.query.filter_by(reqID=reqID).first()
    donationID = req.donationID
    donationItem = Donation.query.filter_by(donationID=donationID).first()
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
        req.postalCode = data['postalCode']
        req.requestQty = data['requestQty']
        db.session.add(req)
        db.session.commit()
        donationItem.itemStatus = data['itemStatus']
        donationItem.donorID = data['donorID']
        db.session.add(donationItem)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Match successfully updated.",
                "match": match.json(),
                # "data": data,
                # "olddata": data
            }
        )

# add new match
@app.route("/addMatch", methods=['POST'])
def addNewMatch():
    formData = request.form
    formDict = formData.to_dict()
    addtodb = {}
    addtodb["reqID"] = formDict['reqID']
    addtodb["migrantID"] = formDict['migrantID']
    addtodb["donorID"] = formDict['donorID']

    # Get datetime of match
    now = datetime.now()
    currentDT = now.strftime("%Y-%m-%d %H:%M:%S")
    timeSubmitted = currentDT

    addtodb["matchDate"] = timeSubmitted
    print(addtodb)
    item = Matches(**addtodb)
    
    try:
        db.session.add(item)
        db.session.commit()
        return jsonify (
            {
                "code": 200,
                "message": "Match added successfully!"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while adding your match, please try again later"
            }
        ), 500

# delete match by matchID
@app.route("/deleteMatch/<matchID>", methods=["DELETE"])
def deleteMatch(matchID):
    match = Matches.query.filter_by(matchID=matchID).first()
    try:
        db.session.delete(match)
        db.session.commit()
        return jsonify (
            {
                "code": 200,
                "message": "Row deleted successfully!"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while deleting the data, please try again later"
            }
        ), 500

def getNumOfMatches(req):
    # reqHist keys is migrantID, values is count
    reqHist = {}
    for r in req:
        # count the no. of times the migrant worker gotten a match
        migrantWorkerCount = Matches.query.filter_by(migrantID=r.migrantID).count()
        # if migrantworker alr in the dict, count will increase by 1
        if migrantWorkerCount in reqHist.keys():
            reqHist[migrantWorkerCount] += [r.migrantID]
        # create migrantID as a new key in the dict
        else:
            reqHist[migrantWorkerCount] = [r.migrantID]
    # all the migrantIDs
    allKeys = reqHist.keys()
    # get min. (smallest) no. of match count
    minValue = min(allKeys, default="EMPTY")
    # get list of migrantID(s) with the least match count
    priorityMW = reqHist[minValue]
    print(priorityMW)

    return priorityMW

def selfPickUpOrDelivery(priorityMW, donationID):
    # new dictionary to calc migrant worker points
    mwPoints = {}
    
    # check whether item requires delivery
    deliveryFieldID = FormBuilder.query.filter_by(fieldName="Delivery Method").first().fieldID
    deliveryOption = FormAnswers.query.filter_by(submissionID=donationID).filter_by(fieldID=deliveryFieldID).first()
    deliveryMWOption = Request.query.filter_by(postalCode="Self Pickup").filter_by()

    # variable to check whether criteria 3 has to be done
    needCheckDist = 0

    # check whether donor opt for self pickup
    if deliveryOption == "Delivery required":
        # if delivery required, all MW start with 0 points
        for mw in priorityMW:
            mwPoints[mw] = 0
        # need check Distance criteria
        needCheckDist += 1
    else:
        # check whether migrant worker opt for self pickup (but donor opt for delivery/arranged by donor)
        for mw in priorityMW:
            deliveryMWOption = Request.query.filter_by(donationID=donationID).filter_by(migrantID=mw).first()
            # if migrant worker is not 
            if deliveryMWOption == "Self Pickup":
                mwPoints[mw] = 0
        # if donor did not choose self pick-up & no mw chose self pick-up, put all mw priority as 0
        if len(mwPoints) == 0:
            for mw in priorityMW:
                deliveryMWOption = Request.query.filter_by(donationID=donationID).filter_by(migrantID=mw).first()
                mwPoints[mw] = 0
            # need check Distance criteria
            needCheckDist += 1

    return mwPoints, needCheckDist

def shortestDistance(mwPoints, needCheckDist, donationID):
    if needCheckDist > 0:
        mwDist = {}
        for mw, points in mwPoints.items():
            mwLoc = Request.query.filter_by(donationID=donationID).filter_by(migrantID=mw).first().postalCode
            addressFieldID = FormBuilder.query.filter_by(fieldName="Postal Code").first().fieldID
            donorLoc = FormAnswers.query.filter_by(submissionID=donationID).filter_by(fieldID=addressFieldID).first().answer 
            # google maps api to calculate distance
            # apikey = environ.get('GOOGLE_API_KEY')
            apikey = config.api_key
            geocodeAPI1 = "https://maps.googleapis.com/maps/api/geocode/json?address=" + donorLoc + "&components=country:SG&key=" + apikey
            response1 = requests.get(geocodeAPI1)
            if response1.status_code == 200:
                donorPlace_id = response1.json()["results"][0]["place_id"]
            geocodeAPI2 = "https://maps.googleapis.com/maps/api/geocode/json?address=" + mwLoc + "&components=country:SG&key=" + apikey
            response2 = requests.get(geocodeAPI2)
            if response2.status_code == 200:
                mwPlace_id = response2.json()["results"][0]["place_id"]
            distanceAPI = "https://maps.googleapis.com/maps/api/distancematrix/json?destinations=place_id:" + donorPlace_id + "&origins=place_id:" + mwPlace_id + "&key=" + apikey
            response3 = requests.get(distanceAPI)
            # value is the distance in meters
            if response3.status_code == 200:
                # print(response3.json()["rows"][0]["elements"][0]["distance"]["value"])
                distance = response3.json()["rows"][0]["elements"][0]["distance"]["value"]
                if distance not in mwDist.keys():
                    mwDist[distance] = [mw]
                else:
                    mwDist[distance].append(mw)
                if distance < 3000:
                    points += 1
                elif 3000 <= distance < 5000:
                    points += 2
                elif 5000 <= distance < 7000:
                    points += 3
                elif 7000 <= distance < 9000:
                    points += 4
                else:
                    points += 5
        # least no. of points = shortest distance
        shortestDist = min(list(mwDist.keys()))
        # finding nearest migrant worker using mwDist dict
        nearestMW = mwDist[shortestDist]
        # mwPoints dict to minus the points they currently have
        for n in nearestMW:
            mwPoints[n] -= 1
    return mwPoints

def timeSinceLastMatch(mwPoints):
    timeNow = datetime.now()
    for mwNum, points in mwPoints.items():
        mw = Matches.query.filter_by(migrantID=mwNum).first()
        if mw is not None:
            lastItemTime = mw.matchDate
            print(lastItemTime, timeNow)
            days = (timeNow - lastItemTime).days # convert difference into no. of days
            print(days)
            if 0 <= days < 14:
                mwPoints[mwNum] += 6
            elif 14 <= days < 28:
                mwPoints[mwNum] += 4
            elif 28 <= days < 42:
                mwPoints[mwNum] += 2
            elif 42 <= days < 56:
                mwPoints[mwNum] += 1
    # get min. no. of points
    minPoints = min(list(mwPoints.values()))
    finalMWs = []
    # get list of migrant workers that has the min. no. of points
    for mw, points in mwPoints.items():
        if points == minPoints:
            finalMWs.append(mw)
    
    return finalMWs

# randomise function for Tied MWs
def randomizeTieBreaker(finalMWs):
    randomInt = random.randint(1, len(finalMWs))
    finalMW = finalMWs[randomInt - 1]

    return finalMW

# matching algo
@app.route("/matchingAlgorithm/<string:donationID>")
def matchingAlgorithm(donationID):
    req = Request.query.filter_by(donationID=donationID)
    if req:
        # CRITERIA 1: NO. OF MATCHES
        priorityMW = getNumOfMatches(req)

        # CRITERIA 2: WHETHER DONOR/MIGRANT WORKER CHOSE SELF PICKUP
        mwPoints, needCheckDist = selfPickUpOrDelivery(priorityMW, donationID)

        # CRITERIA 3: FIND MIGRANT WORKER WITH THE SHORTEST DISTANCE
        newMWPoints = shortestDistance(mwPoints, needCheckDist, donationID)

        # CRITERIA 4: HOW LONG SINCE THEIR LAST MATCH
        finalMWs = timeSinceLastMatch(newMWPoints)

        # if only 1 migrant worker at the end, return this migrant worker
        if len(finalMWs) == 1:
            finalMW = finalMWs[0]
        else: 
            finalMW = randomizeTieBreaker(finalMWs)

        # LAST STEP: add the match to the db
        timeNow = datetime.now()
        reqID = Request.query.filter_by(donationID=donationID).filter_by(migrantID=finalMW).first().reqID
        donorID = Donation.query.filter_by(donationID=donationID).first().donorID
        match = {"reqID": reqID, "migrantID": finalMW, "donorID": donorID, "matchDate": timeNow}
        donation = Donation.query.filter_by(donationID=donationID).first()
        if donation.itemStatus == "Available":
            match = Matches(**match)
            db.session.add(match)
            db.session.commit()
            donation.itemStatus = "Unavailable"
            db.session.add(donation)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "finalMW": finalMW
                }
            )
    return jsonify(
        {
            "code": 404,
            "message": "No migrant workers requested for this donation ID."
        }
    ), 404

# endregion

# region DELIVERY
# get all delivery requests matches 
@app.route("/getDeliveryRequests")
def getDeliveryRequests():
    deliveryRequests = Matches.query.join(Delivery, Delivery.matchID == Matches.matchID).join(
        Request, Matches.reqID == Request.reqID).add_columns(
        Delivery.matchID, Delivery.driverID, Matches.migrantID, 
        Request.postalCode, Delivery.status).distinct()
    data = []
    for delivery in deliveryRequests:
        deliveryRow = delivery._asdict()
        deliveryRow.pop("Matches")
        data.append(deliveryRow)
    columns = list(data[0].keys())
    if deliveryRequests:
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
            "message": "There are no delivery requests at the moment."
        }
    ), 404

# get specific delivery request 
@app.route("/getDeliveryRequests/<matchID>")
def getDeliveryRequestsByMatchID(matchID):
    deliveryRequest = Delivery.query.filter_by(matchID=matchID).join(Matches, Delivery.matchID == Matches.matchID).join(
        Request, Matches.reqID == Request.reqID).add_columns(Delivery.matchID, Delivery.driverID, Matches.migrantID, 
        Request.postalCode, Delivery.status).first()
    columns = list(deliveryRequest.keys())
    columns.pop(0)
    if deliveryRequest:
        data = deliveryRequest._asdict()
        data.pop("Delivery")
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
            "message": "Delivery request not found."
        }
    ), 404

# get delivery locations
def getDeliveryLocations():
    deliveryLocations = Matches.query.join(Delivery, Delivery.matchID == Matches.matchID).join(
        Request, Matches.reqID == Request.reqID).add_columns(Request.postalCode).distinct()
    data = []
    for location in deliveryLocations:
        deliveryLoc = location._asdict()
        deliveryLoc.pop("Matches")
        data.append(list(deliveryLoc.values())[0])
    return data

# get delivery locations in lat, lng format 
@app.route("/getDeliveryLocationsLatLng")
def getDeliveryLocationsLatLng():
    deliveryLocList = getDeliveryLocations()
    if len(deliveryLocList) > 0:
        deliveryLocationsLatLng = []
        apikey = ""
        for loc in deliveryLocList:
            geocodeAPI = "https://maps.googleapis.com/maps/api/geocode/json?address=" + loc + "&components=country:SG&key=" + apikey
            response = requests.get(geocodeAPI)
            lat = response.json()["results"][0]["geometry"]["location"]["lat"]
            lon = response.json()["results"][0]["geometry"]["location"]["lng"]
            deliveryLocationsLatLng.append({"lat": lat, "lng": lon})
        deliveryLocationsLatLng = [{"lat": 1.368042, "lng": 103.9563529}, {"lat": 1.366873, "lng": 103.954398}]
        return jsonify(
            {
                "code": 200,
                "data": deliveryLocationsLatLng
            }
        )


# edit deliveryRequest in table
@app.route("/updateDeliveryRequest/<matchID>", methods=["PUT"])
def updateDeliveryRequest(matchID):
    deliveryRequest = Delivery.query.filter_by(matchID=matchID).join(Matches, Delivery.matchID == Matches.matchID).join(
        Request, Matches.reqID == Request.reqID).add_columns(Delivery.matchID, Delivery.driverID, Matches.migrantID, 
        Request.postalCode, Delivery.status).first()
    data = request.get_json()
    print(data)
    columns = list(deliveryRequest.keys())
    columns.pop(0)
    if (deliveryRequest is None):
        return jsonify( 
            {
                "code": 404,
                "message": "This matchID is not found in the database."
            }
        )
    else:
        deliveryReq = Delivery.query.filter_by(matchID=matchID).first()
        match = Matches.query.filter_by(matchID=matchID).first()
        req = Request.query.filter_by(reqID=match.reqID).first()
        migrantWorker = User.query.filter_by(username=match.migrantID).first()
        req.postalCode = data['postalCode']
        db.session.add(req)
        db.session.commit()
        deliveryReq.status = data['status']
        db.session.add(deliveryReq)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Match successfully updated."
                # "match": match.json(),
                # "data": data,
                # "olddata": data
            }
        )

# add new delivery request
@app.route("/addDeliveryRequest", methods=['POST'])
def addDeliveryRequest():
    formData = request.form
    formDict = formData.to_dict()
    print(formDict)
    addtodb = {}
    addtodb["matchID"] = formDict['matchID']
    addtodb["driverID"] = formDict['driverID']
    addtodb["status"] = formDict['status']

    print(addtodb)
    delivery = Delivery(**addtodb)
    
    try:
        db.session.add(delivery)
        db.session.commit()
        return jsonify (
            {
                "code": 200,
                "message": "Delivery Request added successfully!"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while adding your match, please try again later"
            }
        ), 500

# delete delivery request by matchID
@app.route("/deleteDeliveryRequest/<matchID>", methods=["DELETE"])
def deleteDeliveryRequest(matchID):
    delivery = Delivery.query.filter_by(matchID=matchID).first()
    try:
        db.session.delete(delivery)
        db.session.commit()
        return jsonify (
            {
                "code": 200,
                "message": "Row deleted successfully!"
            }
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while deleting the data, please try again later"
            }
        ), 500

# endregion

# region FAQ
# get all FAQs
@app.route("/faq")
def getAllFaq():
    faqlist = Faq.query.all()
    if len(faqlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "items": [faq.json() for faq in faqlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no FAQs at the moment."
        }
    ), 404

# get specific faq
@app.route("/faq/<int:faqID>")
def getFaq(faqID):
    faq = Faq.query.filter_by(faqID=faqID).first()
    if faq:
        return jsonify(
            {
                "code": 200,
                "data":  faq.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No FAQ was found."
        }
    ), 404

# create new faq
@app.route('/faq', methods=['POST'])
def create_faq():
    data = request.get_json()
    item = Faq(None, **data)
    if ( request.get_json() is not None ): 
        try:
            db.session.add(item)
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# edit existing faq
@app.route('/faq/<int:faqID>', methods=['POST'])
def edit_faq(faqID):
    data = request.get_json()
    item = Faq.query.filter_by(faqID=faqID).first()
    if ( item is not None ): 
        try:
            item.question = data['question']
            item.answer = data['answer']
            item.section = data['section']
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# delete existing faq
@app.route('/faq/<int:faqID>', methods=["DELETE"])
def delete_faq(faqID):
    item = Faq.query.filter_by(faqID=faqID).first()
    if ( item is not None ): 
        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# endregion

if __name__ == "__main__":
    app.run(port="5003", debug=True)
