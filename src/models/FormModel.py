from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length
from src.database.db_postgresql import connect_to_db

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    fullname = StringField('Fullname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
    
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('select username from users where username = %s',(username.data,))
        user = cursor.fetchone()
        connection.close()
        user is None
            
        if user is not None:
            raise ValidationError('Please use a different username.')

        
        

    def validate_email(self, email):
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute('select email from users where email = %s',(email.data,))
        user = cursor.fetchone()
        connection.close()
        user is None
        
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')