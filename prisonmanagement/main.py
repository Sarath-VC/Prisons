from flask import session,Flask,render_template,redirect,request,url_for,flash
from mypackage import database
import sessionfn as sf
import random,string
app=Flask(__name__)
app.secret_key='secretkeyanith'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin/',methods=['GET','POST'])
def admin_home():
    if(sf.is_logged_in()==True):
        return render_template('admindash.html')
    else:
       return redirect(url_for('login'))

@app.route('/user/',methods=['GET','POST'])
def user_home():
    if (sf.is_logged_in() == True):
        lid = session['login_id']
        q3 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res3 = database.selection(q3)
        dicres={
            "db":res3
        }
        return render_template('userdash.html',data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/login/',methods=['GET','POST'])
def login():
    if 'uname' in request.form:
        user=request.form['uname']
        pwd=request.form['password']
        users=(user,pwd)
        if(sf.login(users)):
            if (session['user_type'] == 'ADMIN'):
                return redirect(url_for('admin_home'))
            else:
                return redirect(url_for('user_home'))

        else:
            return render_template('login.html',err="Username or Password is invalid !!!")
    else:
        return render_template('login.html')

@app.route('/logout/',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin/regprison/',methods=['GET','POST'])
def regprison():
    if (sf.is_logged_in() == True):
        q="select * from category"
        result=database.selection(q)
        dicres = {
            "db": result

        }
        if "sbmt" in request.form:
            pris=request.form['pname']
            cat=request.form['cat']
            post=request.form['post']
            city=request.form['city']
            dist=request.form['dist']
            state=request.form['state']
            pin=request.form['pin']
            cont=request.form['contact']
            emil=request.form['mail']

            dict = {
                "p_name": pris ,
                "cat_id": cat ,
                "p_post": post,
                "p_city": city,
                "p_district": dist,
                "p_state": state,
                "p_pin": pin,
                "p_contact": cont,
                "p_email": emil,
                "p_flag": "1",
            }
            database.insertion("prisons", dict)

        return render_template('regprison.html',data=dicres)

    else:
       return redirect(url_for('login'))

@app.route('/admin/viewprison/',methods=['GET','POST'])
def viewprison():
    if (sf.is_logged_in() == True):
        bid = request.args['id']
        q1="select * from prisons left join category using (cat_id) where p_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "bid":bid,
            "res":res

        }
        return render_template('viewprison.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/updprison/',methods=['GET','POST'])
def updprison():
    if (sf.is_logged_in() == True):
        bid = request.args['id']
        q11="select * from category"
        ress=database.selection(q11)
        q1="select * from prisons inner join category using (cat_id) where p_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "bid":bid,
            "res":res,
            "db":ress

        }
        if "sbmt" in request.args:
            pris = request.args['pname']
            cat = request.args['cat']
            post = request.args['post']
            city = request.args['city']
            dist = request.args['dist']
            state = request.args['state']
            pin = request.args['pin']
            cont = request.args['contact']
            emil = request.args['mail']
            q2="UPDATE prisons SET p_name='%s',cat_id='%s',p_post='%s',p_city='%s',p_district='%s',p_state='%s',p_pin='%s',p_contact='%s',p_email='%s',p_flag=1 WHERE p_id='%s'" % (pris,cat,post,city,dist,state,pin,cont,emil,bid)
            database.updation(q2)
            return redirect(url_for('manageprison'))
        return render_template('updprison.html', data=dicres)
    else:
       return redirect(url_for('login'))


@app.route('/admin/manageprison/',methods=['GET','POST'])
def manageprison():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE  FROM prisons WHERE p_id='%s'" % id
            database.deletion(q1)
            return redirect(url_for('manageprison'))
        q = "select * from prisons left join category using (cat_id)"
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('manageprison.html',data=dicres)
    else:
       return redirect(url_for('login'))


@app.route('/admin/regblock/',methods=['GET','POST'])
def regblock():
    if (sf.is_logged_in() == True):
        q="select * from prisons"
        result=database.selection(q)
        dicres = {
            "db": result

        }
        if "sbmt" in request.form:
            blk=request.form['bname']
            pris=request.form['pname']
            dict = {
                "block_name": blk,
                "p_id": pris,
            }
            database.insertion("block", dict)
            return redirect(url_for('manageblock'))
        return render_template('regblock.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/viewblock/',methods=['GET','POST'])
def viewblock():
    if (sf.is_logged_in() == True):
        q="select * from prisons"
        result=database.selection(q)

        bid = request.args['id']
        q1="select * from block left join prisons using (p_id) where block_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res

        }
        return render_template('viewblock.html', data=dicres)
    else:
       return redirect(url_for('login'))



