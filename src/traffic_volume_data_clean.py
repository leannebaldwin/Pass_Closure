import pandas as pd

def clean_volume_data(filename):
    """Take snoqualmie pass PTR traffic volume data and clean it
    input: csv file
    output: pandas dataframe
    """

    data = pd.read_csv(filename)

    #Rename some of the columns
    data.rename(columns={'TravelDirection':'direction', 'Date':'date', 'DayOfWeek':'day'}, inplace=True)

    #Create a pandas series from the date column
    date = pd.to_datetime(data['date'])

    #Rename the row values for the direction column
    data.direction[data.direction == 'Eastbound'] = 'EB'
    data.direction[data.direction == 'Westbound'] = 'WB'

    #Create a pandas series for direction with true if westbound and false if eastbound
    westbound = pd.Series([True if value == 'WB' else False for value in data.direction])

    #Ensure that the pandas series have the same index
    westbound.index = date.index

    #Drop unwanted columns from dataframe
    data = data.drop(['SiteId', 'SiteLocation', 'date', 'direction'], axis=1)
    
    #Concatenate created series with remaining columns in dataframe to create a new dataframe
    df = pd.concat([date, westbound, data], axis=1)
    
    #Rename column
    df.rename(columns={0:'westbound'}, inplace=True)
    return df

def get_correct_dates(df):
    """Take Snoqualmie pass PTR 903 data and remove unwanted rows to be able to concatenate with PTR 901 data
    input: pandas dataframe
    output: pandas dataframe
    """
    cleaned_df = df[(df['date'] > '2017-12-31') & (df['date'] < '2018-04-03')]
    return cleaned_df

def concatenate(df1, df2):
    """Take PTR 901 and cleaned PTR 903 dataframes and concatenate them together to get full date range
    input: two pandas dataframes
    output: one pandas dataframe
    """
    frames = [df1, df2]
    result = pd.concat(frames)
    return result
