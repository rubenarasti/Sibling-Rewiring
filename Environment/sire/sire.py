from flask import Flask, render_template
from database import *

app = Flask(__name__)

@app.route('/')
def index():
    title = "Sire"
    user = {'nombre': 'Maria'}

    return render_template("plantillabase.html", title=title, user=user)
	
@app.route('/users', methods=['POST'])
def register_user():
    insert_user()
register_user()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/register')
def register():
    return render_template('register.html')


@app.route('/authentication',methods=['POST','GET'])
def authenticate():
   if request.method == 'POST':
       uname = request.form['username']
       passwrd = request.form['password']   
       cur = mysql.connection.cursor()
       cur.execute("SELECT username,password FROM user WHERE username=%s",[uname])
       user = cur.fetchone()
       temp = user[1]
       if len(user) > 0:
           session.pop('username',None)
           if (bcrypt.check_password_hash(temp,passwrd)) == True:  
               session['username'] = request.form['username']
               return render_template('home.html',uname=uname)
           else:
               flash('Invalid Username or Password !!')
               return render_template('login.html')
   else:
       return render_template('login.html')

@app.route('/logout')
def logout():
   session.clear()
   return render_template('login.html')
   
if __name__ == '__main__':
    app.run()