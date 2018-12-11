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

## Modeling:

I used a logistic regression model as my baseline model with basic data of temperature and 1s/0s for: precipitation, overcast, poor-visibility, windy. 

![](/imgs/baseline_ROC.PNG)