@app.route('/admin/updblock/',methods=['GET','POST'])
def updblock():
    if (sf.is_logged_in() == True):
        q="select * from prisons"
        result=database.selection(q)

        bid = request.args['id']
        q1="select * from block left join prisons using (p_id) where block_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res

        }
        if "sbmt" in request.args:
            blk=request.args['bname']
            pris=request.args['pname']
            print pris,blk,bid
            q2="UPDATE block SET p_id='%s',block_name='%s' WHERE block_id='%s' " % (pris,blk,bid)
            database.updation(q2)
            return redirect(url_for('manageblock'))
        return render_template('updblock.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/manageblock/',methods=['GET','POST'])
def manageblock():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE  FROM block WHERE block_id='%s'" % id
            database.deletion(q1)
            return redirect(url_for('manageblock'))
        q = "select * from block left join prisons using (p_id)"
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('manageblock.html',data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/regcell/',methods=['GET','POST'])
def regcell():
    if (sf.is_logged_in() == True):
        q="select * from prisons"
        result=database.selection(q)
        dicres = {
            "db": result

        }
        if "sbmt" in request.form:
            blk=request.form['bname']
            cell=request.form['cnum']
            dict = {
                "cell_num": cell,
                "block_id": blk,

            }
            database.insertion("cell", dict)
        return render_template('regcell.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/viewcell/',methods=['GET','POST'])
def viewcell():
    if (sf.is_logged_in() == True):
        q="select * from prisons"
        result=database.selection(q)

        bid = request.args['id']
        q1="select * from cell left join block using (block_id) left join prisons using (p_id) where cell_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res

        }
        return render_template('viewcell.html', data=dicres)
    else:
       return redirect(url_for('login'))



@app.route('/admin/updcell/',methods=['GET','POST'])
def updcell():
    if (sf.is_logged_in() == True):
        q="select * from prisons"
        result=database.selection(q)
        q3="select * from block"
        res3=database.selection(q3)

        bid = request.args['id']
        q1="select * from cell left join block using (block_id) left join prisons using (p_id) where cell_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res,
            "bl":res3

        }
        if "sbmt" in request.args:
            blk=request.args['bname']
            cell = request.args['cnum']
            q2="UPDATE cell SET block_id='%s',cell_num='%s' WHERE cell_id='%s'" % (blk,cell,bid)
            database.updation(q2)
            return redirect(url_for('managecell'))
        return render_template('updcell.html', data=dicres)
    else:
       return redirect(url_for('login'))



@app.route('/admin/managecell/',methods=['GET','POST'])
def managecell():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE  FROM cell WHERE cell_id='%s'" % id
            database.deletion(q1)
            return redirect(url_for('managecell'))
        q = "select * from cell left join block using (block_id) left join prisons using (p_id)"
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('managecell.html',data=dicres)
    else:
       return redirect(url_for('login'))



@app.route('/get_prisblock/')
def get_value():
    if "req" in request.args:
        if "action" in request.args:
            action = request.args['action']
            q = "select * from block where p_id='%s'" % (action)
            result = database.selection(q)
            r  = ""
            for row in result:
                r = r + "<option value='%s'>%s</option>" % (row['block_id'],row['block_name'])

            return r

        else:
            return "false"
    else:
        return "Bad request"
@app.route('/admin/regcases/',methods=['GET','POST'])
def regcases():
    if (sf.is_logged_in() == True):
        if "cname" in request.form and "cdes" in request.form:
            case=request.form['cname']
            des=request.form['cdes']
            dict = {
                "case_name": case,
                "case_discription":des,

            }
            database.insertion("cases", dict)
        return render_template('cases.html')
    else:
       return redirect(url_for('login'))

@app.route('/admin/managecase/',methods=['GET','POST'])
def managecase():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE  FROM cases WHERE case_id='%s'" % id
            database.deletion(q1)
            return redirect(url_for('managecase'))
        q = "select * from cases"
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('managecase.html',data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/viewcase/',methods=['GET','POST'])
def viewcase():
    if (sf.is_logged_in() == True):
        bid = request.args['id']
        q1="select * from cases where case_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "bid":bid,
            "res":res

        }
        return render_template('viewcase.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/updcase/',methods=['GET','POST'])
def updcase():
    if (sf.is_logged_in() == True):
        bid = request.args['id']
        q1="select * from cases where case_id='%s'" % bid
        res=database.selection(q1)
        dicres = {

            "bid":bid,
            "res":res,

        }
        if "sbmt" in request.args:
            cnm=request.args['cname']
            cds = request.args['cdes']
            q2="UPDATE cases SET case_name='%s',case_discription='%s' WHERE case_id='%s'" % (cnm,cds,bid)
            database.updation(q2)
            return redirect(url_for('managecase'))
        return render_template('updcase.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/regevent',methods=['GET','POST'])
def regevent():
    if (sf.is_logged_in() == True):
        if "ename" in request.form and "edes" in request.form:
            ename=request.form['ename']
            edes=request.form['edes']
            edate=request.form['dat']
            etime=request.form['tim']
            dict={
                "eve_name":ename,
                "eve_description":edes,
                "eve_date":edate,
                "eve_time ":etime,
            }
            database.insertion("events",dict)
        return render_template('regevent.html')
    else:
       return redirect(url_for('login'))

