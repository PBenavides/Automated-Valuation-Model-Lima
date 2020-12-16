## Utility functions to run training from the shell.

import joblib
import pandas as pd

import argparse
import os
import yaml
import logging 

from sklearn.metrics import accuracy_score
from data import preprocessing_data

import model_dispatcher
import config
from utils import load_cfg
#In order to use yaml confg file, we'll make this functions.

config = load_cfg('conf.yaml')

def run(fold,model):
    """
    fold: int Number of fold wanted to train.
    model: str model wanted to train.
    """

    #read the training data with folds
    df = pd.read_csv(f"project-template/input/{config['Project_details']['name']}_folds.csv")

    #train_data is where kfold is different to actual fold number
    df_train = df[df['kfold'] != fold].reset_index(drop=True)
    #test_data is where kfold is equal to actual fold number
    df_valid = df[df['kfold'] == fold].reset_index(drop=True)

    #Defining x_train,x_test,y_train,y_valid
    x_train = df_train.drop(config['Target_name'],axis=1).values
    y_train = df_train[config['Target_name']].values

    x_valid = df_valid.drop(config['Target_name'],axis=1).values
    y_valid = df_valid[config['Target_name']].values

    #----------------------------------TRAINING----------------------------------------------
    
    clf = model_dispatcher.models[model]

    clf.fit(x_train, y_train)

    preds = clf.predict(x_valid)
    accuracy = accuracy_score(y_valid, preds)

    print(f"Fold={fold}, Accuracy={accuracy}")

    #saving the model
    joblib.dump(clf,
    os.path.join("project-template/"+config['Model_output'], f"dt_{fold}_{model}.bin"))

if __name__=="__main__":
   #we will specify arguments to run from a shell scripting.
   parser = argparse.ArgumentParser()
   
   parser.add_argument(
       "--fold",
       type=int
   )
   
   parser.add_argument(
       "--model",
       type=str
   )
   
   args = parser.parse_args()
   run(fold = args.fold,
       model = args.model)
   
   print(config)