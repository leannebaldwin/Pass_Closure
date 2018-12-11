from flask import Flask, render_template, Response, make_response
from flask_pymongo import PyMongo
from pipeline_classes import Featurizer
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import prediction
from datetime import datetime as dt
from io import BytesIO

app = Flask(__name__, static_url_path="")

app.config['MONGO_DBNAME'] = 'Snoqualmie'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Snoqualmie'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def render():
    return render_template('index.html', table = output.to_html(index=False))

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
    df['date'] = df.date.dt.strftime("%a %b %d")
    output = df.loc[:, ['date', 'probabilities']]
    return output

output = get_pred()

@app.route('/plot.png')
def build_plot():
    '''Create bar chart to display a visual representation of predicted probabilities'''
    ax = output[['probabilities']].plot(kind='bar', title ="Snoqualmie Pass Closure Probabilities", figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Probabilities", fontsize=12)
    ax.set_xticklabels(output['date'], rotation='vertical')
    f = BytesIO()
    plt.savefig(f)
    image_data = f.getvalue()
    response = make_response(image_data)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='plot.png')
    return response


    







