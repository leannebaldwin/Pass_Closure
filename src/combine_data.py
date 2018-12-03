import pandas as pd
from pass_data_clean import clean_pass_data

pass_closure_df = clean_pass_data('../data/Cumulative_Snoqualmie_Pass_Delay_Closures_1992_2018.xlsx')

def get_pass_closure(date_time):
    """take a date_time and check if it is between the start and end times of a closure event
    input: datetime
    output: boolean
    """
    start_end_times = list(zip(pass_closure_df.start_time, pass_closure_df.end_time))
    for row in start_end_times:
        if row[0] <= date_time <= row[1]:
            return True
    return False

def add_pass_closed(df):
    """take the weather df and add a new column for whether or not the pass is closed at each date_time
    input: pandas dataframe
    output: pandas dataframe
    """
    df['pass_closed'] = df['date'].map(get_pass_closure)
    return df

def aggregate_data_to_daily(df):
    """take the combined df and aggregate the data into daily rather than hourly data to be used to train the model
    input: pandas dataframe
    output: pandas dataframe
    """
    daily_df = df.resample("D").agg({'temp':'mean','precipitation':'max', 'overcast':'max', 'poor_visibility':'max', 'windy':'max', 'pass_closed':'max'})
    daily_df.dropna(inplace=True)
    return daily_df
