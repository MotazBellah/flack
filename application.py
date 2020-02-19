import os

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user
from passlib.hash import pbkdf2_sha256
from flask_socketio import SocketIO, emit
from wtform_fields import *
from models import *

# configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = 'Super_Secret'
socketio = SocketIO(app)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://empawzdedkzmzu:ec111b26dda56b50cd61a648b60eebda842e2189b782ff308a8d56d3c1a512c6@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d8s47squ17rp4l"
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
        if current_user.is_authenticated:
            return "Logged in!"
        return "not logged in"

    return render_template('login.html', form=login_form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