@app.route('/admin/manageevent/',methods=['GET','POST'])
def manageevent():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE  FROM events WHERE eve_id='%s'" % id
            database.deletion(q1)
            return redirect(url_for('manageevent'))
        q = "select * from events"
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('manageevent.html',data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/viewevent/',methods=['GET','POST'])
def viewevent():
    if (sf.is_logged_in() == True):
        bid = request.args['id']
        q1="select * from events where eve_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "bid":bid,
            "res":res

        }
        return render_template('viewevent.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/updevent/',methods=['GET','POST'])
def updevent():
    if (sf.is_logged_in() == True):
        bid = request.args['id']
        q1="select * from events where eve_id='%s'" % bid
        res=database.selection(q1)
        dicres = {

            "bid":bid,
            "res":res,

        }
        if "sbmt" in request.args:
            enm=request.args['ename']
            eds = request.args['edes']
            edt = request.args['dat']
            etm = request.args['tim']
            q2="UPDATE events SET eve_name='%s', eve_description='%s',eve_date='%s',eve_time='%s' WHERE eve_id='%s'" % (enm,eds,edt,etm,bid)
            database.updation(q2)
            return redirect(url_for('manageevent'))
        return render_template('updevent.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/regstaff/',methods=['GET','POST'])
def regstaff():
    if (sf.is_logged_in() == True):
        q = "select * from prisons"
        result = database.selection(q)
        dicres = {
            "db": result

        }
        if "fname" in request.form:
            fname=request.form['fname']
            mname=request.form['mname']
            lname=request.form['lname']
            gen=request.form['gen']
            dob=request.form['dob']
            house=request.form['house']
            post=request.form['post']
            city=request.form['city']
            dist=request.form['dist']
            state=request.form['state']
            pin=request.form['pin']
            contact=request.form['contact']
            mail=request.form['mail']
            rank=request.form['rank']
            pname=request.form['pname']
            dict={
                "staff_fname":fname,
                "staff_mname":mname,
                "staff_lname":lname,
                "staff_gender":gen,
                "staff_dob":dob,
                "staff_house":house,
                "staff_post":post,
                "staff_city":city,
                "staff_district":dist,
                "staff_state":state,
                "staff_pin":pin,
                "staff_contact":contact,
                "staff_email":mail,
                "staff_rank":rank,
                "p_id":pname,
                "staff_flag":"1",
            }
            database.insertion("staff",dict)
        return render_template('regstaff.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/managestaff/',methods=['GET','POST'])
def managestaff():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE  FROM staff WHERE staff_id='%s'" % id
            database.deletion(q1)
            return redirect(url_for('managestaff'))
        q = "select * from staff left join prisons using (p_id)"
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('managestaff.html',data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/viewstaff/',methods=['GET','POST'])
def viewstaff():
    if (sf.is_logged_in() == True):
        q = "select * from prisons"
        result = database.selection(q)
        bid = request.args['id']
        q1="select * from staff left join prisons using (p_id) where staff_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res

        }
        return render_template('viewstaff.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/updstaff/',methods=['GET','POST'])
def updstaff():
    if (sf.is_logged_in() == True):
        q = "select * from prisons"
        result = database.selection(q)
        bid = request.args['id']
        q1="select * from staff left join prisons using (p_id) where staff_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res,

        }
        if "sbmt" in request.args:
            fname = request.args['fname']
            mname = request.args['mname']
            lname = request.args['lname']
            gen = request.args['gen']
            dob = request.args['dob']
            house = request.args['house']
            post = request.args['post']
            city = request.args['city']
            dist = request.args['dist']
            state = request.args['state']
            pin = request.args['pin']
            contact = request.args['contact']
            mail = request.args['mail']
            rank = request.args['rank']
            pname = request.args['pname']
            q2="UPDATE staff SET staff_fname='%s',staff_mname='%s',staff_lname='%s',staff_gender='%s',staff_dob='%s',staff_house='%s',staff_post='%s',staff_city='%s',staff_district='%s',staff_state='%s',staff_pin='%s',staff_contact='%s',staff_email='%s',staff_rank='%s',p_id='%s' WHERE staff_id='%s'" % (fname,mname,lname,gen,dob,house,post,city,dist,state,pin,contact,mail,rank,pname,bid)
            database.updation(q2)
            return redirect(url_for('managestaff'))
        return render_template('updstaff.html', data=dicres)
    else:
       return redirect(url_for('login'))



