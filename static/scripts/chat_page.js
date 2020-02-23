document.addEventListener("DOMContentLoaded", () =>{
    // Make 'enter' key submit message
    let msg = document.querySelector('#user_message');
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        // key code of `enter` key is 13
        if (event.keyCode === 13) {
            document.querySelector('#send_message').click();
        }
    });
})
