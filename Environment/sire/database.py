import mysql.connector

siredb = mysql.connector.connect(host="localhost", user="root", passwd="mysqlserver", database="sire")

cursor = siredb.cursor()

def create_table():
	cursor.execute("CREATE TABLE usersBD(name VARCHAR(30), surname VARCHAR(30), password VARCHAR (30)")
	siredb.commit()

def insert_user():
    sql = "INSERT INTO users(name, surname, password) VALUES (%s,%s,%s)"
    val = ("Pepe", "Ojeda", "passwd")
    cursor.execute(sql, val)
	
    siredb.commit()

