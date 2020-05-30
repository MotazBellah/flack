document.addEventListener("DOMContentLoaded", () =>{

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

    document.querySelector('#create-room').onclick = () => {
        const room = prompt("Please enter the name of the room");
        if (room != null){
            $.ajax({
                type: 'post',
                url: '/create',
                data: {
                    room: room
                },
                success: function() {
                    alert("New Room Created")
                    window.location.href = "/chat"
                }
            });
        }
    };
})
