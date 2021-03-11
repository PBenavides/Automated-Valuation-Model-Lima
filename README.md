# House_pricing_Lima

In Progress...

Note: The main idea was to have an algorithm to price houses , apartments, lands and offices across time. But due to the fact that the webpage is unscrapable without proxys I turned this repository in a set of experiments on Time-Series Predictions. This was built thinking about two approaches (models): 

#### 1.- A Pricing algorithm that depends of the chracteristics of the House (i.g. #Bathrooms, #Bedrooms, Coordinates, etc) which is independent of time. 
        This was built on Data Analysis/. But the deploynment still neds to be done (It is expected to have a Flask API)
        
### 2.- A Time-Series Forecasting for the apartments squared meter price per districts depending on macroeconomic features (GDP, Rates, Demographic ratios, etc). 
        This repository contains this approach on: House-pricing-ML/notebooks/. 
        The data used from this: House-Pricing-ML/input/macro-data    House-Pricing-ML/input/series-bcrp
        
### About the Scraper: Since the webpage scraped use cloudfare we tried to use [this repository](https://github.com/Anorov/cloudflare-scrape) The other options involves renting proxy servers or use a JS Solution.

This project was made mainly to practice DScience concepts and codes. It'll improve soon.
