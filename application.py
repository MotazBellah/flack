import os
from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from wtform_fields import *
from models import *

# configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = 'Super_Secret'
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
#  Initialize Flask-socketIO
socketio = SocketIO(app)
#  Create predefined rooms
ROOMS = ['lounge', 'news', 'games', 'coding']

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///chat.db')
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

        flash("Registered succesfully. Please login.", 'success')
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
        flash("Please login", 'danger')
        return redirect(url_for('login'))
    rooms = Room.query.all()
    print(rooms)
    return render_template('chat.html', username=current_user.username, rooms=rooms)


# @app.route('/create', methods=['POST'])
# def create():
#     if not current_user.is_authenticated:
#         flash("Please login", 'danger')
#         return redirect(url_for('login'))
#
#     room = request.form['room']
#     print('/////////////////')
#     print(room)
#     print('/////////////////')
#     if room in ROOMS:
#         return redirect(url_for('chat'))
#
#     ROOMS.append(room)
#     print(ROOMS)
#     return redirect(url_for('chat', rooms=ROOMS))

@app.route('/get-rooms', methods=['POST'])
def get_rooms():
    print('%%%%%%%%%%%%%%%%%')
    
    if 'username' not in session:
        flash("Please login", 'danger')
        return redirect(url_for('login'))

    if request.method == "GET":
        rooms = Room.query.all()
        print('####################')
        print(rooms)
        print('#####################')
        # return jsonify({'rooms': ROOMS})
        return jsonify(rooms=[i.serialize for i in catalogs])
    else:
        room = request.form['room'].lower()
        room_object = Room.query.filter_by(name=room).first()
        print('/////////////////')
        print(room_object)
        print('/////////////////')
        if not room_object:
            room = Room(name=room)
            db.session.add(room)
            db.session.commit()

    return jsonify({'success': 'Room created'})


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash("You have logged out successfuly", "success")
    return redirect(url_for('login'))

# server-side event handler to recivie/send messages
@socketio.on('message')
def message(data):
    # print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'],
          'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])


# server-side event handler to join the room
@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({"msg": data['username'] + " has joined the " + data['room'] + " room."}, room=data['room'])


# server-side event handler to leave the room
@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({"msg": data['username'] + " has left the " + data['room'] + " room."}, room=data['room'])


@socketio.on("create room")
def create(data):
    room = data["room"]
    join_room(room)
    emit("creation", {"room": room}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
