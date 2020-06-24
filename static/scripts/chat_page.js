document.addEventListener("DOMContentLoaded", () =>{
    console.log(login);
    // if (login==='loggedout') {
    //     const name = prompt("Please enter your name")
    //     if (name != null){
    //         $.ajax({
    //             type: 'post',
    //             url: '/',
    //             data: {
    //                 name: name
    //             },
    //             success: function(response) {
    //                 console.log(response);
    //                 alert("Welcome to the chat app")
    //                 var div = document.querySelector('#user-name')
    //                 var p = document.createElement('p')
    //                 p.textContent = "Let's chatting " + name
    //                 console.log(p);
    //                 div.appendChild(p)
    //                 console.log(div);
    //                 // window.location.href = "/chat"
    //             }
    //         });
    //     }
    // }
    // let room = localStorage.getItem('lastRoom');
    // console.log(room);
    // if (!room) {
    //     document.querySelector('#send_message').display = true;
    //     document.querySelector("#input-area").style.display = "none";
    // } else {
    //     document.querySelector('#send_message').disabled = false;
    //     document.querySelector("#input-area").style.display = "block";
    // }

    // Make sidebar collapse on click
    document.querySelector('#show-sidebar-button').onclick = () => {
        document.querySelector('#sidebar').classList.toggle('view-sidebar');
    };

    // Make 'enter' key submit message
    let msg = document.querySelector('#user_message');
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        // key code of `enter` key is 13
        if (event.keyCode === 13) {
            document.querySelector('#send_message').click();
        }
    });

    // document.querySelector('#create-room').onclick = () => {
    //     const room = prompt("Please enter the name of the room");
    //     if (room != null){
    //         $.ajax({
    //             type: 'post',
    //             url: '/create',
    //             data: {
    //                 room: room
    //             },
    //             success: function(response) {
    //                 if ('error' in response) {
    //                     alert(response['error'])
    //                     return
    //                 } else {
    //                     alert("New Room Created")
    //                     // var rooms = document.querySelector('#rooms')
    //                     // var p = document.createElement('p')
    //                     // p.textContent = room
    //                     // p.className = 'select-room'
    //                     // console.log(p);
    //                     // rooms.appendChild(p)
    //                     // console.log(rooms);
    //                     window.location.href = "/"
    //             }
    //             }
    //         });
    //     }
    // };
})
