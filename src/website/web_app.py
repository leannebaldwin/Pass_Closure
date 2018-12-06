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
    return render_template('index.html')

def get_pred():
    """Get the predictions and data to display"""
    pass_closure = mongo.db.docs
    output = []
    data = pass_closure.find()
    df = pd.DataFrame(data)
    df.drop(['_id'], axis=1, inplace=True)
    df['predictions'] = round(prediction.get_predictions(df), 2)
    for row in df:
        output.append({'date' : row['date'],  'probability': row['predictions']})
    return output

output = get_pred()
