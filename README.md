# Pass_Closure
**A service predicting the probability of Snoqualmie Pass Road Closure**

*Problem: Snoqualmie Pass drivers need to be better prepared for disruption to their winter travel plans*

*Solution: A service predicting the probability of Snoqualmie Pass Closure based on historical and weather data*

## Product: [pass-closure](http://pass-closure.com "Title")

At pass-closure.com users are able to see the probability of Snoqualmie Pass Closure over the next 15 days.
The website was created using Flask and is hosted on AWS.

## High level solution diagram:

![](/imgs/high_level_solution.PNG)

## Data used:

* Historic weather data from NOAA using the ASOS (Automated Surface Observing Systems) for Stampede Pass
* Snoqualmie Pass closure data requested from WSDOT
* Forecast weather data scraped from weather.com to feed into model

## Modeling:

### Baseline:
I used a logistic regression model as my baseline model with basic data of temperature and 1s/0s for: precipitation, overcast, poor-visibility, windy. 

![](/imgs/baseline_ROC.png)

### Final Model:
I tried other models and features including Random Forest and Gradient Boosting. Then chose a random forest model as my final model with aggregated daily data including year, month, day and get_dummies for day of week as well as the original data.

![](/imgs/final_model_ROC.png)

## Accessing the project:

Clone the repo, then run the following commands:
* from the src folder: 
    * python initialize_db.py 
    * Note - because this is an hourly process the first data will be populated to the MongoDB after an hour
* from the website folder: 
    * export FLASK_APP=web_app.py
    * flask run

## Future work:

* Move to a hourly granularity for at least the first 3 days, with 2 separate models, to give users a better idea of the best time of day to use the pass
* Expand to other frequently used mountain passes

## Sources:

* Washington State Department of Transport (WSDOT)
* Robert Sherer's dressing for the weather project used as a reference for web scraping: [repo](https://github.com/rsherer/dressing-for-the-weather "Title")

