import os
from deta import Deta
from dotenv import load_dotenv

#load env var

load_dotenv(".env")
DETA_KEY=os.getenv("DETA_KEY")
deta=Deta("d0ukwav3_c5Sg1LR6Xy4ZnmdcNx64SJr5nA2RNvdF")
#config env key

cred=deta.Base("AuthInfo")
entries=deta.Base("Entries")

def fetch_all_users():
    res=cred.fetch()
    return res.items

def insert_user(username,password,email):
    dev=fetch_all_users()
    usernames=[]
    emails=[]
    for user in dev:
        usernames.append(user["key"])
        emails.append(user["email"])
    if(username in usernames):
        return "Username already exists!\nTry another username !"
    elif(email in emails):
        return "email already exists!\nTry with another email !"
    else:
        cred.put({"key":username,"password":password,"email":email})

def authenticate(username,password):
    var=1
    dev=fetch_all_users()
    usernames=[user["key"] for user in dev]
    emails=[user["email"] for user in dev]
    for user in dev:
        if(username==user["key"] and user["password"]==password):
            return True
            var=0
    if(var):
        return False

def entrydata(date,data,username):
    entries.put({"username":username,"date":date,"data":data})

def fetch_all_instances():
    dev=entries.fetch()
    res=dev.items
    return res

def fetch_all_entries(username):
    data=[]
    dev=entries.fetch()
    res=dev.items
    for user in res:
        if user["username"]==username:
            data.append({"Entry":user["data"],"Date":user["date"]})
    return data

def delete_entry(data):
    dev=entries.fetch()
    res=dev.items
    for user in res:
        if user["data"]==data:
            entries.delete(user["key"])
