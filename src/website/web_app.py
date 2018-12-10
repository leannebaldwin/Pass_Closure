from flask import Flask, render_template, Response
from flask_pymongo import PyMongo
from pipeline_classes import Featurizer
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import prediction
from datetime import datetime as dt

app = Flask(__name__, static_url_path="")

app.config['MONGO_DBNAME'] = 'Snoqualmie'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Snoqualmie'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def render():
    return render_template('index.html', table = output.to_html(index=False), graph=graph)

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
    df['date'] = df.date.dt.strftime("%b %d")
    output = df.loc[:, ['date', 'probabilities']]
    return output

output = get_pred()

@app.route('/plot')
def build_plot():
    '''Create bar chart to display a visual representation of predicted probabilities'''
    ax = output[['probabilities']].plot(kind='bar', title ="Snoqualmie Pass Closure Probabilities", figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Probabilities", fontsize=12)
    ax.set_xticklabels(output['date'], rotation='vertical')
    return plt.savefig('static/images/graph')

graph = build_plot()
    







