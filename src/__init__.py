# from flask import Flask
# from os import environ
# from src.models.UserModel import login
# # Routes
# from src.routes import LanguagesRoutes,AuthRoutes
# from src.utils import Errors

# app = Flask(__name__)

# app.config["AWS_ACCESS_KEY"] = environ.get("AWS_ACCESS_KEY")
# app.config["AWS_SECRET_KEY"] = environ.get("AWS_SECRET_KEY")
# app.config["SECRET_KEY"] = environ.get("SECRET_KEY")

# def init_app(config):
#     # Configuration
#     app.config.from_object(config)

#     # Blueprints
#     app.register_blueprint(LanguagesRoutes.main)
#     app.register_blueprint(AuthRoutes.main)
#     app.register_error_handler(Errors.not_found_error,404)
#     app.register_error_handler(Errors.internal_error,500)
    
#     return app