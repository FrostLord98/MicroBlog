from flask_login import UserMixin, LoginManager
from src.database.db_postgresql import get_user_with_id
from hashlib import md5
from datetime import datetime
import pytz
import src.database.db_postgresql as db

login = LoginManager()
login.login_view = "auth_blueprint.new_login"
key = "secret"

class User(UserMixin):
    
    def __init__(self, id=0, username = 0, password = 0, fullname = 0, email = 0, about_me = 0, last_seen = 0) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname  
        self.email = email  
        self.about_me = about_me
        self.last_seen = last_seen
        

    @login.user_loader
    def load_user(id) :
        
        try:
            data = get_user_with_id(id)
            user = User(data[0],data[1],data[2],data[3],data[4],data[5],data[6])
            return  user
        except:
            return None
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
# followed y following

    def follow(self, user):
         if not self.is_following(user):
            db.add_following(self.id,user)

    def unfollow(self, user):
        if self.is_following(user):
            db.remove_following(self.id,user)
    
    def get_following(self):
        return db.get_following(self.id)
    
    
    def is_following(self, user):
        return db.user_is_following(self.id,user)
        
    def is_followed(self):
        return db.user_is_followed(self.id)
    
    def following_posts(self):
        return db.show_posts_following(self)
    
    def followers_count(self):
        return db.follower_count(self.id)
    
    def following_count(self):
        return db.get_following_count(self.id)
    
    def check_post(self):
        return db.check_post(self)

    
class Post():
    def __init__(self, id = 0, body=0,time_stamp=lambda: datetime.now(pytz.timezone("America/Caracas")),user_id=0,author=0 ) -> None:
        self.id = id
        self.body = body
        self.time_stamp = time_stamp
        self.author = author
        self.user_id = user_id


    def avatar(self, size):
        author = self.author
        user = db.get_user_with_name(author)
        digest = md5(user[4].lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def load_user(self) :
        username = self.username
        try:
            data = db.get_user_with_username(username)
            user = User(data[0],data[1],data[2],data[3],data[4],data[5],data[6])
            return  user
        except:
            return None