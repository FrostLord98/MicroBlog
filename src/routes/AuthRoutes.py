#librerias

from flask import Blueprint,render_template, request,flash, jsonify,redirect,url_for,abort,current_app,g as app_ctx
from flask_login import current_user, login_user,logout_user,login_required
from urllib.parse import urlsplit
from datetime import datetime, timezone
import pytz

#modulos del proyecto

import src.database.db_postgresql as db 
from src.services.AuthServices import AuthService
from src.utils.Security import Security
from src.services import MailServices

from src.models.UserModel import User, Post
from src.models.FormModel import LoginForm,RegistrationForm,EditProfileForm,EmptyForm,PostForm

main = Blueprint("auth_blueprint",__name__)

@main.route('/templates/mail')
def mail():
    MailServices.send_mail()
    return render_template("mail.html", title='Home Page',data= "funciona")

@main.route('/explore')
@login_required
def explore():
    posts = db.check_post()
    publicacion = []
    for i in posts:
        data = Post(body=i[1],time_stamp=i[2],author=i[4])
        publicacion.append(data)

            #paginacion
    page = request.args.get('page', 1, type=int)
    per_page = 1
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(publicacion) + per_page - 1)//per_page

    items_on_pages = publicacion[start:end]
    return render_template("index.html", title='Home Page', posts=items_on_pages, total_pages=total_pages, page = page)



@main.route('/', methods=['GET', 'POST'])
@main.route('/templates/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    
    if form.validate_on_submit():
        post_class = Post(body=form.post.data, author=current_user.username, time_stamp= datetime.now(pytz.timezone("America/Caracas")), user_id=current_user.id)
        db.new_post(post_class)
        flash('Your post is now live!')
        return redirect(url_for('auth_blueprint.index'))
    
    posts = current_user.following_posts()
    publicacion = []
    for i in posts:
        data = Post(body=i[0],time_stamp=i[1],author=i[2])
        publicacion.append(data)
        
        #paginacion
    page = request.args.get('page', 1, type=int)
    per_page = 1
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(publicacion) + per_page - 1)//per_page

    items_on_pages = publicacion[start:end]
    return render_template("index.html", title='Home Page', form=form, posts=items_on_pages, user=current_user, total_pages=total_pages, page = page)

   


@main.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.get_user_with_name(username)
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('auth_blueprint.index'))
        if user[0] == current_user.id:
            flash('You cannot follow yourself!')
            return redirect(url_for('auth_blueprint.user', username=username))
        current_user.follow(user[0])
        flash(f'You are following {username}!')
        return redirect(url_for('auth_blueprint.user', username=username))
    else:
        return redirect(url_for('auth_blueprint.index'))