@app.route('/admin/reguser/',methods=['GET','POST'])
def reguser():
    if (sf.is_logged_in() == True):
        q = "select * from prisons"
        result = database.selection(q)
        dicres = {
            "db": result

        }
        if "fname" in request.form:
            fname=request.form['fname']
            mname=request.form['mname']
            lname=request.form['lname']
            gen=request.form['gen']
            dob=request.form['dob']
            house=request.form['house']
            post=request.form['post']
            city=request.form['city']
            dist=request.form['dist']
            state=request.form['state']
            pin=request.form['pin']
            contact=request.form['contact']
            mail=request.form['mail']
            rank=request.form['rank']
            pname=request.form['pname']
            uname=mail
            psw=''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(8))
            log={
                "username":uname,
                "password":psw,
                "user_type":"USER",
                "login_flag":"1",
            }
            res=database.insertion('login',log)
            if res>0:
                dict={
                "user_fname":fname,
                "user_mname":mname,
                "user_lname":lname,
                "user_gender":gen,
                "user_dob":dob,
                "user_house":house,
                "user_post":post,
                "user_city":city,
                "user_district":dist,
                "user_state":state,
                "user_pin":pin,
                "user_contact":contact,
                "user_email":mail,
                "user_rank":rank,
                "login_id":res,
                "user_flag":"1",
            }
            res1=database.insertion("usermaster",dict)
            if res1>0:
                uchil={
                "user_id":res1,
                "p_id":pname,
                "u_flag":"1",
                }
            database.insertion("userchild",uchil)
        return render_template('reguser.html', data=dicres)
    else:
       return redirect(url_for('login'))


@app.route('/admin/manageuser/',methods=['GET','POST'])
def manageuser():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE from login where login_id=(select login_id from usermaster where user_id='%s')" % id
            database.deletion(q1)
            q12 = "DELETE from userchild where user_id='%s'" % id
            database.deletion(q12)
            q13 = "DELETE from usermaster where user_id='%s'" % id
            database.deletion(q13)
            return redirect(url_for('manageuser'))
        q = "select * from usermaster left join userchild using (user_id) left join prisons using (p_id) "
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('manageuser.html',data=dicres)
    else:
       return redirect(url_for('login'))
@app.route('/admin/viewuser/',methods=['GET','POST'])
def viewuser():
    if (sf.is_logged_in() == True):
        q = "select * from prisons"
        result = database.selection(q)
        bid = request.args['id']
        q1="select * from usermaster left join userchild using (user_id) left join prisons using (p_id) where user_id='%s' " % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res

        }
        return render_template('viewuser.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/upduser/',methods=['GET','POST'])
def upduser():
    if (sf.is_logged_in() == True):
        q = "select * from prisons"
        result = database.selection(q)
        bid = request.args['id']
        q1="select * from usermaster left join userchild using (user_id) left join prisons using (p_id) where user_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res,

        }
        if "sbmt" in request.args:
            fname = request.args['fname']
            mname = request.args['mname']
            lname = request.args['lname']
            gen = request.args['gen']
            dob = request.args['dob']
            house = request.args['house']
            post = request.args['post']
            city = request.args['city']
            dist = request.args['dist']
            state = request.args['state']
            pin = request.args['pin']
            contact = request.args['contact']
            mail = request.args['mail']
            rank = request.args['rank']
            pname = request.args['pname']
            q2="UPDATE usermaster SET user_fname='%s',user_mname='%s',user_lname='%s',user_gender='%s',user_dob='%s',user_house='%s',user_post='%s',user_city='%s',user_district='%s',user_state='%s',user_pin='%s',user_contact='%s',user_email='%s',user_rank='%s' WHERE user_id='%s'" % (fname,mname,lname,gen,dob,house,post,city,dist,state,pin,contact,mail,rank,bid)
            database.updation(q2)
            q3="update userchild set p_id='%s' where user_id='%s'" % (pname,bid)
            database.updation(q3)
            return redirect(url_for('manageuser'))
        return render_template('upduser.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/admin/updpass/',methods=['GET','POST'])
def updpass():
    if(sf.is_logged_in()):
        if "sbmt" in request.form :
            pswd=request.form['oldp']
            new=request.form['newp']
            cnew=request.form['cnfp']
            psw=session['password']
            user="ADMIN"
            if (pswd==psw):
                q="update login set password='%s' where user_type='%s'" %(cnew,user)
                database.updation(q)
                return redirect(url_for('admin_home'))
            else:
                flash("You were entered a wrong password !!!")
                return render_template('updpass.html')
        return render_template('updpass.html')
    else:
        return redirect(url_for('login'))


@app.route('/user/updpass/',methods=['GET','POST'])
def updpassu():
    if(sf.is_logged_in()):
        if "sbmt" in request.form :
            pswd=request.form['oldp']
            new=request.form['newp']
            cnew=request.form['cnfp']
            psw=session['password']
            user=session['login_id']
            if (pswd==psw):
                q="update login set password='%s' where login_id='%s'" %(cnew,user)
                database.updation(q)
                return redirect(url_for('user_home'))
            else:
                flash("You were entered a wrong password !!!")
                return render_template('uupdpass.html')
        return render_template('uupdpass.html')
    else:
        return redirect(url_for('login'))



@app.route('/user/vieweventu/',methods=['GET','POST'])
def vieweventu():
    if (sf.is_logged_in() == True):
        bid = request.args['id']
        q1="select * from events where eve_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "bid":bid,
            "res":res

        }
        return render_template('vieweventu.html', data=dicres)
    else:
       return redirect(url_for('login'))


