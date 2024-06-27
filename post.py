
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)


app.config['MAIL_SERVER']= 'live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = 'b690bb3fe214777aa8be32ef4d4ecad0'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
@app.route("/")
def index():
    msg = Message(subject='Hello from the other side!', sender='luis@demomailtrap.com', recipients=['luisobando22@gmail.com'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works."
    mail.send(msg)
    return "Message sent!"


if __name__ == '__main__':
    app.run(debug=True)