#This file is to specify every model we want to try. 
#It's made also to try different models with different hyperparameters

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet


models = {"linear_reg": LinearRegression(
    ),
    "lasso_reg" : Lasso(
    )
        }
