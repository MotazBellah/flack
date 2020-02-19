import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from wtform_fields import *

# configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = 'Super_Secret'
socketio = SocketIO(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        return "Great"
    return render_template('index.html', form=reg_form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
