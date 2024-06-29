from flask import Flask, json, request, session
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import os
import mysql.connector

db_config = {
    'host': os.getenv('DATABASE_HOST', 'db'),
    'user': os.getenv('DATABASE_USER', 'root'),
    'password': os.getenv('DATABASE_PASSWORD', 'root'),
    'database': os.getenv('DATABASE_NAME', 'sire')
}

mydb = mysql.connector.connect(**db_config)
mycursor = mydb.cursor()

def create_tables():
	mycursor.execute("CREATE TABLE IF NOT EXISTS tbl_user(user_id INT AUTO_INCREMENT PRIMARY KEY, user_name VARCHAR(45) NOT NULL, user_surname VARCHAR(45) NULL, user_school VARCHAR(80) NULL, user_email VARCHAR(150) NOT NULL UNIQUE, user_password VARCHAR (45) NOT NULL)")
	mycursor.execute("CREATE TABLE IF NOT EXISTS tbl_network(net_id INT AUTO_INCREMENT PRIMARY KEY, net_totalStudents INT NOT NULL, net_numberSiblings INT NOT NULL, net_initialt FLOAT, net_finalt FLOAT, net_l INT, net_alpha FLOAT, net_optionCooling VARCHAR(40), net_seed INT)")
	mycursor.execute("CREATE TABLE IF NOT EXISTS tbl_file(file_id INT AUTO_INCREMENT PRIMARY KEY, file_name VARCHAR(45) NOT NULL, file_directory VARCHAR(100))")
	
def create_procedure():
	mycursor.execute("DROP PROCEDURE IF EXISTS sp_createUser")
	file = open('procedure.sql','r')
	query = file.read()
	mycursor.execute(query)

def signUp():
	try:
		_name = request.form['name']
		_surname = request.form['surname']
		_email =  request.form['email']
		_school = request.form['school']
		_password = request.form['password']
			
			
		if _name and _surname and _email and _password:
			mycursor.callproc('sp_createUser',(_name,_surname,_school,_email,_password))
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
		_email = request.form['email']
		_password = request.form['password']
		
		if  _email and _password:		
			sql = ('SELECT user_id FROM tbl_user where user_email = %s and user_password = %s')
			values = (_email, _password)
			mycursor.execute(sql, values)
			users = mycursor.fetchone()
			user_exist = False
			
			if users != None:
				user_exist = True
				
	except Exception as e:
		return json.dumps({'error':'El usuario especificado no existe, compruebe su mail y contraseña'})
		
	finally:
		return user_exist
	
def addNet(totalStudents,numberSiblings):
	try: 
		if totalStudents and numberSiblings:
			sql = ('INSERT INTO tbl_network(net_totalStudents, net_numberSiblings) VALUES(%s,%s)')
			values = (totalStudents, numberSiblings)
			mycursor.execute(sql, values)
			data = mycursor.fetchall()
			if len(data) == 0:
				mydb.commit()
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	
	except Exception as e:
		return json.dumps({'error':str(e)})
		
	finally:
		mydb.commit()
	
def returnNet():
	try:
		mycursor.execute('SELECT net_id, net_totalStudents, net_numberSiblings FROM tbl_network WHERE net_id = (SELECT max(net_id) FROM tbl_network)')
		selection = mycursor.fetchone()
		_netid = selection[0]
		_totalStudents = selection[1]
		_numberSiblings = selection[2]
		
		return _netid, _totalStudents, _numberSiblings
		
	except Exception as e:
		return json.dumps({'error':str(e)})
		
	finally:
		mydb.commit()

def introduce_net_data(id, L, t0, tf, alpha, option_cooling, seed_value):
	try: 
		sql = ('UPDATE tbl_network set net_l = %s, net_initialt = %s, net_finalt = %s, net_alpha = %s, net_optionCooling = %s, net_seed = %s  where net_id = %s')
		values = (int(L), float(t0), float(tf), float(alpha), option_cooling, int(seed_value), int(id))
		mycursor.execute(sql, values)
		data = mycursor.fetchall()
		if len(data) == 0:
			mydb.commit()
		return json.dumps({'message': 'Values added successfully'})
	
	except Exception as e:
		return json.dumps({'error':str(e)})
		
	finally:
		mydb.commit()

def addFile(_filename, _directory):
	try: 
		sql = 'INSERT INTO tbl_file(file_name, file_directory) VALUES(%s,%s)'
		values = (_filename, _directory)
		mycursor.execute(sql, values)
		data = mycursor.fetchall()
		if len(data) == 0:
			mydb.commit()
			return json.dumps({'message':'File added successfully!'})
		else:
			return json.dumps({'error':str(data[0])})
	
	except Exception as e:
		return json.dumps({'error':str(e)})
		
	finally:
		mydb.commit()

def get_penultimate_file():
	try:
		mycursor.execute('SELECT file_directory FROM tbl_file WHERE file_id = ((SELECT max(file_id) FROM tbl_file) - 1)')
		_d = mycursor.fetchone()
		_directory = _d[0]
		
		mycursor.execute('SELECT file_name FROM tbl_file WHERE file_id = ((SELECT max(file_id) FROM tbl_file) - 1 )')
		_n = mycursor.fetchone()
		_name = _n[0]
		
		if _directory == '' or _name == '':
			return json.dumps({'error'})
		else: 
			return _name, _directory
	except Exception as e:
		return json.dumps({'error':str(e)})
		
	finally:
		mydb.commit()

def get_last_file():
	try:
		mycursor.execute('SELECT file_directory FROM tbl_file WHERE file_id = (SELECT max(file_id) FROM tbl_file)')
		_d = mycursor.fetchone()
		_directory = _d[0]
		
		mycursor.execute('SELECT file_name FROM tbl_file WHERE file_id = (SELECT max(file_id) FROM tbl_file)')
		_n = mycursor.fetchone()
		_name = _n[0]
		
		if _directory == '' or _name == '':
			return json.dumps({'error'})
		else: 
			return _name, _directory
	except Exception as e:
		return json.dumps({'error':str(e)})
		
	finally:
		mydb.commit()

create_tables()
create_procedure()
