document.addEventListener("DOMContentLoaded", () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    if (!localStorage.getItem('lastRoom')) {
        localStorage.setItem('lastRoom', '')
    }

    // make lounge is a default room
    //  and add the user to it
    let room = localStorage.getItem('lastRoom');

    if (room !== '') {
        document.querySelector('#send_message').disabled = false;
        // document.querySelector("#input-area").style.display = "block";
        joinRoom(room)
    } else {

        alert("Please create a room to start chatting")
        document.querySelector('#send_message').display = true;
        // document.querySelector("#input-area").style.display = "none";
    }


    function displayMessage(data) {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_data = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        // If user write message in one of the room
        if(data.username){
            p.setAttribute("class", "my-msg");
            p.onclick = displayFile;
            span_username.setAttribute("class", "my-username");
            span_timestamp.setAttribute("class", "timestamp");
            span_timestamp.setAttribute("class", "data");

            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            span_data.innerHTML = data.msg;
            p.innerHTML = span_username.outerHTML + br.outerHTML +
                          span_data.outerHTML + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
        }
        // If user join/leave the room
        // no need to display the username
        else {
            printSysMsg(data.msg);
        }
    }

    function displayFile(event) {
        event.preventDefault();
        const file_name = this.children[2].textContent;

        $.ajax({
            type: 'get',
            url: '/uploads/' + file_name ,
            data: {

            },
            success: function(response) {
                window.location.href = '/uploads/' + file_name
            }
        });

    }

    // recieve message from the server
    // Create a pragraph contains username, data and time
    socket.on('message', data => {
        displayMessage(data);
    });


    // Get the text on the input field and send it to the server once the button is clicked
    document.querySelector('#send_message').onclick = () => {
        // Get the user message
        var user_message = document.querySelector('#user_message').value
        // Send post AJAX request to check_profanity
        // If profanity found, informe the user before send it to all other users
        // else, send it to all other users
        $.ajax({
            type: 'post',
            url: '/check-profanity',
            data: {
                text: user_message
            },
            success: function(response) {
                if ('error' in response) {
                    var acknowledge = confirm("Your message contains a profanity, do want to send anyway?")
                    if (acknowledge) {
                        socket.send({'msg': user_message,
                                    'username': username, 'room': room
                                    });
                        }

                } else {
                    socket.send({'msg': user_message,
                                'username': username, 'room': room
                                });
                }
            }
        });

        // Clear input area
        document.querySelector('#user_message').value = '';

    }

        /* attach a submit handler to the form */
    $("#send_file_form").submit(function(event) {


      /* stop form from submitting normally */
      event.preventDefault();
      var form_data = new FormData($('#send_file_form')[0]);

      /* get the action attribute from the <form action=""> element */
      var form = $(this);


      $.ajax({
             type: "POST",
             url: '/upload-file',
             data: form_data, // serializes the form's elements.
             contentType: false,
             cache: false,
             processData: false,
             success: function(data)
             {

                 socket.send({'msg': data['filename'],
                                  'username': username, 'room': room
                              });
             }
           });

    });

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
        var room = room.toLowerCase();
        // use emit, beacuse its custom event
        socket.emit('leave', {'username': username, 'room': room});
    }

    // Join room
    function joinRoom(room) {
        var room = room.toLowerCase();
        // use emit, beacuse its custom event
        socket.emit('join', {'username': username, 'room': room});
        localStorage.setItem('lastRoom', room)
        // clear message area
        document.querySelector("#display-message-section").innerHTML = '';
        // Autofocus on text box
        document.querySelector("#user_message").focus();
        $.ajax({
            type: 'post',
            url: '/get-messages',
            data: {
                room: room
            },
            success: function(response) {
                for (var i = 0; i < response['messages'].length; i++) {

                    displayMessage(response['messages'][i])
                }
            }
        });
    }

    // When connected, check room creation
      socket.on('connect', () => {
          document.querySelector('#create-room').onclick = () => {
              const room = prompt("Please enter the name of the room");
              if (room != null){
                socket.emit('create room', {'room': room});

                $.ajax({
                    type: 'POST',
                    url: '/get-rooms',
                    data: {
                        room: room
                    },
                    success: function() {
                        // Do Nothing!
                        }
                    });

              }
          };
      });

      // Create a room in HTML
      socket.on('creation', data => {
          var rooms = document.querySelector('#rooms')
          var p = document.createElement('p')
          p.textContent = data.room
          p.className = 'select-room'

          rooms.appendChild(p)

          const cx = document.querySelectorAll('.select-room');

          cx.forEach((p) => {
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
      });


    // Print system messages
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector("#display-message-section").append(p)
        document.querySelector("#user_message").focus();
    }



})
