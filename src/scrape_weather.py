import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime

def get_raw_forecast(day):
    '''
    Get raw text from weather.com's 10 day forecast, for the day passed into the function.
    Day = 1 will be today.
    
    Input: int
    Day between 1 and 15, representing the day of the desired forecast.
    
    Output: list of strings
    Raw text for the day chosen, in the following order:
        [daymonth date, weather forecast, hi/lo temp, % chance precipitation, 
         wind speed and direction, humidity]
    '''
    page_link = 'https://weather.com/weather/tenday/l/USWA0413:1:US'
    page_response = requests.get(page_link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    
    print(page_content)

    web_predictions = []
    for i in range(0,105):
        predictions = page_content.find_all('td')[i].text
        web_predictions.append(predictions)
    return web_predictions[(day*7 - 6):(day*7)]

def get_raw_forecast_dataframe():
    ''' 
    Get latest raw weather forecast dataframe for the next 15 days.
    Output: raw dataframe.
    '''
    #Get list of forecasts for the next 15 days
    forecasts = []
    for day in range(1,16):
        forecasts.append(get_raw_forecast(day))
    
    #Set todays date to be used as the start of the dataframe index
    todays_date = datetime.datetime.now().date()
    index = pd.date_range(todays_date, periods=15, freq='D')
    #Set the columns for the dataframe
    columns = ['date','weather','temp', 'precipitation', 'wind', 'humidity']
    #Create the raw forecast dataframe with forecasts list, index and column headings
    forecasts_df = pd.DataFrame(forecasts, index=index, columns=columns)
    return forecasts_df

def get_hi_temperature(temp_string):
    '''
    Take the hi/lo string from weather.com and convert to an integer of the high temperature.
    Input: string
    Output: int
    '''
    numbers = [str(num) for num in range(0,10)]
    temp = ''
    for char in temp_string:
        if char in numbers:
            temp += char
        else:
            break
    return int(temp)

def get_low_temperature(temp_string):
    '''
    Take the hi/lo string from weather.com and convert to an integer of the
    low temperature.
    Input: string
    Output: int
    '''
    numbers = [str(num) for num in range(0,10)]
    temp = ''
    hilo = temp_string
    for char in reversed(hilo[:-1]):
        if char in numbers:
            temp = char + temp
        else:
            break
    return int(temp)

def get_wind_speed(temp_string):
    '''
    Take the wind string from weather.com and convert to an integer of the wind speed.
    Input: string
    Output: int
    '''
    numbers = [str(num) for num in range(0,10)]
    temp = ''
    for char in temp_string:
        if char in numbers:
            temp += char
    return int(temp)

def get_overcast(weather_string):
    """
    Take the weather string from weather.com and convert to a 1 if string contains words in overcast_list
    otherwise return a 0
    Input: string
    output: int(0 or 1)
    """
    overcast_list = ['Cloudy', 'Snow', 'Rain', 'Showers', 'Thunderstorms']
    for word in weather_string.split():
        if word in overcast_list:
            return 1
        else:
            return 0

def get_poor_visibility(weather_string):
    """
    Take the weather string from weather.com and convert to a 1 if string contains words in poor_visibility_list
    otherwise return a 0
    Input: string
    output: int(0 or 1)
    """
    poor_visibility_list = ['Snow', 'Rain', 'Fog', 'Mist']
    for word in weather_string.split():
        if word in poor_visibility_list:
            return 1
        else:
            return 0

def snoqualmie_pass_prediction_components():
    """
    Get latest cleaned features from weather.com to be used to gain closure probabilities
    Output: Clean dataframe to be used for predicting probability of closure
    """
    forecasts_df = get_raw_forecast_dataframe()
    
    #Extract high/low and calulate average temperature
    forecasts_df['high'] = forecasts_df['temp'].map(get_hi_temperature)
    forecasts_df['low'] = forecasts_df['temp'].map(get_low_temperature)
    forecasts_df['average'] = ((forecasts_df['high'] + forecasts_df['low']) / 2)

    #Re-use get_hi_temperature function to get just the integer from precipitation
    forecasts_df['precip'] = forecasts_df['precipitation'].map(get_hi_temperature)
    #Set precipitation to 1 if chance of precipitation is >= 30%
    forecasts_df['is_precipitating'] = forecasts_df['precip'].apply(lambda x: 1 if (x >= 30) else 0)

    #Extract wind speed and set to 1 if windspeed >= 10mph
    forecasts_df['wind_int'] = forecasts_df['wind'].map(get_wind_speed)
    forecasts_df['windy'] = forecasts_df['wind_int'].apply(lambda x: 1 if (x >= 10) else 0)

    #Infer overcast and poor visibility
    forecasts_df['overcast'] = forecasts_df['weather'].map(get_overcast)
    forecasts_df['poor_visibility'] = forecasts_df['weather'].map(get_poor_visibility)

    #Drop unwanted columns
    forecasts_df = forecasts_df.drop(['temp', 'high', 'low', 'precipitation', 'precip', 'wind', 'wind_int', 'weather', 'humidity'], axis=1)

    #Rename columns
    forecasts_df.rename(columns={'average':'temp', 'is_precipitating':'precipitation', }, inplace=True)

    return forecasts_df