@app.route('/user/manageeventu/',methods=['GET','POST'])
def manageeventu():
    if(sf.is_logged_in()==True):

        q = "select * from events"
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('manageeventu.html',data=dicres)
    else:
       return redirect(url_for('login'))


@app.route('/user/managestaffu/',methods=['GET','POST'])
def managestaffu():
    if(sf.is_logged_in()==True):

        lid=session['login_id']
        q3 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res3 = database.selection(q3)
        for row in res3:
            pris = row['p_id']
        q = "select * from staff left join prisons using (p_id) where p_id='%s'" % pris
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('managestaffu.html',data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/user/viewstaffu/',methods=['GET','POST'])
def viewstaffu():
    if (sf.is_logged_in() == True):
        q = "select * from prisons"
        result = database.selection(q)
        bid = request.args['id']
        q1="select * from staff left join prisons using (p_id) where staff_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res

        }
        return render_template('viewstaffu.html', data=dicres)
    else:
       return redirect(url_for('login'))




@app.route('/user/regvisitor/',methods=['GET','POST'])
def regvisitor():
    if (sf.is_logged_in() == True):
        lid=session['login_id']
        q1="SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1=database.selection(q1)
        for row in res1:
            pris=row['p_id']
        q2 = "SELECT * FROM prisonermaster LEFT JOIN prisonerchild using (pm_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where p_id='%s'" % pris
        result = database.selection(q2)
        dicres = {
            "db": result

        }
        if "fname" in request.form:
            fname = request.form['fname']
            mname = request.form['mname']
            lname = request.form['lname']
            gen = request.form['gen']
            dob = request.form['dob']
            house = request.form['house']
            post = request.form['post']
            city = request.form['city']
            dist = request.form['dist']
            state = request.form['state']
            pin = request.form['pin']
            contact = request.form['contact']
            datee=request.form['date']
            timee=request.form['time']
            pname = request.form['pname']
            dict = {
                "v_fname": fname,
                "v_mname": mname,
                "v_lname": lname,
                "v_gender": gen,
                "v_dob": dob,
                "v_house": house,
                "v_post": post,
                "v_city": city,
                "v_district": dist,
                "v_state": state,
                "v_pin": pin,
                "v_contact": contact,
                "pm_id": pname,
                "v_date": datee,
                "v_time": timee,
            }
            database.insertion("visitors", dict)
        return render_template('regvisitor.html', data=dicres)
    else:
        return redirect(url_for('login'))

@app.route('/user/managevisitor/',methods=['GET','POST'])
def managevisitor():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE from visitors where v_id='%s'" % id
            database.deletion(q1)
            return redirect(url_for('managevisitor'))
        lid = session['login_id']
        q1 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q1)
        for row in res1:
            pris = row['p_id']
        q = "SELECT * FROM visitors left join prisonermaster using (pm_id) LEFT JOIN prisonerchild using (pm_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where p_id='%s'" % pris
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('managevisitor.html',data=dicres)
    else:
       return redirect(url_for('login'))
@app.route('/user/viewvisitor/',methods=['GET','POST'])
def viewvisitor():
    if (sf.is_logged_in() == True):
        q = "select * from prisonermaster"
        result = database.selection(q)
        bid = request.args['id']
        q1="select * from visitors left join prisonermaster using (pm_id) where v_id='%s' " % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res

        }
        return render_template('viewvisitor.html', data=dicres)
    else:
       return redirect(url_for('login'))


@app.route('/user/updvisitor/',methods=['GET','POST'])
def updvisitor():
    if (sf.is_logged_in() == True):
        lid = session['login_id']
        q12 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q12)
        for row in res1:
            pris = row['p_id']
        q21 = "SELECT * FROM prisonermaster LEFT JOIN prisonerchild using (pm_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where p_id='%s'" % pris
        result = database.selection(q21)
        bid = request.args['id']
        q1="select * from visitors left join prisonermaster using (pm_id) where v_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result,
            "bid":bid,
            "res":res,

        }
        if "sbmt" in request.args:
            fname = request.args['fname']
            mname = request.args['mname']
            lname = request.args['lname']
            gen = request.args['gen']
            dob = request.args['dob']
            house = request.args['house']
            post = request.args['post']
            city = request.args['city']
            dist = request.args['dist']
            state = request.args['state']
            pin = request.args['pin']
            contact = request.args['contact']
            pname = request.args['pname']
            q2="UPDATE visitors SET v_fname='%s',v_mname='%s',v_lname='%s',v_gender='%s',v_dob='%s',v_house='%s',v_post='%s',v_city='%s',v_district='%s',v_state='%s',v_pin='%s',v_contact='%s',pm_id='%s' WHERE v_id='%s'" % (fname,mname,lname,gen,dob,house,post,city,dist,state,pin,contact,pname,bid)
            database.updation(q2)
            return redirect(url_for('managevisitor'))
        return render_template('updvisitor.html', data=dicres)
    else:
       return redirect(url_for('login'))




