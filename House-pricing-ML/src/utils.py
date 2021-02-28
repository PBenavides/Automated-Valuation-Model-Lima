import os
import yaml
import logging
import pandas as pd
import numpy as np 

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def make_paths_absolute(dir_, cfg):
    """
    Make all values for keys ending with `_path` absolute to dir_.
    """
    for key in cfg.keys():
        if key.endswith("_path"):
            cfg[key] = os.path.join(dir_, cfg[key])
            cfg[key] = os.path.abspath(cfg[key])
            if not os.path.isfile(cfg[key]):
                logging.error("%s does not exist.", cfg[key])
        if type(cfg[key]) is dict:
            cfg[key] = make_paths_absolute(dir_, cfg[key])
    return cfg

def load_cfg(yaml_filepath):
    """
    yaml_filepath: string

    -----
    Returns cfg: dict
    """
    with open(yaml_filepath, 'r') as stream:
        cfg = yaml.safe_load(stream)
    cfg = make_paths_absolute(os.path.dirname(yaml_filepath), cfg)
    return cfg

def formatting_predictions(dict_districts):
    """
    dict_districts: A dictionary with datetime as index, and a subdict with 'Distrito' & 'actuals|predictions'
    This will return us two matrixes, one of predictions and the other of actuals values.
    In order to compare their metrics.
    
    """
    data_districts = pd.DataFrame().from_dict({(outerKey, innerKey) : values for outerKey, innerDict in dict_districts.items() for innerKey, values in innerDict.items()})
    #Duplicate columns
    data_districts.columns = [str(tup[0]) if tup[1] != 'Distrito' else tup[1] for tup in data_districts.columns]
    data_districts = data_districts.loc[:, ~data_districts.columns.duplicated()].set_index('Distrito').T
    data_districts.columns.names = [None]
    
    return data_districts


#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------METRICS-----------------------------------------------------

def calculate_mape(actual, prediction):
        mask = actual != 0
        return (np.fabs(actual - prediction)/actual)[mask].mean()

def subdict_metrics(actuals, preds):
    """
    This function is made to build a dictionary that contains metrics.
    """
    #Calculating metrics:
    mae = mean_absolute_error(actuals, preds)
    mse = mean_squared_error(actuals, preds)
    rmse = np.sqrt(mse)
    rmsle = np.sqrt(np.mean(np.power(np.log(np.array(abs(preds))+1) - np.log(np.array(abs(actuals))+1), 2)))
    r2 = r2_score(actuals,preds)
    mape = calculate_mape(actuals, preds)
    #Since doesn't matter how many time the algorithm will train, we don't add this metrics.
    
    return {'MAE': mae, 'MSE': mse, 'RMSE' : rmse, 'R2' : r2,
                                  'RMSLE' : rmsle, 'MAPE' : mape}