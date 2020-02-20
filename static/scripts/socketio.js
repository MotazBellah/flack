document.addEventListener("DOMContentLoaded", () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    // Connect to the server
    socket.on('connect', () => {
        socket.send("Iam connected");
    });
    // recieve message from the server
    socket.on('message', data => {
        const p = document.createElement('p');
        const br = document.createElement('br');
        p.innerHTML = data;
        document.querySelector('#display-message-section').append(p);
    });

    socket.on('some-event', data => {
        console.log(data);
    });

    const button = document.querySelector('#send_message');
    const inputText = document.querySelector('#user_message');
    // Get the text on the input field and send it to the server once the button is clicked
    button.onclick = () => {
        socket.send(inputText.value)
    }



})
