import pytz
from src.models.UserModel import User
import jwt
from flask import jsonify
import json
import requests
import datetime
from os import environ

class Security():
    key = environ.get("AWS_SECRET_KEY")
    tz = pytz.timezone("America/Caracas")

    @classmethod 
    def create_token(cls,user):
        payload={
            "iat":datetime.datetime.now(tz=cls.tz),
            "exp":datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes = 100),
            "user":user.username,
            "fullname":user.password
        }
        return jwt.encode(payload,cls.key,algorithm="HS256")
    
    @classmethod
    def verify_token(cls,headers):
        if "Authorization" in headers.keys():
            authorization = headers["Authorization"]

            encoded_token = authorization.split(" ")[1]

            try:
                jwt.decode(encoded_token,cls.key,algorithms="HS256")
                return True
            except(jwt.ExpiredSignatureError,jwt.InvalidSignatureError):
                return False
        return False
    
    @classmethod
    def do_auth(cls, id) -> dict:

        user = User.get(id)

        url = Security.create_token(user)
        # sending post request and saving response as response object
        response_text = jsonify(url)

        return response_text



    def do_get(url, access_token: str):
        headers = {
            'Authorization': ('Bearer ' + str(access_token))
        }

        response = requests.get(url, headers=headers)

        return response