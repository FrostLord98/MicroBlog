from flask import Blueprint,request,jsonify
from src.services.LanguageServices import LanguageService
from src.utils.Security import Security

main = Blueprint('language_blueprint', __name__)


@main.route("/languages", methods=["get"])
def get_lang():

    has_access = Security.verify_token(request.headers)
    if has_access:
        return LanguageService.get_languages()
    else:
        return jsonify({"response":"Unauthorized"})