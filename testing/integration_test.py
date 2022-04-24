import unittest
import flask_testing
import bcrypt
import json
from datetime import datetime
from testingapp import app, db, User, FormBuilder, FormAnswers, CategoryItem, Donation, Wishlist, Request, Matches, Delivery, Faq

class TestApp(flask_testing.TestCase):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestRegisterAccount(TestApp):

    def test_register_new_migrant_worker(self):

        request_body = {
                            "userName": 91234567,
                            "pw": "abc123"
                        }

        response = self.client.post("/registermw",
                                    data=request_body)
        self.assertEqual(response.json,
                        {
                                "code" : 200,
                                "message" : "Worker account for 91234567 successfully created!"
                        })

    def test_login_account(self):
        pw = bcrypt.hashpw(str("abc123").encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        print(pw)
        user = User(username=91234567, password=pw, userType="worker")

        db.session.add(user)
        db.session.commit()

        request_body = {
                            "username": 91234567,
                            "password": "abc123"
                        }

        response = self.client.post("/login",
                                    data=request_body)
        self.assertEqual(response.json,
                        {
                                "code" : 200,
                                "data": {
                                    "message": "Authentication success!",
                                    "userType": user.json()
                                }                        
                        })


class TestFormBuilder(TestApp):

    def test_get_form_fields(self):

        field1 = FormBuilder(fieldID=1, formName="donation", fieldName="First Name", fieldType="text", placeholder="Enter your first name", options=None)
        field2 = FormBuilder(fieldID=2, formName="donation", fieldName="Last Name", fieldType="text", placeholder="Enter your last name", options=None)
        
        db.session.add(field1)
        db.session.add(field2)
        db.session.commit()

        response = self.client.get("/formbuilder/donation")
        self.assertEqual(response.json,
                        {
                            "code" : 200,
                            "data": {
                                "items": [field1.json(), field2.json()]
                            }                       
                        })

    def test_create_field(self):

        request_body = {
                        "fieldID": 1,
                        "formName": "donation",
                        "fieldName": "Name",
                        "fieldType":"text",
                        "placeholder":"Enter your name",
                        "options":None
                        }

        response = self.client.post("/formbuilder",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json,
                        {
                        "fieldID": 1,
                        "formName": "donation",
                        "fieldName": "Name",
                        "fieldType":"text",
                        "placeholder":"Enter your name",
                        "options":None})


class TestCategoryItem(TestApp):

    def test_retrieve_catalog(self):

        item1 = CategoryItem(itemID=1, itemName="Shirt", category="Clothes", subCat="Tops")
        item2 = CategoryItem(itemID=2, itemName="Jacket", category="Clothes", subCat="Tops")
        
        db.session.add(item1)
        db.session.add(item2)
        db.session.commit()

        response = self.client.get("/getCatalog")
        self.assertEqual(response.json,
                        {
                            "code" : 200,
                            "items": [item1.json(), item2.json()]
                        })

    def test_get_item_names(self):

        item1 = CategoryItem(itemID=1, itemName="Shirt", category="Clothes", subCat="Tops")
        item2 = CategoryItem(itemID=2, itemName="Pants", category="Clothes", subCat="Bottoms")
        
        db.session.add(item1)
        db.session.add(item2)
        db.session.commit()

        response = self.client.get("/getItemNames/Clothes/Tops")
        
        self.assertEqual(response.json,
                        {
                            "code" : 200,
                            "data": {
                                "itemsInCat": [item1.json()]
                            }
                        })


class TestFormAnswers(TestApp):

    def test_get_specific_form_answers(self):

        current_datetime = datetime.now()
        field1 = FormBuilder(fieldID=1, formName="donation", fieldName="First Name", fieldType="text", placeholder="Enter your first name", options=None)
        field2 = FormBuilder(fieldID=2, formName="donation", fieldName="Last Name", fieldType="text", placeholder="Enter your last name", options=None)
        donation = Donation(donorID=91234567, donationID=1, itemID=1, timeSubmitted=current_datetime, itemStatus="Available")
        answer1 = FormAnswers(answerID=1, submissionID=1, formName="donation", fieldID=1, answer="John")
        answer2 = FormAnswers(answerID=2, submissionID=1, formName="donation", fieldID=2, answer="Doe")

        db.session.add(field1)
        db.session.add(field2)
        db.session.add(donation)
        db.session.add(answer1)
        db.session.add(answer2)
        db.session.commit()

        self.maxDiff = None
        response = self.client.get("/getFormAnswers/donation/1")
        self.assertEqual(response.json,
                        {
                            "code" : 200,
                            "columnHeaders":{
                                '1': 'First Name',
                                '2': 'Last Name',
                                '3': 'donorID',
                                '4': 'donationID',
                                '5': 'itemID',
                                '6': 'timeSubmitted',
                                '7': 'itemStatus'
                            } ,
                            "data": {
                                'First Name': 'John', 
                                'Last Name': 'Doe', 
                                'donationID': '1', 
                                'donorID': 91234567, 
                                'itemID': 1, 
                                'itemStatus': 'Available', 
                                'submissionID': '1',
                                'timeSubmitted': current_datetime.strftime('%a, %d %b %Y') + ' 00:00:00 GMT'}        
                        })

    def test_create_submission(self):

        request_body = {
                        "contactNo": 91234567,
                        "formName": "donation",
                        "itemName": 1,
                        "1":"John",
                        "2":"Doe",
                        }

        response = self.client.post("/formanswers",
                                    data=request_body)
        self.assertEqual(response.json,
                        {
                        "message": "Form submitted successfully."})


class TestDonation(TestApp):

    def test_get_all_donations(self):

        current_datetime = datetime.now()
        item1 = CategoryItem(itemID=1, itemName="Shirt", category="Clothes", subCat="Tops")
        field1 = FormBuilder(fieldID=1, formName="donation", fieldName="First Name", fieldType="text", placeholder="Enter your first name", options=None)
        field2 = FormBuilder(fieldID=2, formName="donation", fieldName="Last Name", fieldType="text", placeholder="Enter your last name", options=None)
        donation = Donation(donorID=91234567, donationID=1, itemID=1, timeSubmitted=current_datetime, itemStatus="Available")
        answer1 = FormAnswers(answerID=1, submissionID=1, formName="donation", fieldID=1, answer="John")
        answer2 = FormAnswers(answerID=2, submissionID=1, formName="donation", fieldID=2, answer="Doe")

        db.session.add(item1)
        db.session.add(field1)
        db.session.add(field2)
        db.session.add(donation)
        db.session.add(answer1)
        db.session.add(answer2)
        db.session.commit()

        response = self.client.get("/donation")
        self.assertEqual(response.json,
                        {
                            "code" : 200,
                            "data": {
                                "items": [{
                                    'First Name': 'John', 
                                    'Last Name': 'Doe', 
                                    'category': 'Clothes', 
                                    'donationID': '1', 
                                    'donorID': 91234567, 
                                    'itemID': 1, 
                                    'itemName': 'Shirt', 
                                    'itemStatus': 'Available', 
                                    'subCat': 'Tops', 
                                    'timeSubmitted': current_datetime.strftime('%a, %d %b %Y') + ' 00:00:00 GMT'}]
                            }
                        })

    def test_filter_items(self):

        current_datetime = datetime.now()
        item1 = CategoryItem(itemID=1, itemName="Shirt", category="Clothes", subCat="Tops")
        field1 = FormBuilder(fieldID=1, formName="donation", fieldName="First Name", fieldType="text", placeholder="Enter your first name", options=None)
        field2 = FormBuilder(fieldID=2, formName="donation", fieldName="Last Name", fieldType="text", placeholder="Enter your last name", options=None)
        donation = Donation(donorID=91234567, donationID=1, itemID=1, timeSubmitted=current_datetime, itemStatus="Available")
        answer1 = FormAnswers(answerID=1, submissionID=1, formName="donation", fieldID=1, answer="John")
        answer2 = FormAnswers(answerID=2, submissionID=1, formName="donation", fieldID=2, answer="Doe")

        db.session.add(item1)
        db.session.add(field1)
        db.session.add(field2)
        db.session.add(donation)
        db.session.add(answer1)
        db.session.add(answer2)
        db.session.commit()

        response = self.client.get("/getItemsBySubCat/Clothes/Tops")
        self.assertEqual(response.json,
                        {
                            "code" : 200,
                            "data": {
                                "items": [{
                                    'First Name': 'John', 
                                    'Last Name': 'Doe', 
                                    'category': 'Clothes', 
                                    'donationID': '1', 
                                    'donorID': 91234567, 
                                    'itemID': 1, 
                                    'itemName': 'Shirt', 
                                    'itemStatus': 'Available', 
                                    'subCat': 'Tops', 
                                    'timeSubmitted': current_datetime.strftime('%a, %d %b %Y') + ' 00:00:00 GMT'}]
                            }
                        })


class TestFaq(TestApp):

    def test_get_all_faq(self):
            
        faq1 = Faq(faqID=1, question="What is the best way to donate?", answer="You can donate by phone, email, or in person.", section="donor")
        faq2 = Faq(faqID=2, question="How do I contact the admin?", answer="You can contact the admin by clicking on the contact button on the home page.", section="donor")
    
        db.session.add(faq1)
        db.session.add(faq2)
        db.session.commit()

        response = self.client.get("/faq")
        self.assertEqual(response.json,
                        {
                            "code" : 200,
                            "data": {
                                "items": [faq1.json(), faq2.json()]
                            }
                        })