@app.route('/user/regprisoner/',methods=['GET','POST'])
def regprisoner():
    if (sf.is_logged_in() == True):
        lid=session['login_id']
        q1="SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1=database.selection(q1)
        for row in res1:
            pris=row['p_id']
        q2 = "select * from block where p_id='%s'" % pris
        result1 = database.selection(q2)
        q3="select * from cases "
        result2=database.selection(q3)


        dicres = {
            "db": result2,
            "blk":result1

        }
        if "fname" in request.form:
            fname = request.form['fname']
            mname = request.form['mname']
            lname = request.form['lname']
            gen = request.form['gen']
            dob = request.form['dob']
            house = request.form['house']
            post = request.form['post']
            city = request.form['city']
            dist = request.form['dist']
            state = request.form['state']
            pin = request.form['pin']
            contact = request.form['contact']
            date1=request.form['edate']
            date2=request.form['rdate']
            cname = request.form['cname']
            cel=request.form['cel']
            dict = {
                "pm_fname": fname,
                "pm_mname": mname,
                "pm_lname": lname,
                "pm_gender": gen,
                "pm_dob": dob,
                "pm_house": house,
                "pm_post": post,
                "pm_city": city,
                "pm_district": dist,
                "pm_state": state,
                "pm_pin": pin,
                "pm_contact": contact,
                "pm_entry": date1,
                "pm_release": date2,
                "cell_id":cel,
                "pm_flag":"1"
            }
            data1=database.insertion("prisonermaster", dict)
            if data1>0 :
                pchil={
                    "pm_id":data1,
                    "case_id":cname
                }
            database.insertion("prisonerchild",pchil)
        return render_template('regprisoner.html', data=dicres)
    else:
        return redirect(url_for('login'))


@app.route('/user/manageprisoner/',methods=['GET','POST'])
def manageprisoner():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE from prisonermaster where pm_id='%s'" % id
            database.deletion(q1)
            q12 = "DELETE from prisonerchild where pm_id='%s'" % id
            database.deletion(q12)

            return redirect(url_for('manageprisoner'))
        lid = session['login_id']
        q12 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q12)
        for row in res1:
            pris = row['p_id']
        q2 = "SELECT * FROM prisonermaster LEFT JOIN prisonerchild using (pm_id) left join cases using (case_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where p_id='%s'" % pris
        result1 = database.selection(q2)
        dicres = {
            "db": result1

        }
        return render_template('manageprisoner.html',data=dicres)
    else:
       return redirect(url_for('login'))
@app.route('/user/viewprisoner/',methods=['GET','POST'])
def viewprisoner():
    if (sf.is_logged_in() == True):
        id = request.args['id']
        lid = session['login_id']
        q1 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q1)
        for row in res1:
            pris = row['p_id']
        q2 = "select * from block where p_id='%s'" % pris
        result1 = database.selection(q2)
        q3 = "select * from cases "
        result2 = database.selection(q3)
        q21 = "SELECT * FROM prisonermaster LEFT JOIN prisonerchild using (pm_id) left join cases using (case_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where pm_id='%s'" % id
        result13 = database.selection(q21)
        dicres = {
            "res": result13,
            "db": result2,
            "blk":result1

        }
        return render_template('viewprisoner.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/user/updprisoner/',methods=['GET','POST'])
def updprisoner():
    if (sf.is_logged_in() == True):
        id = request.args['id']

        lid = session['login_id']
        q1 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q1)
        for row in res1:
            pris = row['p_id']
        q2 = "select * from block where p_id='%s'" % pris
        result1 = database.selection(q2)
        q3 = "select * from cases "
        result2 = database.selection(q3)
        q21 = "SELECT * FROM prisonermaster LEFT JOIN prisonerchild using (pm_id) left join cases using (case_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where pm_id='%s'" % id
        result13 = database.selection(q21)
        dicres = {
            "res": result13,
            "db": result2,
            "blk": result1

        }
        if "sbmt" in request.form:
            fname = request.form['fname']
            mname = request.form['mname']
            lname = request.form['lname']
            gen = request.form['gen']
            dob = request.form['dob']
            house = request.form['house']
            post = request.form['post']
            city = request.form['city']
            dist = request.form['dist']
            state = request.form['state']
            pin = request.form['pin']
            contact = request.form['contact']
            date1 = request.form['edate']
            date2 = request.form['rdate']
            cname = request.form['cname']
            cel = request.form['cel']
            q2="UPDATE prisonermaster SET pm_fname='%s',pm_mname='%s',pm_lname='%s',pm_gender='%s',pm_dob='%s',pm_house='%s',pm_post='%s',pm_city='%s',pm_district='%s',pm_state='%s',pm_pin='%s',pm_contact='%s',pm_entry='%s',pm_release='%s',cell_id='%s' WHERE pm_id='%s'" % (fname,mname,lname,gen,dob,house,post,city,dist,state,pin,contact,date1,date2,cel,id)
            database.updation(q2)
            q3="update prisonerchild set case_id='%s' where pm_id='%s'" % (cname,id)
            database.updation(q3)
            return redirect(url_for('manageprisoner'))
        return render_template('updprisoner.html', data=dicres)
    else:
       return redirect(url_for('login'))



