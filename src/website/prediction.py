import pandas as pd
import numpy as np
from pipeline_classes import Featurizer
from sklearn.ensemble import RandomForestClassifier
import pickle

with open('../../data/final_pickled_pipe.pkl', 'rb') as f:
    pipe = pickle.load(f)

def get_predictions(df):
    """function to use pickled pipeline to get predictions on new scraped weather forecast data
    Input: pandas dataframe
    Output: numpy array of predictions
    """
    forecast_probs = pipe.predict_proba(df)
    return forecast_probs

def get_one_prediction(row: dict) -> float:
    """make a prediction for a single event, i.e. a single row from Mongo DB where scraped weather data is stored
    Input: dict
    Output: float
    """
    df = pd.DataFrame([row])
    df.drop(['_id'], axis=1, inplace=True)
    predictions = get_predictions(df)
    return predictions[0, 1]
