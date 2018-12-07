from flask import Flask, render_template, Response
from flask_pymongo import PyMongo
from pipeline_classes import Featurizer
import pandas as pd
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import prediction

app = Flask(__name__, static_url_path="")

app.config['MONGO_DBNAME'] = 'Snoqualmie'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Snoqualmie'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def render():
    return render_template('index.html', table = output.to_html(index=False), plot = plt.show())

def get_pred():
    """Get the predictions and data to display"""
    pass_closure = mongo.db.docs
    output = []
    data = pass_closure.find()
    df = pd.DataFrame(list(data))
    df.drop(['_id'], axis=1, inplace=True)
    predictions = prediction.get_predictions(df)
    df['probabilities'] = predictions[:,1]
    df = df.round(2)
    output = df.loc[:, ['date', 'probabilities']]
    return output

output = get_pred()

@app.route('/plot.png')
def plot_png():
    '''Generate image for display on web page'''
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    '''Create bar chart to display a visual representation of predicted probabilities'''
    fig = Figure()
    ax = output[['probabilities']].plot(kind='bar', title ="Probabilities", figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Probabilities", fontsize=12)
    ax.set_xticklabels(output['date'], rotation='vertical')
    ax.plot()
    return fig





