from flask import Flask, render_template
from flask_pymongo import PyMongo
#import prediction

app = Flask(__name__, static_url_path="")

app.config['MONGO_DBNAME'] = 'Snoqualmie'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Snoqualmie'

mongo = PyMongo(app)

@app.route('/')
def render():
    return render_template('index.html', title = 'Snoqualmie Pass Closure Forecaster')

'''@app.route('/', methods=['GET'])  
def index():
    """Get the predictions and data to display"""
    pass_closure = mongo.db.docs
    output = []
    data = pass_closure.find()
    for row in data:
        pred = round(prediction.get_one_prediction(row), 2)
        output.append({'date' : row['date'],  'probability of closure': pred})
    """populate table to display"""
    table = render_template('table.html', rows = output)
    """Return the main page."""
    return render_template('index.html', table = table)'''
