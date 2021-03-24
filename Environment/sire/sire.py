import os
from flask import Flask, render_template, request, flash, redirect, jsonify, send_file
from flask_bootstrap import Bootstrap
import networkx as nx
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
from database import *
from netCreation import RandomNet

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
	ALLOWED_EXTENSIONS = set(['gexf', 'graphml'])
	def allowed_file(filename):
		return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

	if request.method == 'POST':
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
			x = addFile(file.filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))
			if x == json.dumps({'message':'File added successfully!'}):
				file_name, file_directory = get_last_file()
				
				n, extension = os.path.splitext(file_name)
				if extension == '.gexf':
					G = nx.read_gexf(file_directory)
				elif extension == '.graphml':
					return ('PROXIMAMENTE')
					#G = nx.read_graphml(file_directory)
					
				totalStudents = len(G.nodes())
				numberSiblings = 250
				
				net = RandomNet(totalStudents,numberSiblings)
				net.create_initial_network()
				schoolyear_class = net.create_schoolyear_class_network()
				
				pos=nx.kamada_kawai_layout(schoolyear_class)
				nx.draw(schoolyear_class, pos)
				node_labels = nx.get_node_attributes(schoolyear_class,'Nombre')
				nx.draw_networkx_labels(schoolyear_class, pos, labels = node_labels)
				
				addNet(totalStudents, numberSiblings)
				
				return render_template('success.html', name=plt.show())
				
			else:
				return render_template('upload.html')
		else:
			flash('Los archivos permitidos son .gexf o .graphml')
			return render_template('upload.html')

	
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
