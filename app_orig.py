from flask import Flask, render_template, request

# app = Flask(__name__, static_url_path="", static_folder="static")
app = Flask(__name__)

@app.route('/')
def source():
	return render_template('home.html', mytitle='Test Heroku Flask shitshow', firstPar='burn this, burn that')