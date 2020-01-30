from flask import Flask,request,session
from twilio.twiml.voice_response import VoiceResponse, Gather
from model import db

app = Flask(__name__)

app.secret_key="adithya"
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()
    string="Welcome to Darwinbox IVR. "
    unique_Str="Please enter the unique 5 digit id"
    gather = Gather(num_digits=5,action="/gather")
    gather.say(string+unique_Str)
    resp.append(gather)
    resp.redirect('/voice')

    print(resp)
    return str(resp)    

@app.route("/gather",methods=['GET','POST'])
def check_id():
    resp = VoiceResponse()
    id_entered = request.values['Digits']
    id_check_result=db.check_id(id_entered)
    reply=id_check_result['reply']
    if(reply=='ok'):
        session['ivr_id']=id_entered
        
        resp.redirect('/dates')
        return str(resp)
    elif(reply=="wrong"):
        resp.say(body="Wrong Id entered. Goodbye!")
        return str(resp)
    else:
        resp.say(body="You have already booked your slot. Thank you   ")
        return str(resp)

@app.route("/dates",methods=['GET','POST'])
def dates_fix():
    dates=db.retrive_slots()
    dates=dates['dates']
    session['dates']=dates
    str_generate=""
    for i in range(min(len(dates),9)):
        str_generate=str_generate+" Press "+str(i)+" for "+str(dates[i]['month']+"/"+dates[i]['day']+"/"+dates[i]['year'])+". "
    print(str_generate)
    resp=VoiceResponse()
    #resp.say(body=str_generate)
    gather = Gather(num_digits=1,action="/slot_fix")
    gather.say(body=str_generate)
    resp.append(gather)
    return str(resp)

@app.route("/slot_fix",methods=['GET','POST'])
def slot_fix():
    date_number=int(request.values['Digits'])
    session['slot_date']=session['dates'][date_number]
    get_slots=db.get_slots(session['dates'][date_number])
    get_slots=get_slots['reply']
    session['time']=get_slots
    str_generate=""
    for i in range(len(get_slots)):
        str_generate=str_generate+" Press "+str(i)+" for "+str(get_slots[i])+" . "
    resp = VoiceResponse()
    gather = Gather(num_digits=1,action="/slot_booked")
    gather.say(str_generate)
    resp.append(gather)
    print(resp)
    return str(resp)    

@app.route("/slot_booked",methods=['GET','POST'])
def slot_booked():
    resp=VoiceResponse()
    slot_time=request.values['Digits']
    reply=db.fix_slot(session['ivr_id'],session['slot_date'],session['time'][int(slot_time)])
    if(reply['reply']=='success'):
        str_generate="Your slot has been successfully booked on "+str(session['slot_date'])+"          Thank you   "
    else:
        str_generate="Sorry your slot cannot be booked try again"
    resp.say(str_generate+"      Thank you")
    return str(resp)






months_mapping={
    '1':"January",
    '2':'February',
    '3':'March',
    '4':'April',
    '5':'May',
    '6':'June',
    '7':'July',
    '8':'August',
    '9':'September',
    '10':'October',
    '11':'November',
    '12':'December'
}

if __name__ == "__main__":
    app.run(debug=True)


# from signalwire.voice_response import VoiceResponse, Gather

# @app.route('/voice',methods=['GET','POST'])
# def voice():
#     response = VoiceResponse()
#     response.say("Hello World")
#     print(response)
