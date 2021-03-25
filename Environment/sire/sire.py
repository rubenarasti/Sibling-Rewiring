import os
from flask import Flask, render_template, request, flash, redirect, jsonify, send_file
from flask_bootstrap import Bootstrap
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from werkzeug.utils import secure_filename
from database import *
from randomNetCreation import RandomNet
from fileNetCreation import FileNet

app = Flask(__name__)
bootstrap = Bootstrap(app)

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
	user_created = signUp()
	if user_created == json.dumps({'message':'User created successfully !'}):
		return render_template('login.html')
	return jsonify({'NOT': x})

@app.route('/user_home')
def show_user_home():
	return render_template('user_home.html')
	
@app.route('/selection')
def show_selection_page():
	return render_template('selection.html')

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
	
	ALLOWED_EXTENSIONS = set(['gexf', 'csv'])
	
	def allowed_file(filename):
		return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

	if request.method == 'POST':
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
			
		files = request.files.getlist('files[]')
		
		if len(files) != 2:
			flash('Debe introducir dos archivos.')
			return render_template('upload.html')
		
		name1 = files[0].filename
		extension1 = files[0].filename.rsplit('.', 1)[1].lower()
		name2 = files[1].filename
		extension2 = files[1].filename.rsplit('.', 1)[1].lower()
		
		if (extension1 == 'gexf' and extension2 == 'csv') or (extension2 == 'gexf' and extension1 == 'csv'):
			for file in files:
				if file and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					flash('Los archivos permitidos son .gexf o .graphml')
					return render_template('upload.html')
		else:
			flash('Debe introducir un .csv y un grafo.')
			return render_template('upload.html')
		
		file1 = addFile(name1, os.path.join(app.config['UPLOAD_FOLDER'], name1))
		file2 = addFile(name2, os.path.join(app.config['UPLOAD_FOLDER'], name2))
		
		if file1 == json.dumps({'message':'File added successfully!'}) and file2 == json.dumps({'message':'File added successfully!'}):
			file1_name, file1_directory = get_last_file()
			file2_name, file2_directory = get_penultimate_file()
				
			n1, ext1 = os.path.splitext(file1_name)
			n2, ext2 = os.path.splitext(file2_name)
			
			if ext1 == '.gexf':
				G = nx.read_gexf(file1_directory)
			elif ext1 == '.csv':
				df = pd.read_csv(file1_directory, index_col=0)
			if ext2 == '.gexf':
				G = nx.read_gexf(file2_directory)
			elif ext2 == '.csv':
				df = pd.read_csv(file2_directory, index_col=0)
		
			net = FileNet(df, G)
			schoolyear_class = net.create_schoolyear_class_network()
					
			pos=nx.circular_layout(schoolyear_class)
			nx.draw(schoolyear_class, pos)
			node_labels = nx.get_node_attributes(schoolyear_class,'Nombre')
			nx.draw_networkx_labels(schoolyear_class, pos, labels = node_labels)
			
		flash('Archivo subido con éxito.')
		return render_template('success.html', name=plt.show())

	
@app.route("/downloadfile", methods=['GET'])
def show_download():
	return render_template('downloads.html')
	
@app.route("/download")
def download():
	path = os.getcwd()
	UPLOAD_FOLDER = os.path.join(path, 'uploads')
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	p = "/randomGraphuploaded.gexf"
	return send_file(app.config['UPLOAD_FOLDER']+ p, as_attachment=True)

@app.route('/showData')
def show_introduce_data():
    return render_template('introduce_data.html')
	
@app.route('/showData/data', methods=['POST', 'GET'])
def addNetwork():
	_totalStudents = request.form['totalStudents']
	_numberSiblings = request.form['numberSiblings']
		
	totalStudents, numberSiblings = addNet(_totalStudents, _numberSiblings)
	
	net = RandomNet(totalStudents,numberSiblings)
	net.create_initial_network()
	schoolyear_class = net.create_schoolyear_class_network()
	
	pos=nx.kamada_kawai_layout(schoolyear_class)
	nx.draw(schoolyear_class, pos)
	node_labels = nx.get_node_attributes(schoolyear_class,'Nombre')
	nx.draw_networkx_labels(schoolyear_class, pos, labels = node_labels)
	
	return render_template('success.html', name = plt.show())
	


@app.route('/logout')
def logout():
	session.clear()
	return render_template('login.html')
	
	
	
if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()
