import pandas as pd
from pass_data_clean import clean_pass_data

pass_closure_df = clean_pass_data('../data/Cumulative_Snoqualmie_Pass_Delay_Closures_1992_2018.xlsx')

def get_pass_closure(date_time):
    """take a date_time and check if it is between the start and end times of a closure event
    input: datetime
    output: boolean
    """
    for row in pass_closure_df:
        if row.start_time < date_time < row.end_time:
            return True
    return False

def add_pass_closed(df):
    """take the weather df and add a new column for whether or not the pass is closed at each date_time
    input: pandas dataframe
    output:pandas dataframe
    """
    for row in df:
        df['pass_closed'] = get_pass_closure(row.date)
    return df