@app.route('/get_priscell/')
def get_value1():
    if "req" in request.args:
        if "action" in request.args:
            action = request.args['action']
            q = "select * from cell where block_id='%s'" % (action)
            result = database.selection(q)
            if "p_id" in request.args:
                p_id = request.args['p_id']
                qn = "select * from prisonermaster where pm_id ='%s' " % p_id
                ress=database.selection(qn)
                cell_no = ress[0]['cell_id']
                r  = ""
                for row in result:
                    if cell_no == row['cell_id']:
                        r = r + "<option selected value='%s'>%s</option>" % (row['cell_id'],row['cell_num'])
                    else:
                        r = r + "<option value='%s'>%s</option>" % (row['cell_id'], row['cell_num'])
            else:
                r = ""
                for row in result:
                    r = r + "<option value='%s'>%s</option>" % (row['cell_id'], row['cell_num'])
            return r

        else:
            return "false"
    else:
        return "Bad request"


@app.route('/user/manageprisonerduty/',methods=['GET','POST'])
def manageprisonerduty():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE from prisonerduty where pd_id='%s'" % id
            database.deletion(q1)
            return redirect(url_for('manageprisonerduty'))
        lid = session['login_id']
        q1 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q1)
        for row in res1:
            pris = row['p_id']
        q = "SELECT * FROM prisonerduty left join prisonermaster using (pm_id) LEFT JOIN prisonerchild using (pm_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where p_id='%s'" % pris
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('manageprisonerduty.html',data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/user/updprisonerduty/',methods=['GET','POST'])
def updprisonerduty():
    if (sf.is_logged_in() == True):
        lid = session['login_id']
        q12 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q12)
        for row in res1:
            pris = row['p_id']
        q2 = "SELECT * FROM prisonermaster LEFT JOIN prisonerchild using (pm_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where p_id='%s'" % pris
        result1 = database.selection(q2)
        bid = request.args['id']
        q1="select * from prisonerduty left join prisonermaster using (pm_id) where pd_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result1,
            "bid":bid,
            "res":res,

        }
        if "sbmt" in request.form:
            pname = request.form['pname']
            date1 = request.form['datee']
            time1 = request.form['timee']
            type = request.form['type']
            bid = request.form['id']
            q2="UPDATE prisonerduty SET pm_id='%s',pd_date='%s',pd_time='%s',pd_type='%s' WHERE pd_id='%s'" % (pname,date1,time1,type,bid)
            database.updation(q2)
            return redirect(url_for('manageprisonerduty'))
        return render_template('updprisonerduty.html', data=dicres)
    else:
       return redirect(url_for('login'))


@app.route('/user/regprisonerduty/',methods=['GET','POST'])
def regprisonerduty():
    if (sf.is_logged_in() == True):
        lid=session['login_id']
        q1="SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1=database.selection(q1)
        for row in res1:
            pris=row['p_id']
        q2 = "SELECT * FROM prisonermaster LEFT JOIN prisonerchild using (pm_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where p_id='%s'" % pris
        result1 = database.selection(q2)
        dicres = {
            "blk":result1

        }
        if "pname" in request.form:
            pname = request.form['pname']
            date1=request.form['datee']
            time1=request.form['timee']
            type = request.form['type']
            dict = {
                "pm_id":pname,
            "pd_date":date1,
            "pd_time":time1,
            "pd_type":type
            }
            data1=database.insertion("prisonerduty", dict)

        return render_template('regprisonerduty.html', data=dicres)
    else:
        return redirect(url_for('login'))

