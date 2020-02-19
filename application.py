import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from wtform_fields import *
from models import *

# configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = 'Super_Secret'
socketio = SocketIO(app)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://empawzdedkzmzu:ec111b26dda56b50cd61a648b60eebda842e2189b782ff308a8d56d3c1a512c6@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d8s47squ17rp4l"
db = SQLAlchemy(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Check username exists
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return 'Someone else has taken this username!'
        # Add user to DB
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB!"
        
    return render_template('index.html', form=reg_form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
