from datetime import datetime
import unittest
from requests import request

from sqlalchemy import null
import app

class TestUser(unittest.TestCase):

    def test_json(self):
        user = app.User(username=91234567, password="abc123", userType="worker")
        self.assertEqual(user.json(), {
            "username": 91234567,
            "password": "abc123",
            "userType": "worker"}
        )
        
class TestFormBuilder(unittest.TestCase):

    def test_json(self):
        field = app.FormBuilder(fieldID=1, formName="donation", fieldName="Name", fieldType="text", placeholder="Enter your name", options=None)
        self.assertEqual(field.json(), {
            "fieldID": 1,
            "formName": "donation",
            "fieldName": "Name",
            "fieldType":"text",
            "placeholder":"Enter your name",
            "options":None}
        )
        
class TestCategoryItem(unittest.TestCase):

    def test_json(self):
        item = app.CategoryItem(itemID=1, itemName="Shirt", category="Clothes", subCat="Tops")
        self.assertEqual(item.json(), {
            "itemID": 1,
            "itemName": "Shirt",
            "category": "Clothes",
            "subCat": "Tops"}
        )
        
class TestDonation(unittest.TestCase):

    def test_json(self):
        donation = app.Donation(donorID=91234567, donationID=1, itemID=1, timeSubmitted=datetime.now(), itemStatus="Available")
        self.assertEqual(donation.json(), {
            "donorID": 91234567,
            "donationID": 1,
            "itemID": 1,
            "timeSubmitted": datetime.now(),
            "itemStatus": "Available"}
        )

class TestWishlist(unittest.TestCase):

    def test_json(self):
        wishlist = app.Wishlist(migrantID=91234567, wishlistID=1, itemID=1, timeSubmitted=datetime.now(), itemStatus="Pending")
        self.assertEqual(wishlist.json(), {
            "migrantID": 91234567,
            "wishlistID": 1,
            "itemID": 1,
            "timeSubmitted": datetime.now(),
            "itemStatus": "Pending"}
        )

class TestFormAnswers(unittest.TestCase):

    def test_json(self):
        formanswers = app.FormAnswers(answerID=1, submissionID=1, formName="donation", fieldID=1, answer="abc123")
        self.assertEqual(formanswers.json(), {
            "answerID": 1,
            "submissionID": 1,
            "formName": "donation",
            "fieldID": 1,
            "answer": "abc123"}
        )

class TestRequest(unittest.TestCase):

    def test_json(self):
        request = app.Request(reqID=1, migrantID=91234567, postalCode=123456, donationID=1, timeSubmitted=datetime.now())
        self.assertEqual(request.json(), {
            "reqID": 1,
            "migrantID": 91234567,
            "postalCode": 123456,
            "donationID": 1,
            "timeSubmitted": datetime.now()}
        )

class TestMatches(unittest.TestCase):

    def test_json(self):
        match = app.Matches(matchID=1, reqID=1, migrantID=91234567, donorID=98765432, matchDate=datetime.now())
        self.assertEqual(match.json(), {
            "matchID": 1,
            "reqID": 1,
            "migrantID": 91234567,
            "donorID": 98765432,
            "matchDate": datetime.now()}
        )

class TestDelivery(unittest.TestCase):

    def test_json(self):
        delivery = app.Delivery(matchID=1, status="Delivered", driverID=93456789)
        self.assertEqual(delivery.json(), {
            "matchID": 1,
            "status": "Delivered",
            "driverID": 93456789}
        )
        
class TestFaq(unittest.TestCase):

    def test_json(self):
        user = app.Faq(faqID=1, question="What is the best way to donate?", answer="You can donate by phone, email, or in person.", section="donor")
        self.assertEqual(user.json(), {
            "faqID": 1,
            "question": "What is the best way to donate?",
            "answer": "You can donate by phone, email, or in person.",
            "section": "donor"}
        )
