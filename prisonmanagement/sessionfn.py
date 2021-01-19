import mysql.connector
from mypackage import database
from flask import session

def is_logged_in():
    if ("login_id" in session) and ("username" in session) and ("password" in session) and ("user_type" in session):
        return True
    else:
        return False
def login(data):
    q="select * from login where username='%s' and password='%s'" % data
    result = database.selection(q)
    if(len(result)==1):
        session['login_id']=result[0]['login_id']
        session['username']=result[0]['username']
        session['password']=result[0]['password']
        session['user_type']=result[0]['user_type']
        session['login_flag']=result[0]['login_flag']
        return True
    else:
        return False
def getuser():
    return session['user_type']


