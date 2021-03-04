from flask import Flask, json, request, session
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="Password", database="prueb")


mycursor = mydb.cursor()

def create_table():
	mycursor.execute("CREATE TABLE IF NOT EXISTS tbl_user(user_id INT AUTO_INCREMENT PRIMARY KEY,user_name VARCHAR(45) NULL, user_surname VARCHAR(45) NULL,user_username VARCHAR(45) NULL,user_password VARCHAR (45) NULL)")
	
def create_procedure():
	mycursor.execute("DROP PROCEDURE IF EXISTS sp_createUser")
	file = open('procedure.txt','r')
	query = file.read()
	mycursor.execute(query)

def signUp():
	try:
		_name = request.form['name']
		_surname = request.form['surname']
		_username =  request.form['username']
		_password = request.form['password']
			
			
		if _name and _surname and _username and _password:
			mycursor.callproc('sp_createUser',(_name,_username,_surname,_password))
			data = mycursor.fetchall()
				
			if len(data) == 0:
				mydb.commit()
				return json.dumps({'message':'User created successfully !'})
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	
	except Exception as e:
		return json.dumps({'error':str(e)})
		
	finally:
		mydb.commit()


def logIn():
	try:
		_username = request.form['username']
		_password = request.form['password']
		
		if  _username and _password:		
			sql = ('SELECT user_id FROM tbl_user where user_username = %s and user_password = %s')
			values = (_username, _password)
			mycursor.execute(sql, values)
			users = mycursor.fetchone()
			user_exist = False
			
			if users != None:
				user_exist = True
				
	except Exception as e:
		return json.dumps({'error':str(e)})
		
	finally:
		return user_exist
	

create_table()
create_procedure()