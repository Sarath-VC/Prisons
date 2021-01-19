import mysql.connector
def selection(q):
    con = get_current_con()
    cursor = con.cursor(dictionary=True)
    cursor.execute(q)
    result = cursor.fetchall()
    return result
    cursor.close()
    con.close()

def insertion(tablename,values):
    con = get_current_con()
    cursor = con.cursor()
    value=values.values()
    key=",".join(values.keys())
    val=[]
    for i in value:
        val.append("'"+str(i)+"'")
    value=",".join(val)

    q="insert into %s (%s) values (%s)" % (tablename,key,value)
    cursor.execute(q)
    con.commit()
    rowid=cursor.lastrowid
    cursor.close()
    con.close()
    return rowid
def updation(q):
    con = get_current_con()
    cursor = con.cursor()
    cursor.execute(q)
    con.commit()
    cursor.close()
    con.close()

def deletion(q):
    con = get_current_con()
    cursor = con.cursor()
    cursor.execute(q)
    con.commit()
    cursor.close()
    con.close()
def get_current_con():
    con = mysql.connector.connect(user="root", password="root", host="localhost", database="nebula")
    cursor = con.cursor(dictionary=True)
    dbs = "prison"
    cursor.execute("select * from log inner join db using (db_id) inner join cloud using (cloud_id) where db_name='%s' order by log_id DESC" % dbs)
    result = cursor.fetchall()
    hst = result[0]['host']
    username = result[0]['username']
    password = result[0]['password']
    con = mysql.connector.connect(user=username, password=password, host=hst, database="prison")
    return con
