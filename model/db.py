import pymongo
import pymongo
import datetime
import random
client = pymongo.MongoClient("mongodb+srv://dbuser:1234@cluster0-hi2xt.gcp.mongodb.net/test?retryWrites=true&w=majority")

def retrive_slots():
    db=list(client.Interviewer.slots.find({}))
    print(len(db))
    for i in range(len(db)):
        if (len(db[i]['slots'])==0):
            del db[i]
            continue
        del db[i]['_id']
    dates=[]
    for i in range(len(db)):
        dates.append({'day':db[i]['day'],'month':db[i]['month'],'year':db[i]['year']})
    # print(db)
    # print(dates)
    l=sorted(dates, key=lambda x:(x['year'],x['month'],x['day']))
    #print(l)
    seen = set()
    sorted_dates = []
    for a in l:
        t = tuple(a.items())
        if t not in seen:
            seen.add(t)
            sorted_dates.append(a)
    print(sorted_dates)
    return {'dates':sorted_dates}

def check_id(id):
    db=client.login.candidate.find_one({'ivr_id':id})
    if(db==None):
        reply="wrong"
    elif(db['status']=='done'):
        reply="Already Booked"
    else:
        reply="ok"
    return {'reply':reply}

def get_slots(date):
    db=list(client.Interviewer.slots.find({'day':date['day'],'month':date['month'],'year':date['year']}))
    slot=[]
    for i in range(len(db)):
        for j in range(len(db[i]['slots'])):
            slot.append(db[i]['slots'][j])
    slot=list(set(slot))
    print(slot)
    return {'reply':slot}
#get_slots({'day': '09', 'month': '1', 'year': '2020'})

def fix_slot(ivr_id,date,time):
    print(ivr_id,date,time)
    username=client.login.candidate.find_one({'ivr_id':ivr_id})
    get_slots=list(client.Interviewer.slots.find({'slots':time,'day':date['day'],'month':date['month'],'year':date['year']}))
    print(username)
    print(get_slots)
    if(get_slots==None):
        reply="failure"
    elif(len(get_slots)!=0):
        min=0
        max=len(get_slots)
        s=random.randint(min,max-1)
        client.Interviewer.slots.update({'name':get_slots[s]['name'],'day':date['day'],'month':date['month'],'year':date['year']},{ '$pullAll': { 'slots': [ time ] } })
        client.login.candidate.update_one({'ivr_id':ivr_id},{'$set':{'status':'done'}})
        client.Interviewer.fixed.insert_one({'i_name':get_slots[s]['name'],'c_username':username['username'],'day':date['day'],'month':date['month'],'year':date['year'],'slot':str(time)})
        reply="success"
    else:
        reply="failure"
    return {"reply":reply}

#retrive_slots()
#fix_slot('12345',{'day':'09','month':'1','year':'2020'},"12.00PM")