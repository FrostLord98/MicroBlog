from src.database.db_postgresql import connect_to_db
from src.models.UserModel import User
from flask import request
import jwt

key = "secret"

class AuthService():
    

    @classmethod
    def register_user(cls,user):
        connection = connect_to_db()
        username = user.username
        passwordDecoded = user.password
        fullname=user.fullname
        email = user.email
        passwordEncoded = jwt.encode({"password": passwordDecoded}, key, algorithm="HS256")
        cursor = connection.cursor()
        cursor.execute('insert into users (username,password,fullname,email) values(%s,%s,%s,%s)',(username,passwordEncoded,fullname,email,))
        connection.commit()
        connection.close()
        return "success"
    
    @classmethod
    def fn_get_all_users(cls):
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('select * from users')
        users = cursor.fetchall()
        connection.close()
        return users
    
    @classmethod
    def fn_get_user(cls,user):
        username = user.username
        passwordEncoded = jwt.encode({"password": user.password}, key, algorithm="HS256")
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('select * from users where password =%s and username = %s',(passwordEncoded,username,))
        auth_user = cursor.fetchone()
        connection.close()
        user = User(auth_user[0],auth_user[1],auth_user[2],auth_user[3],auth_user[4],auth_user[5],auth_user[6])

        return user
