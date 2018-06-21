
from flask_restful import Resource, Api

from flask import request

from werkzeug.security import generate_password_hash, check_password_hash
# hashes passwords
from datetime import datetime, timedelta
# to get departure time
from models.user_model import User
import jwt

signup_info = []
# where user signup information is stored
driver_info = []
# where driver information is stored after registration
driver_details = {}
# the driver details a passanger user sees while viewing ride_offers[].

class UserSignUp(Resource):
    # inherits from resource


    def post(self):
        # user post signup data
        signup_data = request.get_json()        
        # returns data in json format
        hashed_password = generate_password_hash(signup_data.get("password"), method="sha256")

        # validation starts

        # checks if data field is empty
        # firstname
        if not signup_data.get("firstname"):
            return{'message':"enter first name"},400
        # lastname
        if not signup_data.get("lastname"):
            return{'message':"enter last name"},400
        # username
        if not signup_data.get("username"):
            return{'message':"enter user name"},400
        # password
        if not signup_data.get("password"):
            return{'message':"enter password"},400
        # confirmpassword
        if not signup_data.get("confirmpassword"):
            return{'message':"enter confirm password"},400

        # checks if data is space filled 
        if " " in signup_data.get("firstname"):
            return{'message':"enter visible character"},400
        if " " in signup_data.get("lastname"):
            return{'message':"enter visible character"},400
        if " " in signup_data.get("username"):
            return{'message':"enter visible character"},400
        if " " in signup_data.get("password"):
            return{'message':"enter visible character"},400
        if " " in signup_data.get("confirmpassword"):
            return{'message':"enter visible character"},400

        # confirms confirm password == password is the same
        if signup_data.get("password") != signup_data.get("confirmpassword"):
            return{"message":"password and confirm password not the same"}

        for user in signup_info:
            if signup_data.get("username") == user["username"]:
                return {"message":"username already exist"},400
        # an instance of User in models containing user data
        new_user = User(signup_data.get("firstname"),
                        signup_data.get("lastname"),
                        signup_data.get("username"),
                        hashed_password
                        )            
        # save new user as a {}, to signup info[]
        signup_info.append({"firstname":new_user.firstname,
                      "lastname":new_user.lastname,
                      "username":new_user.username,
                       "password":hashed_password
                       })
        return{"message":"Welcome you have successfully signed up"},201            
 
    def get(self):
        pass

class DriverReg(Resource):
    #class driver registration  resource

    def post(self):
        regData = request.get_json()
        hashed_password = generate_password_hash(regData.get("password"), method="sha256")
        # check empty field
        if not regData.get("firstname"):
            return{'message':"enter first name"},400
        if not regData.get("lastname"):
            return{'message':"enter last name"},400
        if not regData.get("username"):
            return{'message':"enter user name"},400
        if not regData.get("phone_number"):
            return{'message':"enter phone number"},400
        if not regData.get("password"):
            return{'message':"enter password"},400
        if not regData.get("car"):
            return{'message':"enter your type of car"},400
        if not regData.get("confirmpassword"):
            return{'message':"enter confirm password"},400

        # checks for spaces only field
        if " " in regData.get("firstname"):
            return{'message':"enter visible character"},400
        if " " in regData.get("lastname"):
            return{'message':"enter visible character"},400
        if " " in regData.get("username"):
            return{'message':"enter visible character"},400
        if " " in regData.get("phone_number"):
            return{'message':"enter visible character"},400
        if " " in regData.get("car"):
            return{'message':"enter visible character"},400    
        if " " in regData.get("password"):
            return{'message':"enter visible character"},400
        if " " in regData.get("confirmpassword"):
            return{'message':"enter visible character"},400

        #confirms confirmpassword == password is the same
        if regData.get("password") != regData.get("confirmpassword"):
            return{"message":"password and confirm password not the same"},400
        
        # an instance of class ser containing user data
        new_driver = Driver(regData.get("firstname"),
                            regData.get("lastname"),
                            regData.get("username"),
                            regData.get("car"),
                            hashed_password
                            )
        # save driver_details to driver_detail{} will be see by passangers
        driver_details[new_driver.username] = {"type_of_car":new_driver.car}
        print("driver_details")

                        
        # save new drive to driver info[]
        driver_info.append({"firstname":new_user.firstname,
                            "lastname":new_user.lastname,
                            "username":new_user.username,
                            "password":hashed_password,
                            "driver_detail":driver_details
                            })
        print("driver_info")
        return{"message":"Welcome you have successfully registered as a driver"},201  

class UserLogIn(Resource):
    # userlogin resource
    def post(self):
        
        # username and password requied
        data = request.get_json()
        for dictionary in signup_info:
            if data.get("username") == dictionary["username"]:
                # compares given and stored hash passwords
                if check_password_hash(dictionary["password"], data.get("password")):
                    access_token =jwt.encode({"username":dictionary["username"],
                                            "exp":datetime.utcnow() + timedelta(minutes=60)},
                                             "this is my secret key to encode the token")
                    # import pdb;pdb.set_trace()
                    return {"token":access_token.decode("UTF -8"),"message":"successfully logged in"},200

                return{"message":"wrong password"}
        return{"message":"signup first"}