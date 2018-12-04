import pandas as pd 
import numpy as np 
from sklearn.base import BaseEstimator, TransformerMixin

class Featurizer(BaseEstimator, TransformerMixin):
    """Transform incoming df to fit into model"""
   
    def __init__(self, cols=None):
        """INPUT: an optional cols list of columns to select"""
        if cols==None:
            self.cols = ['date', 'temp', 'precipitation', 'overcast', 'poor_visibility', 'windy']
        else:
            self.cols = cols

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """tranform incoming training or test"""
        df = X.copy()
        date_column = pd.Series(df.date)
        month_day_of_week = pd.DataFrame({"year": date_column.dt.year,
                                        "month": date_column.dt.month, 
                                        "day": date_column.dt.day,
                                        "dayofweek": date_column.dt.dayofweek})
        month_day_of_week.dayofweek[month_day_of_week.dayofweek == 0] = 'Monday'
        month_day_of_week.dayofweek[month_day_of_week.dayofweek == 1] = 'Tuesday'
        month_day_of_week.dayofweek[month_day_of_week.dayofweek == 2] = 'Wednesday'
        month_day_of_week.dayofweek[month_day_of_week.dayofweek == 3] = 'Thursday'
        month_day_of_week.dayofweek[month_day_of_week.dayofweek == 4] = 'Friday'
        month_day_of_week.dayofweek[month_day_of_week.dayofweek == 5] = 'Saturday'
        month_day_of_week.dayofweek[month_day_of_week.dayofweek == 6] = 'Sunday'
        month_day_of_week = pd.get_dummies(month_day_of_week)
        df.reset_index()
        month_day_of_week.index = df.index
        features = pd.concat([df, month_day_of_week], axis=1)
        return features