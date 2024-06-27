from src.database.db_postgresql import connect_to_db
from src.models.LanguageModel import Language
from flask import jsonify


class LanguageService():

    def get_languages():
            connection = connect_to_db()
            languages = []
            with connection.cursor() as cursor:
                cursor.execute('select * from languages')
                resultset = cursor.fetchall()
                for row in resultset:
                    language = Language(int(row[0]), row[1])
                    languages.append(language.to_json())
            connection.close()
            return languages
    