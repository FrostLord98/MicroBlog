#librerias

from flask import Blueprint, render_template
from flask_mail import Mail, Message

#modulos
import src.database.db_postgresql as db

mail = Mail()


def send_mail():
    msg = Message(subject='Hello from the other side!', sender='luis@demomailtrap.com', recipients=['luisobando22@gmail.com'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works."
    mail.send(msg)
    return render_template('mail.html', title='Home Page',data= "funciona")