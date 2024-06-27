from flask import Flask
from flask_mail import Mail
from os import environ
# # Routes
from src.models.UserModel import login
from src.routes import LanguagesRoutes,AuthRoutes
from src.utils import Errors

app = Flask(__name__)

login.init_app(app)



#registro de blueprint
app.register_blueprint(LanguagesRoutes.main)
app.register_blueprint(AuthRoutes.main)


#registro de errores

app.register_error_handler(404,Errors.not_found_error)
app.register_error_handler(500,Errors.internal_error)

#configuracion AWS
app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
app.config["AWS_ACCESS_KEY"] = environ.get("AWS_ACCESS_KEY")
app.config["AWS_SECRET_KEY"] = environ.get("AWS_SECRET_KEY")


#configuracion mail
app.config['MAIL_SERVER']= 'live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = 'b690bb3fe214777aa8be32ef4d4ecad0'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

mail.init_app(app)



if __name__ =="__main__":
    app.run(debug=True)