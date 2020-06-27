# import Twilio, the Client does create Twilio object that it allow us to communicate with a Twilio account on the website
from twilio.rest import Client

# Import the flask framework
from flask import Flask, request

# This is needed to respond to any texts that come in
from twilio.twiml.messaging_response import MessagingResponse

# for csv file
import pandas as pd

from my_secret_numbers import my_auth_token, my_cell_phone_number

# Codes required by Twilio. There are specific to the twilio account being used
account_sid = 'AC6b29033ccbc35ea89272c75a48372550'
auth_token = my_auth_token

# make our twilio client
client = Client(account_sid, auth_token)

# 
sender = '+13303032055'
receivers = pd.read_csv('receivers.csv', names=['phoneNumber']).phoneNumber.tolist()[1:]
blacklist = pd.read_csv('blacklist.csv', names=['phoneNumber']).phoneNumber.tolist()[1:]
whitelist = set(receivers).difference(set(blacklist))

# Broadcast the initial text to get subscriber aware
def broadcast():
    for receiver in whitelist:
        # the text that we will text out
        text = 'Hey there gogoro roder! Do you want to check out our new powerful smart scooter S3?' + \
                '\n\nReply Y to be given the link.' + \
                '\n\nReply B to be blacklisted and stop receiving the texts from us.'

        # Use the client to send the SMS text
        client.messages.create(
            to=receiver, 
            from_=sender, 
            body=text,
            media_url='https://img.zi.org.tw/kocpc/2019/08/1565930684-e40f3c9b4a4c290919e66d5a906d2298.png'
        )

# Create our flask app
web_app = Flask(__name__)

def sms_reply():

    if request.method == 'POST':
        
        # Make incoming message to uppercase
        receive_message = str(request.data.upper())

        # Check the reply message, if they want to get the link
        if receive_message[2] == 'Y':

            response_texts = 'YooHoo~ Here is the link:' + \
                '\n\nhttps://www.gogoro.com/tw/smartscooter/s-performance/s3/'

        # If the person want to be blacklisted
        elif receive_message[2] == 'B':

            # Get the person's phone number who want to be removed from our list
            phone_number_from = request.form['From']

            response_texts = 'Got it! You have been removed from our list. If you want to re-subscribe, please reply R to us.'

            blacklist.append(phone_number_from)

            df = pd.Dataframe(blacklist, columns=['phoneNumber'])

            df.to_csv('blacklist.csv', index=False)

        # If the person want to re-subscribe
        elif receive_message[2] == 'R':
            
            phone_number_from = request.form['From']

            response_texts = 'Thank you for your re-subscribe! You have been add to our list!'

            for i in range(len(blacklist)):

                if blacklist[i] == phone_number_from:

                    blacklist.remove(phone_number_from)

                    df = pd.Dataframe(blacklist, columns=['phoneNumber'])

                    df.to_csv('blacklist.csv', index=False)
            
    # Create a response object (translate strings to twiml for us. Twilio expects twiml.)
    auto_response = MessagingResponse()

    # Put a message in our response object
    auto_response.message(response_texts)

    # Return the message to our flask website
    return str(auto_response)

web_app.add_url_rule('/sms', 'sms_reply', sms_reply, methods=['POST'])

# Code starts here
if __name__ == '__main__':

    # Broadcast initial text
    broadcast()
    
    # Run this flask app on our local server port 5000
    web_app.run()