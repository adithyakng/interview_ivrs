from flask import Flask,url_for
from twilio.twiml.voice_response import VoiceResponse
app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def hello():
    return "Hello World! ADithya"

@app.route("/voice", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Thank you for calling! Have a great day.", voice='alice')

    return str(resp)
@app.route("/welcome",methods=['GET','POST'])
def welcome():
    response = VoiceResponse()
    with response.gather(
        num_digits=1, action=url_for('hello'), method="POST"
    ) as g:
        g.say(body="Thanks for calling the E T Phone Home Service. " +
              "Please press 1 for directions." +
              "Press 2 for a list of planets to call.", loop=3)
    print(response)
    return "string"

if __name__ == "__main__":
    app.run(debug=True)
