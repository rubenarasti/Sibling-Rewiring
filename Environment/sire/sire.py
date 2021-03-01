import os
from flask import Flask, render_template, request, flash, redirect, jsonify
from werkzeug.utils import secure_filename
from database import *

app = Flask(__name__)

@app.route('/')
def index():
    title = "Sire"
    user = {'nombre': 'Maria'}

    return render_template('plantillabase.html', title=title, user=user)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/LogInDB', methods=['POST', 'GET'])
def logInDB():
	exist = logIn()
	if exist:
		return render_template('user_home.html')
	return jsonify({'message': exist})

@app.route('/showSignUp')
def showSignUp():
    return render_template('register.html')

@app.route('/showLogin/register', methods=['POST','GET'])
def register():
    signUp()
    return jsonify({'ok': True})

@app.route('/user_home')
def show_user_home():
	return render_template('user_home.html')

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    path = os.getcwd()
    UPLOAD_FOLDER = os.path.join(path, 'uploads')
    
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = set(['gexf'])
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No se ha seleccionado ningún archivo')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Archivo subido con éxito.')
            return render_template('success.html')
        else:
            flash('Los archivos permitidos son .gexf')
            return render_template('upload.html')
    return render_template('success.html', name = file.filename)



@app.route('/logout')
def logout():
	session.clear()
	return render_template('login.html')
	
	
if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()