import pandas as pd
import numpy as np
from pipeline_classes import Featurizer
from weather_data_clean import clean_weather_data
from pass_data_clean import clean_pass_data
from combine_data import get_pass_closure, add_pass_closed, true_false_to_one_zero, aggregate_data_to_daily
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import pickle

def get_data():
    """function to get all the original data that is required to train the model
    Output: pandas dataframe to use to train model"""
    weather_df = clean_weather_data('../data_exploration/ASOS_stampede_pass/SMP-2.txt')
    combined_df = add_pass_closed(weather_df)
    combined_df = true_false_to_one_zero(combined_df)
    daily_df = aggregate_data_to_daily(combined_df)
    return daily_df

def get_training_data():
    """get the training data that used to train the model
    Output: X, y used to train the model"""
    df = get_data()
    y = np.array(df['pass_closed'])
    df= df.drop('pass_closed', axis=1)
    X = np.array(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
    return X_train, X_test, y_train, y_test

def pass_pipeline():
    """instantiate a pipeline object"""
    pipeline = Pipeline([
        ('featurizer', Featurizer()),
        ('model', RandomForestClassifier(n_estimators=600, 
                                         max_depth=40))
        ])
    return pipeline

def pickle_pipeline(pipeline, output_name):
    """Save fitted pipeline to pickle file"""
    with open(output_name, 'wb') as f:
        pickle.dump(pipeline, f)
