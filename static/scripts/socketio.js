document.addEventListener("DOMContentLoaded", () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // make lounge is a default room
    //  and add the user to it
    let room = 'Lounge';
    joinRoom("Lounge")


    // recieve message from the server
    // Create a pragraph contains username, data and time
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        // If user write message in one of the room
        if(data.username){
            p.setAttribute("class", "my-msg");
            span_username.setAttribute("class", "my-username");
            span_timestamp.setAttribute("class", "timestamp");
            
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML +
                          data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
        }
        // If user join/leave the room
        // no need to display the username
        else {
            printSysMsg(data.msg);
        }

    });


    // Get the text on the input field and send it to the server once the button is clicked
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value,
                     'username': username, 'room': room
                 });
        // Clear input area
        document.querySelector('#user_message').value = '';

    }

    // Room selection
    const rooms = document.querySelectorAll('.select-room');
    rooms.forEach((p) => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room){
                msg = `You are already in ${room} room.`;
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }

        }
    });

    // Leave room
    function leaveRoom(room) {
        // use emit, beacuse its custom event
        socket.emit('leave', {'username': username, 'room': room});
    }

    // Join room
    function joinRoom(room) {
        // use emit, beacuse its custom event
        socket.emit('join', {'username': username, 'room': room});
        // clear message area
        document.querySelector("#display-message-section").innerHTML = '';
        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }

    // Print system messages
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector("#display-message-section").append(p)
        document.querySelector("#user_message").focus();
    }



})
