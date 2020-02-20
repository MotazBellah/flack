document.addEventListener("DOMContentLoaded", () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    // Connect to the server
    socket.on('connect', () => {
        socket.send("Iam connected");
    });
    // recieve message from the server
    socket.on('message', data => {
        console.log(`Message recived: ${data}`);
    });



})
