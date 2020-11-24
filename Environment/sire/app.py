from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = "Sire"
    user = {'nombre': 'Maria'}

    return render_template("plantillabase.html", title=title, user=user)