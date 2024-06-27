from psycopg2 import connect
from os import environ


# def connect_to_db() -> connect:

#     conn = connect(
#     user=environ.get("DATABASE_USER"),
#     password=environ.get("DATABASE_PASS"),
#     host=environ.get("DATABASE_HOST"),
#     port=environ.get("DATABASE_PORT"),
#     database=environ.get("DATABASE_NAME"))

#     return conn
def connect_to_db() -> connect:

    database = environ.get("DATABASE_URL")

    conn = connect(database)

    return conn

def get_user_with_name(username) -> tuple:

    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('select * from users where username = %s',(username,))
    user = cursor.fetchone()
    connection.close()
    return user

def get_user_with_id(id) -> tuple:

    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('select * from users where id = %s',(id,))
    user = cursor.fetchone()
    connection.close()
    return user

    
def update_user(current_user) -> None:
    last_seen = current_user.last_seen
    about_me = current_user.about_me
    username = current_user.username
    id = current_user.id
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(
    'update users set last_seen = %s, about_me = %s, username = %s where id = %s',(last_seen,about_me,username,int(id),)
        )
    connection.commit()
    connection.close()

def user_rollback() -> None:
    connection = connect_to_db()
    connection.rollback()
    connection.close()

def new_post(post) -> None:
    body = post.body
    user_id = post.user_id
    time_stamp = post.time_stamp
    author = post.author
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("insert into posts (body, user_id, time_stamp, author) values (%s, %s, %s ,%s)",(body,user_id,time_stamp,author,))
    connection.commit()
    connection.close()

def check_post() -> list:
    
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("select * from posts order by time_stamp desc")
    posts = cursor.fetchall()
    connection.close()
    return posts

def show_posts_following(self) -> list:
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT body, time_stamp,author FROM posts LEFT JOIN users ON posts.user_id = users.id LEFT JOIN followers on posts.user_id = followers.followed_id where follower_id = %s or author = %s order by time_stamp desc"
        ,(self.id,self.username,))
    posts = cursor.fetchall()

    connection.close()
    return posts

def show_posts(username) -> list:
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("select body, time_stamp,author from posts where author = %s order by time_stamp desc",(username,))
    posts = cursor.fetchall()

    connection.close()
    return posts

def add_following(follower_id, followed_id) -> None:
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("insert into followers (follower_id, followed_id) values (%s, %s)",(follower_id, followed_id,))    
    connection.commit()
    connection.close()

def get_following(follower_id) -> list:
    list = []
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("select * from followers where follower_id = %s",(follower_id,))
    followers = cursor.fetchall()
    
    for i  in followers:
        cursor.execute("select username from users where id = %s",(i[1],))
        list.append(cursor.fetchall()[0][0])
    connection.close()
    return list



def user_is_following(self, user) -> str:
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("select * from followers where follower_id = %s and followed_id = %s",(self, user))
    user = cursor.fetchone()
    connection.close()
    if user is None:
        return False
    return True

def remove_following(follower_id, followed_id) -> None:
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("delete from followers where follower_id = %s and followed_id = %s",(follower_id, followed_id,))
    connection.commit()
    connection.close()

def user_is_followed(self) -> list|str:
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("select * from followers where followed_id = %s",(self,))
    followers = cursor.fetchall()
    list = []
    if followers == []:
        return "No one is following you"
    for i  in followers:
        cursor.execute("select username from users where id = %s",(i[0],))
        list.append(cursor.fetchall()[0][0])
    connection.close()
    return list


def follower_count(self) -> int:
    count = user_is_followed(self)
    if count == "No one is following you":
        return 0
    return len(count)

def get_following_count(self) -> int:
    data = get_following(self)
    return len(data)

