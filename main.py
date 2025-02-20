from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/about")
def about():
    return render_template("about.html")

app.run(debug=True)
