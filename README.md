# Automated Valuation Model - Lima
## A Spatial Machine Learning project to price Houses 

This project contains mainly three files:
- Scraper 🕷️
- notebooks 📓
- webapp 💻

## Exploratory Spatial Analysis
This notebook uses Spatial Analysis in order to take advantage of the coordinates features extracted of the webpage, in that sense, we made sure that Spatial analysis could leverage the model performance. You can watch the results in the [Spatial Autocorrelations Notebook](https://github.com/PBenavides/Automated-Valuation-Model-Lima/blob/b681c9cd0813c1a79913c5636ed17a7c95689f17/notebooks/Experiments/Spatial%20Autocorrelations.ipynb). The conclusions about these features can be sumarry as follows:

- Moran’s test says to us that our data contains a relationship between our target variable and the space.
- The relationship mentioned above it’s not strong but exists. Meaning the Spatial Features could add some value to the model.
- Local Spatial Autocorrelation test validates the well-known hypothesis that Lima is a centric city since the clusters are spread out around the center of the city.

You could also see Choropleths and other exploration images on [Exploratory Data Analysis Notebook](https://github.com/PBenavides/House_pricing_Lima/blob/b681c9cd0813c1a79913c5636ed17a7c95689f17/notebooks/Experiments/Exploratory%20Spatial%20Data%20Analysis.ipynb)

Choropleth

![Image](https://ibb.co/Tb82bCP)


# About the Machine Learning Model
Results are stored mainly in [2020_Notebook04_Model_Selection Notebook](https://github.com/PBenavides/House_pricing_Lima/blob/b681c9cd0813c1a79913c5636ed17a7c95689f17/notebooks/2020_Notebook04_Model_Selection.ipynb) and Pycaret were used for the rapid development on model selection and features. The main problem with this dataset is that is apparently small to solve the problem of outliers. Outliers are the main thing when it came to overperformance the first benchmarks that we tested.

Also, there is multiple integrations such as Point Of interest Clusters or Crime Clusters added to the model. But since there is many development cost on going with these into production, in comparison with value added on the benchmark metrics, the ML Model is maintained as a basic version in their API. It's also importat to add that the value of the ML Model is totally dependent on the quality of data. This project has only been trained by one-period housing data, there is much pontentiality on seeing trends through time but the Urbania webpage doesn't allow to scrap recurrently information of their webpage.  


## Webapp

For the deploynment, 
- [CSS & HTML] - Basic thing for web apps!
- [Flask] - As a Backend. (API DONE, form interface in progress) 
- [Heroku] - Server app (In progress)

## License

MIT

**Free Software, Hell Yeah!**
