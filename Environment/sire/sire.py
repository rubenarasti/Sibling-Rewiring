import os
import random
from flask import Flask, render_template, request, flash, redirect, jsonify, send_file
from flask_bootstrap import Bootstrap
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from werkzeug.utils import secure_filename
from database import *
import randomNetCreation as randomNet
import fileNetCreation as fileNet
from function import *
from deap import base

app = Flask(__name__)
bootstrap = Bootstrap(app)
 
schyear_class = nx.Graph() 
matrix_siblings = []

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

@app.route('/showSingup/register', methods=['POST','GET'])
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
	global schyear_class
	global matrix_siblings
	
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
					flash('Los archivos permitidos son .gexf y .csv')
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
		
			schoolyear_class = fileNet.create_schoolyear_class_network(df, G)
			schyear_class = schoolyear_class
			matrix_siblings = df.values
			
			_totalStudents = len(G.nodes())
			_numberSiblings = len(df)
			
			addNet(_totalStudents, _numberSiblings)
			
		return render_template('random_advanced.html')

	
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
	global schyear_class
	global matrix_siblings
	
	_totalStudents = int(request.form['totalStudents'])
	_numberSiblings = int(request.form['numberSiblings'])
		
	addNet(_totalStudents, _numberSiblings)
	
	randomNet.create_initial_network(_totalStudents,_numberSiblings)
	schoolyear_class = randomNet.create_schoolyear_class_network()
	schyear_class = schoolyear_class
	randomNet.create_siblings_matrix()
	matrix_siblings = randomNet.__siblingsMatrix
	
	return render_template('random_advanced.html')
	
@app.route('/showSelection')
def show_random_advanced():
    return render_template('random_advanced.html')

@app.route('/showSelection/randomAdvanced', methods=['POST', 'GET'])
def pick_option():
	selected_option = None
	selected_option = request.form.get('options')
	values = []
	
	if selected_option == 'default':
		tf = random.uniform(0.05, 0.01)
		alpha = random.uniform(0.8, 0.99)
		l = random.randint(10,50)
		option_cooling = 6
		seed_value = random.randint(0,10)
		percentage_component = 60
		
		cooling_sequence = change_number_to_cooling_sequence(option_cooling)
		
		net_id, totalStudents, numberSiblings = returnNet()
		
		initial_t, initial_neighbour, ini_fmax, best_neighbour, current_fmax = solve_simulated_annealing(schyear_class,matrix_siblings,numberSiblings,totalStudents,l,tf, alpha ,int(option_cooling), seed_value, percentage_component)
		
		introduce_net_data(net_id, l, initial_t, tf, alpha, cooling_sequence, seed_value)
		
		pos=nx.kamada_kawai_layout(schyear_class)
		nx.draw(schyear_class, pos)
		node_labels = nx.get_node_attributes(schyear_class,'Nombre')
		nx.draw_networkx_labels(schyear_class, pos, labels = node_labels)
		
		plt.savefig('schyear_class_default', dpi=None, facecolor='w', edgecolor='w', orientation='portrait')
		plt.close('all')
		
		return render_template('results.html', name = 'JOLA', initial_neighbour = initial_neighbour, ini_fmax = ini_fmax, best_neighbour = best_neighbour, current_fmax = current_fmax)
	elif selected_option == 'advanced':
		return render_template('advanced.html')
	
	if selected_option == None:
		flash('Debe seleccionar una opción')
		return render_template('random_advanced.html')	

@app.route('/advancedOptions', methods=['POST', 'GET'])
def advanced_option():
	alpha = 0
	seed_value = random.randint(0,10)
	
	_l = request.form['l']
	_tf = request.form['tf']
	_coolingSeq = request.form['cooling_sequence']
	_percentage = request.form['percentage_component']
	
	l = int(_l)
	tf = float(_tf)
	option_cooling = int(_coolingSeq)
	percentage_component = int(_percentage)
	
	if l < 0:
		flash('L debe ser entero positivo')
		return render_template('advanced.html')
	
	if tf == 0:
		flash('tf no puede ser 0')
		return render_template('advanced.html')
		
	if percentage_component > 100:
		flash('El porcentaje no puede ser mayor de 100')
		return render_template('advanced.html')
	
	if option_cooling == 3:
		alpha = 20 
	elif option_cooling == 6:
		alpha = random.uniform(0.8, 0.99)
	
	cooling_sequence = change_number_to_cooling_sequence(option_cooling)
	net_id, totalStudents, numberSiblings = returnNet()
		
	initial_t, initial_neighbour, ini_fmax, best_neighbour, current_fmax = solve_simulated_annealing(schyear_class,matrix_siblings,numberSiblings,totalStudents,l,tf, alpha ,int(option_cooling), seed_value, percentage_component)
		
	introduce_net_data(net_id, l, initial_t, tf, alpha, cooling_sequence, seed_value)
		
	pos=nx.kamada_kawai_layout(schyear_class)
	nx.draw(schyear_class, pos)
	node_labels = nx.get_node_attributes(schyear_class,'Nombre')
	nx.draw_networkx_labels(schyear_class, pos, labels = node_labels)
		
	plt.savefig('schyear_class_advanced', dpi=None, facecolor='w', edgecolor='w', orientation='portrait')
	plt.close('all')
	
	return render_template('results.html', name = '', initial_neighbour = initial_neighbour, ini_fmax = ini_fmax, best_neighbour = best_neighbour, current_fmax = current_fmax)

def change_number_to_cooling_sequence(number):
	if number == 1:        
		cooling_sequence = 'linear_cooling_sequence'
	elif number == 3:
		cooling_sequence = 'logarithmic_cooling_sequence'
	elif number == 4:
		cooling_sequence = 'cauchy_cooling_sequence'
	elif number == 5:
		cooling_sequence = 'modified_cauchy_cooling_sequence'
	elif number == 6:
		cooling_sequence = 'geometrical_cooling_sequence'
	
	return cooling_sequence
	
@app.route('/logout')
def logout():
	session.clear()
	return render_template('login.html')
	
	
	
if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()
