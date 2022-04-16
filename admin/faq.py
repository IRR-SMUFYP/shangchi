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


if __name__ == "__main__":
    app.run(port="5001", debug=True)
