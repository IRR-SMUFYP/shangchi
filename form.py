from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
from flask_cors import CORS
from datetime import datetime
import os
from os import environ
from sqlalchemy import ForeignKey
from werkzeug.utils import secure_filename
import bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fyptest'
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

class Carousel(db.Model):
    __tablename__ = 'newcarousel'
    
    donorID = db.Column(db.Integer)
    carouselID = db.Column(db.String(30), nullable=False, primary_key=True)
    itemID = db.Column(db.Integer, nullable=False)
    timeSubmitted = db.Column(db.Date, nullable=False)
    itemStatus = db.Column(db.String(50), nullable=False)
        
    def json(self):
        return {"carouselID": self.carouselID, "donorID": self.donorID, "carouselID": self.carouselID, "itemID": self.itemID, "timeSubmitted": self.timeSubmitted, "itemStatus": self.itemStatus}

class Wishlist(db.Model):
    __tablename__ = 'newwishlist'
    
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
    __tablename__ = 'newrequest'
    
    reqId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    migrantID = db.Column(db.Integer, nullable=False)           #, ForeignKey('user.username')
    postalCode = db.Column(db.Integer, nullable=False)
    carouselID = db.Column(db.String(30), nullable=False)       #, ForeignKey('carousel.id')
    timeSubmitted = db.Column(db.Date, nullable=False)
        
    def json(self):
        return {"reqId": self.reqId, "migrantID": self.migrantID, "postalCode": self.postalCode, "carouselID": self.carouselID, "timeSubmitted": self.timeSubmitted}

#endregion


# region USER
@app.route("/registermw", methods=['POST'])
def register():
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
                    "message": "Worker account successfully created!"
                }
            )
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while registering user :" + str(e)
                }
            ), 500

@app.route("/login", methods=['POST'])
def checkLogin():
    formData = request.form
    formDict = formData.to_dict()
    uName = formDict["username"]
    pw = formDict["password"]
    
    user = User.query.filter_by(username=uName).first()
    if (user != None):
        if (bcrypt.checkpw(str(pw).encode('utf-8'), str(user.password).encode('utf-8'))):
        
            print("Password checks out")
    
        
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "message": "Authentication success!",
                        "userType": user.json()
                    }
                }
            )
        return jsonify(
        {
            "code": 404,
            "message": "User not found, please register and try again."
        }
    ), 404
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

# edit existing faq
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

@app.route("/getItemsInSubCat/<subcat>")
def getItemsInSubCat(subcat):
    itemsInCategory = CategoryItem.query.filter_by(subCat=subcat)
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

# region FORMANSWERS + CAROUSEL/WISHLIST
# get all form answers by carousel/wishlist submission
def getFormAnswersBySubmission(submissionID):
    answerlist = FormAnswers.query.filter_by(submissionID=submissionID).all()

    # map answers to field names
    mappedAnswerlist = {}
    for answer in answerlist:
        field = FormBuilder.query.filter_by(fieldID=answer.fieldID).options(load_only('fieldName')).first()
        mappedAnswerlist[field.fieldName] = answer.answer
    
    return mappedAnswerlist

# get all details of a carousel/wishlist submission
@app.route("/formanswers/<string:submissionID>")
def getAllDetailsBySubmission(submissionID):
    # check if submission from Carousel or wishlist
    submission = Carousel.query.filter_by(carouselID=submissionID).first()
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

# create new submission
@app.route('/formanswers', methods=['POST'])
def createSubmission():
    formData = request.form
    formDict = formData.to_dict()
    files = request.files
    userid = formDict['contactNo']
    formName =  formDict['formName']
    itemID = formDict['itemNameOptions']

    # calculate submissionID (datetime userID)
    now = datetime.now()
    currentDT = now.strftime("%Y-%m-%d %H:%M:%S")
    submissionID = currentDT + " " + userid
    # print(submissionID)

    # file uploading
    for fileId in files:
        # file = files[fileId]
        # save file
        # fileName = secure_filename(file.filename)
        imgFile = request.files[fileId]
        fileName = secure_filename(imgFile.filename.replace(" ", ""))
        imgFile.save(os.path.join(uploads_dir, fileName))

    # for answer in formDict:
    #     print(type(answer))
    #     print(answer + ": " +formDict[answer])

    # submit into carousel/wishlist
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
                "message": "Unable to commit to database.",
                "data" : submission.json()
            }), 500
    elif formName == "carousel":
        details["donorID"] = userid
        details["carouselID"] = submissionID
        submission = Carousel(**details)
        try:
                db.session.add(submission)
                db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({
                "message": "Unable to commit to database.",
                "data" : submission.json()
            }), 500

    # submit into formAnswers
    for id in formDict:
        answer = {"submissionID": submissionID, "formName": formName, "fieldID": id, "answer": formDict[id]}
        item = FormAnswers(**answer)
        if ( id.isdigit() ): 
            try:
                db.session.add(item)
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({
                    "message": "Unable to commit to database.",
                    "data" : item.json()
                }), 500
    
    return jsonify(formDict), 201
# endregion

# region CAROUSEL
# get all carousel items
@app.route("/carousel")
def getAllCarouselItems():
    carouselList = Carousel.query.all()
    if len(carouselList):
        itemList = []
        for carouselItem in carouselList:
            item = carouselItem.json()
            formAnswers = getFormAnswersBySubmission(item["carouselID"])
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

# get specified carousel item
@app.route("/carousel/<string:carouselID>")
def getCarouselItem(carouselID):
    carouselItem = Carousel.query.filter_by(carouselID=carouselID).first()
    if carouselItem:
        formAnswers = getFormAnswersBySubmission(carouselItem.carouselID)
        itemDetails = getItem(carouselItem.itemID).get_json()["data"]
        itemDetails.pop("itemID")   # remove duplicate itemID

        return jsonify(
            {
                "code": 200,
                "data": dict(**carouselItem.json(), **formAnswers, **itemDetails)
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
        itemList = Carousel.query.filter_by(itemID=category.itemID).all()
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

@app.route("/getItemsBySubCat/<subcat>")
def filterItems(subcat):
    subcatList = CategoryItem.query.filter_by(subCat=subcat).all()
    subcatItemList = []
    for category in subcatList:
        itemList = Carousel.query.filter_by(itemID=category.itemID).all()
        if (len(itemList)):
            categorydict = category.json()
            categorydict.pop("itemID")
            subcatDetailsList = []
            for item in itemList:
                formAns = getFormAnswersBySubmission(item.carouselID)
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
    itemReqList = Carousel.query\
        .join(Request, Request.carouselID==Carousel.carouselID)\
            .filter(Request.carouselID==Carousel.carouselID)\
                .filter(Request.migrantID==contactNo)\
                    .distinct()

    itemIdArr = [id.json()['carouselID'] for id in itemReqList]
    
    return jsonify(
        {
            "code": 200,
            "requestedItemIds": itemIdArr
        }
    )

@app.route("/request", methods=['POST'])
def addNewRequest():
        formData = request.form
        formDict = formData.to_dict()
        addtodb = {}
        addtodb["carouselID"] = formDict['id']
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
            
# endregion

if __name__ == "__main__":
    app.run(port="5003", debug=True)
