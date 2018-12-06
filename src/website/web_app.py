from flask import Flask, render_template
from flask_pymongo import PyMongo
from pipeline_classes import Featurizer
import pandas as pd
import prediction

app = Flask(__name__, static_url_path="")

app.config['MONGO_DBNAME'] = 'Snoqualmie'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Snoqualmie'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def render():
    return render_template('index.html', table = get_pred())

def get_pred():
    """Get the predictions and data to display"""
    pass_closure = mongo.db.docs
    output = []
    data = pass_closure.find()
    df = pd.DataFrame(list(data))
    df.drop(['_id'], axis=1, inplace=True)
    predictions = prediction.get_predictions(df)
    df['predictions'] = predictions[:,1]
    df = df.round(2)
    output = df.loc[:, ['date', 'predictions']]
    return output.to_html()


