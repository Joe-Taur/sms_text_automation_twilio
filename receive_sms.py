# Import the flask framework
from flask import Flask

# This is needed to respond to any texts that come in
from twilio.twiml.messaging_response import MessagingResponse

# Create our flask app
web_app = Flask(__name__)

def sms_reply():

    # Create a response object (translate strings to twiml for us. Twilio expects twiml.)
    auto_response = MessagingResponse()

    # Put a message in our response object
    auto_response.message('This is SMS text receive and process web app.')
    print(auto_response)

    # Return the message to our flask website
    return str(auto_response)

web_app.add_url_rule('/sms', 'sms_reply', sms_reply, methods=['POST'])

# Code starts here
if __name__ == '__main__':
    # Run this flask app on our local server port 5000
    web_app.run()