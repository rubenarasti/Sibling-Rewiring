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

if __name__ == '__main__':
    app.run()