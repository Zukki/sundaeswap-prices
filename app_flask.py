from flask import Flask, render_template, request, Response
import pandas as pd
import numpy as np
import io
import random
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure


import matplotlib
matplotlib.use('TkAgg')
matplotlib.use('Agg')
#import matplotlib.pyplot as plt

# app = Flask(__name__, static_url_path="", static_folder="static")
app = Flask(__name__)

@app.route('/')
def source():
	return render_template('home2.html', mytitle='Test Heroku Flask shitshow', firstPar='burn this, burn that')

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    Agg.FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = matplotlib.figure.Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig