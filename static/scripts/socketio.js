document.addEventListener("DOMContentLoaded", () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // recieve message from the server
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const br = document.createElement('br');
        span_username.innerHTML = data.username;
        p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML;
        document.querySelector('#display-message-section').append(p);
    });

    // socket.on('some-event', data => {
    //     console.log(data);
    // });


    // Get the text on the input field and send it to the server once the button is clicked
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value,
                     'username': username
                 });

    }



})
