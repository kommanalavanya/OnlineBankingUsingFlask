#from django.shortcuts import render
from flask import Flask, render_template, request,session,url_for
import string,smtplib,random
import mysql.connector
app = Flask(__name__)


db=mysql.connector.connect(database="yourdatabasename",user="yourusername",password="yourpasswordname")
c=db.cursor()

@app.route("/")
def myroot():
    return render_template("index.html")

@app.route("/adminLogin")
def adminLogin():
	return render_template("adminLogin.html")

@app.route("/updatecustomer", methods=['POST'])
def updatecustomer():
        id=request.form['accno']
        c.execute("select * from customers where accno="+id)
        data=c.fetchall()
        #data is tuples in a list
        return render_template("updatecustomer.html",d=data)



@app.route("/updatecustomerDB", methods=['POST'])
def updatecustomerDB():
        t1=request.form['name']
        t2=request.form['mail']
        t3=request.form['contact']
        t4=request.form['address']
        t5=request.form['bal']
        t6= request.form['accno']

        sql = "update customers set name=%s,mail=%s,contact=%s,address=%s,bal=%s where accno = %s"
        data = (t1,t2,t3,t4,t5,t6)
        c.execute(sql,data)
        db.commit()
        c.execute("select * from customers")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("viewcustomer.html",d=data)

@app.route("/deletecustomer", methods=['POST'])
def deletecustomer():
    accno=request.form['accno']
    sql="delete from customers where accno="+accno
    c.execute(sql)
    db.commit()
    c.execute("select * from customers")
    data=c.fetchall()
    
    return render_template("viewcustomer.html",d=data)



@app.route("/userLogin")
def userLogin():
	return render_template("userLogin.html")

@app.route("/logout")
def logout():
	return render_template("index.html")


@app.route("/viewcustomer")
def viewcustomer(): 
    c.execute("select *from customers")
    data=c.fetchall()
    return render_template("viewcustomer.html",d=data)


@app.route("/adminLoginDB", methods=['POST'])
def adminLoginDB():
        un=request.form['uname']
        pwd=request.form['pwd']

        if un=='admin' and pwd=='admin':
                return render_template("adminHomePage.html")
        else:
                return render_template("adminLogin.html")

@app.route("/UserReg")
def UserReg():
    return render_template("UserReg.html")

@app.route("/userRegDB",methods=['POST'])
def userRegDB():
                characters = list(string.ascii_letters + string.digits + "!@#$%^&*")
                dig=str(random.randint(111111,999999))
                
                random.shuffle(characters)
                p=[]
                for i in range(7):
                        p.append(random.choice(characters))

                s1="".join(p)/#you can send this password to usermail (google it how to send)
                e=request.form['mail']
               

                v1=request.form['name']
                v2=request.form['mail']
                v3=request.form['contact']
                v4=request.form['address']
                v5=request.form['bal']     
                pd=s1
                sql="insert into customers(bal,name,mail,contact,address,password,accno) values("+str(v5)+",'"+v1+"','"+v2+"','"+v3+"','"+v4+"','"+pd+"','"+dig+"')"
                c.execute(sql)
                db.commit()
                return render_template("UserReg.html",res="successfully added")

@app.route("/customerlogindb",methods=['POST'])
def customerlogindb():
        em=request.form['uname']
        pwd=request.form['pwd']
        sql="SELECT * FROM `customers` WHERE mail='"+em+"' and password='"+pwd+"'"
        c.execute(sql)
        d=c.fetchall()
        if len(d)>0:
                session['accno']=d[0][1]
                return render_template("customerhomepage.html")
        else:
                return render_template("userLogin.html",result='Invalid login or password. Please try again') 

@app.route("/customerdetails")
def customerdetails():
        i=session['accno']
     
        sql="SELECT * FROM `customers` WHERE accno="+str(i)
       
        c.execute(sql)
        data=c.fetchall()
        return render_template('customerdetails.html',d=data)

@app.route("/viewbalance")
def viewbalance():
        i=session['accno']
     
        sql="SELECT * FROM `customers` WHERE accno="+str(i)
       
        c.execute(sql)
        data=c.fetchall()
        return render_template('viewbalance.html',d=data)

@app.route("/transferAmount")
def transferAmount():
       return render_template("transferAmount.html")

@app.route("/mtransfer",methods=['POST'])
def mtransfer():
           
          acc=request.form['accno']
          amt=request.form['bal']
          c.execute("select *from customers")
          data=c.fetchall()
          for row in data:
              if row[1]==session['accno']:
                  t_bal=row[6]
                  break
          if t_bal<float(amt):
                return render_template("transferAmount.html",res="Insufficient balance to transfer")
          elif float(amt)<0:
                return render_template("transferAmount.html",res="Please Enter Valid amount")
          elif acc==session['accno']:
                return render_template("transferAmount.html",res="Please Enter Receivers accountnumber")
          else:
                t_bal=t_bal-float(amt)
                sql = "update customers set bal=%s where accno = %s"
                data = (t_bal,session['accno'])
                c.execute(sql,data)
                db.commit()
                c.execute("select *from customers")
                data=c.fetchall()
                for row in data:
                        if row[1]==acc:
                                t_bal=float(amt)+row[6]
                                sql = "update customers set bal=%s where accno = %s"
                                data = (t_bal,acc)
                                c.execute(sql,data)
                                db.commit()
                                dig="txn"+str(random.randint(111111,999999))
                                sql="insert into transfer(sendacc,recacc,amount,transactionid) values('"+session['accno']+"','"+acc+"','"+amt+"','"+dig+"')"
                                c.execute(sql)
                                db.commit()
                                return render_template("transferAmount.html",res="successfully transferred")
                                
                
@app.route("/updatecust", methods=['POST'])
def updatecust():
        id=request.form['accno']
        c.execute("select * from customers where accno="+id)
        data=c.fetchall()
        #data is tuples in a list
        return render_template("updatecust.html",d=data)               


@app.route("/updatecustDB", methods=['POST'])
def updatecustDB():
        t1=request.form['name']
        t2=request.form['mail']
        t3=request.form['contact']
        t4=request.form['address']
        t6=session['accno']

        sql = "update customers set name=%s,mail=%s,contact=%s,address=%s where accno = %s"
        data = (t1,t2,t3,t4,t6)
        c.execute(sql,data)
        
        c.execute("select * from customers where accno="+t6)
        data=c.fetchall()
        #data is tuples in a list
        return render_template("customerdetails.html",d=data)

@app.route("/statement")
def statement():
        i=session['accno']
     
        sql="SELECT * FROM `transfer` WHERE sendacc="+str(i)
       
        c.execute(sql)
        data=c.fetchall()
        return render_template('statement.html',d=data)

@app.route("/viewtransactions")
def viewtransactions():
        c.execute("select *from transfer")
        data=c.fetchall()
        return render_template("viewtransactions.html",d=data)

              
@app.route("/About")
def contact():
    return render_template("About.html")      
          

if __name__=='__main__':
    app.secret_key='enter any 4 digit secret key'
    app.run(port=2001)