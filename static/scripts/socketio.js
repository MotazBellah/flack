document.addEventListener("DOMContentLoaded", () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        socket.send("Iam connected");
    });

    socket.on('message', data => {
        console.log(`Message recived: ${data}`);
    });



})