@main.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.get_user_with_name(username)
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('auth_blueprint.index'))
        if user[0] == current_user.id:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('auth_blueprint.user', username=username))
        current_user.unfollow(user[0])
        flash(f'You are not following {username}.')
        return redirect(url_for('auth_blueprint.user', username=username))
    else:
        return redirect(url_for('auth_blueprint.index'))


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.username.data == current_user.username:
            db.update_user(current_user)
            flash('Your changes have been saved.')
            return redirect(url_for('auth_blueprint.user', username=current_user.username))
        else:
            try:
                RegistrationForm().validate_username(form.username.data)
            except:
                flash('Please use a different username.')
                return redirect(url_for('auth_blueprint.edit_profile'))

            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            db.update_user(current_user)
            flash('Your changes have been saved.')
            return redirect(url_for('auth_blueprint.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',form=form)

# @main.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.now(timezone.utc)   
#         update_user(current_user)


@main.route('/templates/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    if current_user.username != username:
        data = db.get_user_with_name(username)
        user = User(data[0],data[1],fullname=data[3],about_me=data[5], email=data[4],last_seen=data[6])
        if user is None:
            abort(404)
        posts = db.show_posts(username)
        publicacion = []
        for i in posts:
            post = Post(body=i[0],time_stamp=i[1],author=i[2])
            publicacion.append(post)
        return render_template("user.html", title='Home Page', posts=items_on_pages, total_pages=total_pages, page = page, user=username, form=form)
    
    posts = db.show_posts(current_user.username)
    publicacion = []
    for i in posts:
        data = Post(body=i[0],time_stamp=i[1],author=i[2])
        publicacion.append(data)

            #paginacion
    page = request.args.get('page', 1, type=int)
    per_page = 1
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(publicacion) + per_page - 1)//per_page

    items_on_pages = publicacion[start:end]
    return render_template("user.html", title='Home Page', posts=items_on_pages, total_pages=total_pages, page = page, user=current_user, form=form)
    
    


@main.route('/templates/register.html', methods=['GET', 'POST'])
def new_register():
    if current_user.is_authenticated:
        return redirect(url_for('auth_blueprint.index'))
    form = RegistrationForm()
    if form.validate_on_submit():

        username = form.username.data
        fullname = form.fullname.data
        passwordDecoded = form.password.data
        email=form.email.data

        _user = User(0,username,passwordDecoded,fullname, email)
        AuthService.register_user(_user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth_blueprint.new_login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/templates/login.html',methods=["get","post"])
def new_login():
    form = LoginForm()    

    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.update_user(current_user)
        return redirect(url_for('auth_blueprint.index'))

    
    if form.validate_on_submit():
        user = User(username = form.username.data,password = form.password.data)
        try:
            
            registered_user = AuthService.fn_get_user(user)

        except:
            flash('Invalid username or password')
            return redirect(url_for('auth_blueprint.new_login'))

        login_user(registered_user, remember=form.remember_me.data)
        current_user.last_seen = datetime.now(timezone.utc)
        db.update_user(current_user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('auth_blueprint.index')

        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.new_login'))
#API


@main.route("/data",methods=["get"])   
@login_required
def data():
    return AuthService.fn_get_all_users()


@main.route("/users/<username>",methods=["get"])
def get_all_users(username):
        
        user = db.get_user_with_name(username)
        auth_user = User(user[0],user[1],user[2],user[3])
        token = Security.do_auth(auth_user.id)
        has_access = Security.do_get("http://127.0.0.1:5000/data", token)
        if not has_access:
            return jsonify({"response":"Unauthorized"}),401
        else :
             return data()
    

@main.route("/verify", methods=["post"])
def get_user():
    has_access = Security.verify_token(request.headers)
    if has_access:
        username = request.form["username"]
        passwordDecoded = request.form["password"]
        _user = User(0,username,passwordDecoded,None)
        registered_user = AuthService.fn_get_user(_user)
        print (request.headers)

        return jsonify({
            "payload":registered_user
        })
    else:
        return jsonify({"response":"Unauthorized"}),401

# @main.route("/register",methods=["post"])
# def register():
#     username = request.form["username"]
#     passwordDecoded = request.form["password"]
#     fullname=request.form["fullname"]

#     _user = User(0,username,passwordDecoded,fullname)
#     registered_user = AuthService.register_user(_user)
    
#     return jsonify({
#         "payload":registered_user
#     }),201

# @main.route("/login",methods=["post"])
# def login():
#     username = request.form["username"]
#     passwordDecoded = request.form["password"]

#     _user = User(0,username,passwordDecoded,None)
#     auth_user = AuthService.fn_get_user(_user)
#     registered_user = User(auth_user[0],auth_user[1],auth_user[2],auth_user[3])
    
    
#     if registered_user != None:
#         token = Security.create_token(registered_user)
#         print (request.headers)
#         return jsonify({"payload":"success", "token":token}), token
#     else:
#         return jsonify({
#             "payload":"failed"
#         })
    

# performance

# @main.before_request
# def logging_before():
#     # Store the start time for the request
#     app_ctx.start_time = time.perf_counter()


# @main.after_request
# def logging_after(response):
#     # Get total time in milliseconds
#     total_time = time.perf_counter() - app_ctx.start_time
#     time_in_ms = int(total_time * 1000)
#     # Log the time taken for the endpoint 
#     current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
#     return response
