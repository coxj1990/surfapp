from os import environ
from twilio.rest import Client

account_sid = environ['TWILIO_ACCOUNT_SID']
auth_token = environ['TWILIO_AUTH_TOKEN']
messaging_service_id = environ['TWILIO_MESSAGING_SID']
my_phone_number = environ['MY_PHONE_NUMBER']

def send_message(body):
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=body,
        messaging_service_sid=messaging_service_id,
        to=my_phone_number
    )
