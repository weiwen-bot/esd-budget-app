from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from os import environ


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    # autoincrement automatically generates a unique value for each new record
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(50), nullable=False)
    # String to account for (+) or (-) country codes 
    PhoneNumber = db.Column(db.String(20), nullable=False)
    # (10,5) represents 10 digits in and 5 decimal point
    Credits = db.Column(db.DECIMAL(10, 5), nullable=False)
    # Can store both numeric and alphabetical characters
    Account_no = db.Column(db.String(20), nullable=False)

    def __init__(self, UserID, UserName, PhoneNumber, Credits,Account_no):
        self.UserID = UserID
        self.UserName = UserName
        self.PhoneNumber = PhoneNumber
        self.Credits = Credits
        self.Account_no = Account_no


    def json(self):
        return {
            "UserID": self.UserID,
            "UserName": self.UserName,
            "PhoneNumber": self.PhoneNumber,
            "Credits": float(self.Credits),  
            "Account_no": self.Account_no
        }



@app.route("/user")
def get_all():
    userlist = db.session.scalars(db.select(User)).all()


    if len(userlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in userlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no user."
        }
    ), 404

 
@app.route("/user/<int:UserID>")
def find_user(UserID):
    user = db.session.scalars(
    	db.select(User).filter_by(UserID=UserID).
    	limit(1)
        ).first()


    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404


@app.route("/user/<int:UserID>", methods=['POST'])
def create_user(UserID):
    if (db.session.scalars(
        db.select(User).filter_by(UserID=UserID).
    	limit(1)
        ).first()
):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "UserID": UserID
                },
                "message": "User already exists."
            }
        ), 400

    data = request.get_json()
    user = User(UserID, **data)


    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "UserID": UserID
                },
                "message": "An error occurred creating the user."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201

@app.route("/user/<int:UserID>", methods=['PUT'])
def update_user(UserID):
    # user = User.query.get(UserID)
    user = db.session.scalars(
    	db.select(User).filter_by(UserID=UserID).
    	limit(1)
        ).first()

    if not user:
        return jsonify(
            {
                "code": 404,
                "message": "User not found."
            }
        ), 404

    data = request.get_json()
    # update da user info
    if 'UserName' in data:
        user.UserName = data['UserName']
    if 'PhoneNumber' in data:
        user.PhoneNumber = data['PhoneNumber']
    if 'Credits' in data:
        user.Credits = data['Credits']
    if 'Account_no' in data:
        user.Account_no = data['Account_no']

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the user."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": user.json()
        }
    ), 200

@app.route("/user/register", methods=['POST'])
def register_user():
    data = request.get_json()
    # Assuming UserID is auto-incremented, can set it as None
    return create_user(None, **data)

@app.route("/user/login", methods=['POST'])
def login_user():
    data = request.get_json()
    user = db.session.query(User).filter_by(UserName=data['UserName'], Password=data['Password']).first()
    if not user:
        return jsonify({
            "code": 401,
            "message": "Invalid credentials."
        }), 401

    return jsonify({
        "code": 200,
        "data": user.json(),
        "message": "Login successful."
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)


    