### Overview
In this project, you’ll build an online messaging service using Flask, similar in spirit to Slack. Users will be able to sign into your site with a display name, create channels (i.e. chatrooms) to communicate in, as well as see and join existing channels. Once a channel is selected, users will be able to send and receive messages with one another in real time. Implemented using Flask-SocketIO with both the database (PostgreSQL) and the app deployed in Heroku

## Files in the program
- application.py: the file containing the server-side elements of the application (Python, Flask, Flask-Socketio).
- scripts/chat_page.js: the file containing the client-side elements of the application
- scripts/socketio.js: the file containing the client-side that handle SocketIO connection
- requirements.txt: list of Python packages installed
- templates/: folder with all HTML files
- static/: for with all JS scripts and CSS files

## Application Features

- Display Name: When a user visits your web application for the first time, they should be prompted to type in a display name that will eventually be associated with every message the user sends. If a user closes the page and returns to your app later, the display name should still be remembered.
- Channel Creation: Any user should be able to create a new channel, so long as its name doesn’t conflict with the name of an existing channel.
- Channel List: Users should be able to see a list of all current channels, and selecting one should allow the user to view the channel. We leave it to you to decide how to display such a list.
- Messages View: Once a channel is selected, the user should see any messages that have already been sent in that channel, up to a maximum of 100 messages. Your app should only store the 100 most recent messages per channel in server-side memory.
- Sending Messages: Once in a channel, users should be able to send text messages to others the channel. When a user sends a message, their display name and the timestamp of the message should be associated with the message. All users in the channel should then see the new message (with display name and timestamp) appear on their channel page. Sending and receiving messages should NOT require reloading the page.
- Remembering the Channel: If a user is on a channel page, closes the web browser window, and goes back to your web application, The application should remember what channel the user was on previously and take the user back to that channel.
- Personal Touch: support use attachments (file uploads) as messages

## Clone/Run app
````
# Clone repo
$ git clone https://github.com/MotazBellah/sc50p2.git

# Install all dependencies
$ pip install -r requirements.txt

# Run
$ python application.py

# Go to 127.0.0.1:5000 on your web browser.
````
