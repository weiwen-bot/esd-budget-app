from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from os import environ


app = Flask(__name__)
from os import environ
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
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
    Email = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(50), nullable=False)

    def __init__(self, UserName, PhoneNumber, Credits,Account_no,Email,Password):

        self.UserName = UserName
        self.PhoneNumber = PhoneNumber
        self.Credits = Credits
        self.Account_no = Account_no

        self.Email = Email
        self.Password = Password



    def json(self):
        return {
            "UserID": self.UserID,
            "UserName": self.UserName,
            "PhoneNumber": self.PhoneNumber,
            "Credits": float(self.Credits),  
            "Account_no": self.Account_no,
            "Email": self.Email,
            "Password": self.Password

        }

class PoolMapping(db.Model):
    __tablename__ = 'poolmapping'

    PoolID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, primary_key=True)

    def __init__(self, PoolID, UserID):
        self.PoolID = PoolID
        self.UserID = UserID

    def json(self):
        return {
            "PoolID": self.PoolID,
            "UserID": self.UserID
        }


# Login function
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    user = find_user(data['UserName'])

    if user:
        if user.Password == data['Password']:
            return jsonify(
                {
                    "code": 200,
                    "data": user.json()
                }
            )
        else:
            return jsonify(
                {
                    "code": 401,
                    "message": "Incorrect password."
                }
            ), 401
    else:
        return jsonify(
            {
                "code": 404,
                "message": "User not found."
            }
        ), 404


#get all users
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

#get user by UserID
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

#add user
@app.route("/user", methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    if (db.session.scalars(
        db.select(User).filter_by(UserName=user.UserName).
    	limit(1)
        ).first()
):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "UserName": user.UserName
                },
                "message": "User already exists."
            }
        ), 400
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "UserID": user.UserName
                },
                "message": "An error occurred creating the user.",
                "error": str(e)
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201


#update user
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

@app.route("/user/<int:UserID>", methods=['DELETE'])
def delete_user(UserID):
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

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while deleting the user.",
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "Message": "successfully deleted user."
        }
    ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5004, debug=True)


    