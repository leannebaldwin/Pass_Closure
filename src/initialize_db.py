import pandas as pd
import numpy as np
import pymongo
from time import sleep

from scrape_weather import snoqualmie_pass_prediction_components

'''Initialize a Mongo Database called Snoqualmie'''
mc = pymongo.MongoClient()
db = mc['Snoqualmie']
docs = db['docs']


def get_data_populate_db():
    '''
    Get data from snoqualmie_pass_prediction_components function in the scrape_weather python file
    populate Snoqualmie database with the features needed to predict probability of closure
    Output: populated db
    '''
    new_data = snoqualmie_pass_prediction_components()
    docs.delete_many({})
    docs.insert_many(new_data.to_dict('records'))

def fetch_every_hour():
    ''' 
    Function waits 60 minutes then calls the get_data_populate_db 
    function. The while loop insures that it repeats forever at 60 minute intervals'''
    while True:
        sleep(60*60)
        get_data_populate_db()

#Function call to start the endless loop
if __name__ == '__main__':
   #fetch_every_hour()
   get_data_populate_db()