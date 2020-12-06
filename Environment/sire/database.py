import mysql.connector

siredb = mysql.connector.connect(host="localhost", user="root", passwd="mysqlserver", database="sire")

cursor = siredb.cursor()

def insert_user():
    sql = "INSERT INTO users (name, surname, password) VALUES (%s,%s,%s)"
    val = ("Maria", "Ojeda", "passwd")
    cursor.execute(sql, val)
	
    siredb.commit()
	
    print(cursor.rowcount, "record inserted.")
    return 'ok'

insert_user()