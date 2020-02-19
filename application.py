import os

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from flask_socketio import SocketIO, emit
from wtform_fields import *
from models import *

# configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = 'Super_Secret'
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
socketio = SocketIO(app)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://syoilhbljjrvyv:35d64a02935af3684ac54adac250d21422a8e5c35b2d2d68bbfe87c9f79c097c@ec2-52-200-119-0.compute-1.amazonaws.com:5432/deevouk6kecicj"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        # hash the password, and save it in db
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add user to DB
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('index.html', form=reg_form)


@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template('login.html', form=login_form)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        return "Please Logged in!"
    return "Chat with me"


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return "Logged out"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
