from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/fyptest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

class FormBuilder(db.Model):
    __tablename__ = 'formbuilder'

    fieldID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    formName = db.Column(db.String(15), nullable=False)
    fieldName = db.Column(db.String(50), nullable=False)
    fieldType = db.Column(db.String(15), nullable=False)
    placeholder = db.Column(db.String(50))
    options = db.Column(db.String(200))

    def __init__(self, fieldID, formName, fieldName, fieldType, placeholder, options):
        self.fieldID = fieldID
        self.formName = formName
        self.fieldName = fieldName
        self.fieldType = fieldType
        self.placeholder = placeholder
        self.options = options

    def json(self):
        return {"fieldID": self.fieldID, "formName": self.formName, "fieldName": self.fieldName, "fieldType": self.fieldType, "placeholder": self.placeholder, "options": self.options}

# get all fields by form
@app.route("/formbuilder/<string:formName>")
def getFieldsByForm(formName):
    fieldlist = FormBuilder.query.all()
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
    item = FormBuilder(None, **data)
    if ( request.get_json() is not None ): 
        try:
            db.session.add(item)
            db.session.commit()
            return jsonify(item.json()), 201
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500


if __name__ == "__main__":
    app.run(port="5003", debug=True)