# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say



# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACc4a94a3084f9c23c6329de7c536c2f27'
auth_token = '4bdd76b4008a1089de65caea99cd9bbd'
client = Client(account_sid, auth_token)
response = VoiceResponse()
response.say('Hello I am Mr.Darwinbot here to book your')

call = client.calls.create(
                        to='+919908849904',
                        from_='+12017482629',
                        url="https://handler.twilio.com/twiml/EHc54e83b3943296b38f097db5bf8d5169"
                    )

print(call.sid)
client.calls.create