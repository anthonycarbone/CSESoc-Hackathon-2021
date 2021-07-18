import os

import config
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def subscribeTwilioClient(mobile):
    account_sid = os.environ[config.TWILIO_ACCOUNT_SID]
    auth_token = os.environ[config.TWILIO_AUTH_TOKEN]
    client = Client(account_sid, auth_token)

    incoming_phone_number = client.incoming_phone_numbers.create(
        phone_number=mobile,
    )
    account_sid = config.TWILIO_SMS_SID
    auth_token = config.TWILIO_SMS_AUTH
    client = Client(account_sid, auth_token)

    return client


def sendTwilioSMS(client, msgBody, subscriberMobile):
    print(f"Successfully sent message: {msgBody} to user {subscriberMobile}!")
    message = client.messages.create(
        messaging_service_sid="MGa696de920e0d52b90076a10865a8d7ca",
        body=msgBody,
        to=subscriberMobile,
    )

    print(message.sid)
