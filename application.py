import os
from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from werkzeug.utils import secure_filename
from flask import send_from_directory
# To make sure the code is correct with python 2.x and 3.x
try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen
import urllib.parse


app = Flask(__name__)
app.config["SECRET_KEY"] = 'Super_secret_key'
socketio = SocketIO(app)
#  Create predefined rooms
ROOMS = []
mesage = {}

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'filename': filename})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        flash("Please login", 'danger')
        return redirect(url_for('login'))
    login = 'loggedout'
    username = ''
    if 'username' in session:
        login = 'loggedin'
        username = session['username']
    else:
        return redirect(url_for('login'))

    return render_template('chat.html', username=username, login=login, ROOMS=ROOMS)


@app.route('/get-rooms', methods=['POST'])
def get_rooms():
    if 'username' not in session:
        flash("Please login", 'danger')
        return redirect(url_for('login'))

    if request.method == "GET":
        return jsonify({'rooms': ROOMS})
    else:
        room = request.form['room'].lower()

        if room not in ROOMS:
            ROOMS.append(room)
            mesage[room] = []

    return jsonify({'success': 'Room created'})

@app.route('/get-messages', methods=['POST'])
def get_messages():
    if 'username' not in session:
        flash("Please login", 'danger')
        return redirect(url_for('login'))

    text = []
    room = request.form['room'].lower()

    if room in mesage:
        return jsonify({'messages': mesage[room]})

    return jsonify({'messages': []})


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        session['username']=request.form['username']
        flash("You have loggedin successfuly", "success")
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username',None)
    flash("You have logged out successfuly", "success")
    return redirect(url_for('login'))

def check_profanity(text):
    encoded_text = urllib.parse.quote(text, 'utf-8')
    with urlopen("http://www.wdylike.appspot.com/?q="+encoded_text) as url:
        output = url.read().decode("utf-8")
        if 'true' in output:
            return True
        else:
            return False

# server-side event handler to recivie/send messages
@socketio.on('message')
def message(data):
    x = data
    print('^^^^^^^^^^^^^^^^^^^^^^^')
    print(check_profanity(data['msg']))
    print('^^^^^^^^^^^^^^^^^^^^^^^')
    if check_profanity(data['msg']):
        error = "Found-Profanity-Alarm-Error"
    else:
        x['time_stamp'] = strftime('%b-%d %I:%M%p', localtime())
        error = ''
        if data['room'] in mesage:
            if len(mesage[data['room'].lower()]) < 5:
                mesage[data['room'].lower()].append(x)
            else:
                mesage[data['room'].lower()].pop(0)
                mesage[data['room'].lower()].append(x)

    send({'msg': data['msg'], 'username': data['username'],
          'time_stamp': strftime('%b-%d %I:%M%p', localtime()), 'errors': error}, room=data['room'].lower())


# server-side event handler to join the room
@socketio.on('join')
def join(data):
    if ROOMS:
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
    port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port, debug=True)
    socketio.run(app, host='0.0.0.0', port=port)
