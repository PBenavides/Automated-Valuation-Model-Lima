#This file is to specify every model we want to try. 
#It's made also to try different models with different hyperparameters

from sklearn.tree import DecisionTreeClassifier

models = {"decision_tree_gini": DecisionTreeClassifier(
    criterion="gini"
    ),
    "decision_tree_entropy" : DecisionTreeClassifier(
        criterion="entropy"
    )
        }
