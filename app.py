from flask import Flask

app = Flask(__name__)

@app.route('/')
def source():
	html = 'Heroku sucks big time'
	return html