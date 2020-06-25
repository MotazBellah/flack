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
# Only python 3
import urllib.parse


app = Flask(__name__)
app.config["SECRET_KEY"] = 'Super_secret_key'
socketio = SocketIO(app)
#  Create gloable variables, to store the rooms and messages
ROOMS = []
mesage = {}

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

# Return all the rooms if exist, to display it
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

# Return all the messages if exist, to display it
@app.route('/get-messages', methods=['POST'])
def get_messages():
    if 'username' not in session:
        flash("Please login", 'danger')
        return redirect(url_for('login'))

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
    # Remove the user from the session
    session.pop('username',None)
    flash("You have logged out successfuly", "success")
    return redirect(url_for('login'))

# check_profanity before send the message to other users
@app.route('/check-profanity', methods=['POST'])
def check_profanity():
    try:
        # Get the data from ajax request, which is the user message
        text = request.form['text']
        # Use wdylike website to check if the text contains a profanity
        encoded_text = urllib.parse.quote(text, 'utf-8')
        with urlopen("http://www.wdylike.appspot.com/?q="+encoded_text) as url:
            output = url.read().decode("utf-8")
            if 'true' in output:
                return jsonify({"error": 'Found Profanity Error'})
    except Exception as e:
        print(e)
        pass

    return jsonify({"success": 'Nothing bad'})

# server-side event handler to recivie/send messages
@socketio.on('message')
def message(data):
    x = data
    # Added time stamp to the data
    x['time_stamp'] = strftime('%b-%d %I:%M%p', localtime())
    # If the user in the room
    # Save the messages in the mesage dict as value for room key
    # keep saving, till the length be 100, then delete the odler message
    if data['room'].lower() in ROOMS:
        if len(mesage[data['room'].lower()]) < 100:
            mesage[data['room'].lower()].append(x)
        else:
            mesage[data['room'].lower()].pop(0)
            mesage[data['room'].lower()].append(x)

    send({'msg': data['msg'], 'username': data['username'],
          'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'].lower())


# server-side event handler to join the room
@socketio.on('join')
def join(data):
    # If the room in the global variable ROOM, then join
    # Else, make sure the user won't be hoisted by nonexistent rooms
    if data['room'] in ROOMS:
        join_room(data['room'])
        send({"msg": data['username'] + " has joined the " + data['room'] + " room."}, room=data['room'])
    else:
        leave_room(data['room'])


# server-side event handler to leave the room
@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({"msg": data['username'] + " has left the " + data['room'] + " room."}, room=data['room'])

# server-side event handler to create new room
@socketio.on("create room")
def create(data):
    room = data["room"]
    join_room(room)
    emit("creation", {"room": room}, broadcast=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port, debug=True)
    socketio.run(app, host='0.0.0.0', port=port)
