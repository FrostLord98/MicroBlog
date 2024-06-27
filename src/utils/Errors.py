from flask import render_template

from src.database.db_postgresql import user_rollback



def not_found_error(error):
    return render_template('404.html'), 404



def internal_error(error):
    user_rollback()
    return render_template('500.html'), 500