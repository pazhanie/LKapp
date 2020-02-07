from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)
app.secret_key = 'LKapp'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'TODO'

mysql = MySQL(app)

@app.route('/LKapp/', methods=['GET', 'POST'])
def login(): 
    msg='LeanKloud , Welcomes you..! 🙏'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM credentials WHERE username = %s AND password = %s', (username, password))
        res=cursor.fetchone()
        if res:
            return render_template('admin.html')
        cursor.execute('SELECT * FROM credent_std WHERE username = %s AND password = %s', (username, password))
        res=cursor.fetchone()
        if res:
            return render_template('viewer.html')
        else:
            msg='Incorrect username/password!'
    return render_template('index.html',msg=msg)
    
    
    
@app.route('/add',methods=['POST'])
def add():
    details=request.form['details']
    due_by=request.form['due_date']
    cur_status='Not started'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("insert into TODOLIST values (NULL,%s,%s,%s)",(details,due_by,cur_status))
    mysql.connection.commit()
    msg = 'TODO Created..!'
    return render_template('admin.html',msg=msg)
   
@app.route('/find',methods=['GET', 'POST'])
def find():
    id = request.form['ID']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM TODOLIST WHERE ID = %s", (id))
    data=cursor.fetchall()
    return render_template('admin.html',results=data)
  
@app.route('/change',methods=['GET', 'POST'])
def change():
    id = request.form['ID']
    duedate = request.form['due']
    status = request.form['status']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE TODOLIST SET due_by=%s,status=%s WHERE ID=%s",(duedate,status,id))
    mysql.connection.commit()
    msg = 'Your TODO has been changed..!'
    return render_template('admin.html',msg=msg)

@app.route('/view',methods=['GET', 'POST'])
def view():
     opt = request.form['option']
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute("SELECT * FROM TODOLIST WHERE STATUS like %s", [opt])
     data=cursor.fetchall()
     return render_template('viewer.html',results=data)
    
    
  
    
    
if __name__== '__Main__':
    app.run(debug=True)
        