@app.route('/user/managestaffduty/',methods=['GET','POST'])
def managestaffduty():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE from staffduty where sd_id='%s'" % id
            database.deletion(q1)
            return redirect(url_for('managestaffduty'))
        lid = session['login_id']
        q1 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q1)
        for row in res1:
            pris = row['p_id']
        q = "SELECT * FROM staffduty left join staff using (staff_id) left join prisons using (p_id) where p_id='%s'" % pris
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('managestaffduty.html',data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/user/updstaffduty/',methods=['GET','POST'])
def updstaffduty():
    if (sf.is_logged_in() == True):
        lid = session['login_id']
        q12 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q12)
        for row in res1:
            pris = row['p_id']
        q2 = "SELECT * FROM staff where p_id='%s'" % pris
        result1 = database.selection(q2)
        bid = request.args['id']
        q1="select * from staffduty left join staff using (staff_id) where sd_id='%s'" % bid
        res=database.selection(q1)
        dicres = {
            "db": result1,
            "bid":bid,
            "res":res,

        }
        if "sbmt" in request.args:
            pname = request.args['pname']
            date1 = request.args['datee']
            time1 = request.args['timee']
            type = request.args['type']
            bid = request.args['id']
            q2="UPDATE staffduty SET staff_id='%s',sd_date='%s',sd_time='%s',sd_type='%s' WHERE sd_id='%s'" % (pname,date1,time1,type,bid)
            database.updation(q2)
            return redirect(url_for('managestaffduty'))
        return render_template('updstaffduty.html', data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/user/regstaffduty/',methods=['GET','POST'])
def regstaffduty():
    if (sf.is_logged_in() == True):
        lid=session['login_id']
        q1="SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1=database.selection(q1)
        for row in res1:
            pris=row['p_id']
        q2 = "SELECT * FROM staff where p_id='%s'" % pris
        result1 = database.selection(q2)
        dicres = {
            "blk":result1

        }
        if "pname" in request.form:
            pname = request.form['pname']
            date1=request.form['datee']
            time1=request.form['timee']
            type = request.form['type']
            dict = {
                "staff_id":pname,
            "sd_date":date1,
            "sd_time":time1,
            "sd_type":type
            }
            data1=database.insertion("staffduty", dict)

        return render_template('regstaffduty.html', data=dicres)
    else:
        return redirect(url_for('login'))
@app.route('/user/prisonerlog/',methods=['GET','POST'])
def prisonerlog():
    if (sf.is_logged_in() == True):
        lid=session['login_id']
        q1="SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1=database.selection(q1)
        for row in res1:
            pris=row['p_id']
        q2 = "SELECT * FROM prisonermaster LEFT JOIN prisonerchild using (pm_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where p_id='%s'" % pris
        result1 = database.selection(q2)
        q3="select * from logtype"
        result2=database.selection(q3)
        dicres = {
            "blk":result1,
            "db":result2

        }
        if "pname" in request.form:
            pname = request.form['pname']
            date1=request.form['date1']
            time1=request.form['time1']
            date2 = request.form['date2']
            time2 = request.form['time2']
            type = request.form['des']
            dict = {
                "pm_id":pname,
                "logtype_id":type,
                "pl_exitdate":date1,
                "pl_exittime":time1,
                "pl_entrydate":date2,
                "pl_entrytime":time2,
                "pl_status":"ACTIVE"
            }
            data1=database.insertion("prisonerlog", dict)

        return render_template('prisonerlog.html', data=dicres)
    else:
        return redirect(url_for('login'))

@app.route('/user/manageprisonerlog/',methods=['GET','POST'])
def manageprisonerlog():
    if(sf.is_logged_in()==True):
        if "id" in request.args:
            id=request.args['id']
            q1="DELETE from prisonerlog where pl_id='%s'" % id
            database.deletion(q1)
            return redirect(url_for('manageprisonerlog'))
        lid = session['login_id']
        q1 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q1)
        for row in res1:
            pris = row['p_id']
        q = "SELECT * FROM prisonerlog left join logtype using (logtype_id) left join prisonermaster using (pm_id) LEFT JOIN prisonerchild using (pm_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where p_id='%s'" % pris
        result = database.selection(q)
        dicres = {
            "db": result

        }
        return render_template('manageprisonerlog.html',data=dicres)
    else:
       return redirect(url_for('login'))

@app.route('/user/updprisonerlog/',methods=['GET','POST'])
def updprisonerlog():
    if (sf.is_logged_in() == True):
        lid = session['login_id']
        q12 = "SELECT * FROM usermaster LEFT JOIN login USING (login_id)LEFT JOIN userchild using (user_id) LEFT JOIN prisons USING (p_id) where login_id='%s'" % lid
        res1 = database.selection(q12)
        for row in res1:
            pris = row['p_id']
        q2 = "SELECT * FROM prisonermaster LEFT JOIN prisonerchild using (pm_id) LEFT JOIN cell USING (cell_id) LEFT JOIN block USING (block_id) LEFT JOIN prisons USING (p_id) where p_id='%s'" % pris
        result1 = database.selection(q2)
        bid = request.args['id']
        q1="select * from prisonerlog left join logtype using (logtype_id) left join prisonermaster using (pm_id) where pl_id='%s'" % bid
        res=database.selection(q1)
        qury="select * from logtype"
        rees=database.selection(qury)
        dicres = {
            "db": result1,
            "bid":bid,
            "res":res,
            "dbs":rees

        }
        if "sbmt" in request.form:
            pname = request.form['pname']
            date1 = request.form['date1']
            time1 = request.form['time1']
            date2 = request.form['date2']
            time2 = request.form['time2']
            type = request.form['des']
            status=request.form['status']
            bid = request.form['id']
            q22="UPDATE prisonerlog SET pm_id='%s',pl_exitdate='%s',pl_exittime='%s',pl_entrydate='%s',pl_entrytime='%s',logtype_id='%s',pl_status='%s' WHERE pl_id='%s'" % (pname,date1,time1,date2,time2,type,status,bid)
            database.updation(q22)
            return redirect(url_for('manageprisonerlog'))
        return render_template('updprisonerlog.html', data=dicres)
    else:
       return redirect(url_for('login'))





if __name__=="__main__":
    app.run("192.168.43.100",port=5000,threaded=True,debug=True)

