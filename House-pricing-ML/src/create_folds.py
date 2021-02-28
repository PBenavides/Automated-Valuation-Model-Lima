
#In this project we will use Walk Forward (or expanding window) as Cross Validation technique.

import os
import glob
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold

from sklearn.impute import KNNImputer
import config

def make_dataframe_with_lags(data, start_date, end_date, agg_dictionary, columns_to_pivot, datecol = 'Fecha',
                            index_col='PCA_comp'):
    """
    Pass data and obtain a dataframe with past values as columns, and also a
    Y column to use as a target feature.
    
    I need to:
    Aggregated methods by dictionary.
    From quarter to another.
    With index attached to it.
    """
    
    #The end_date will be use for making the target:
    temp_df = data[(data[datecol] >= start_date)&(data[datecol] < end_date)]
    #standarize columns names
    dict_repl_dates = {elem:'LAG_'+str(n) for n,elem in enumerate(np.sort(temp_df[datecol].unique())[::-1],1)}
    temp_df[datecol].replace(dict_repl_dates, inplace=True)
    #Pivot table for macro data
    macro_lags = pd.pivot_table(temp_df, values=columns_to_pivot, index=index_col, 
                       columns=datecol, aggfunc=agg_dictionary).ffill().bfill().reset_index() #Careful with ffill & bfill
    macro_lags.columns = macro_lags.columns.map('_'.join).str.strip('_')
    #Creating lagged targets:

    lagged_targets = pd.pivot_table(temp_df, values='Precio_m2',index=['PCA_comp','Distrito'], columns='Fecha').reset_index()

    #Creo una dummy para luego reemplazar los lagged_targets
    for lag_col in ['LAG_1','LAG_2','LAG_3','LAG_4']:
        lagged_targets[lag_col+'_isna'] = 0
        lagged_targets[lag_col+'_isna'].iloc[lagged_targets[lagged_targets[lag_col].isna()].index] = 1
    
    X = lagged_targets.iloc[:,:6]
    imputer = KNNImputer(n_neighbors=5)
    imputed_lagged_targets = imputer.fit_transform(X)

    lagged_targets.iloc[:,:6] = pd.DataFrame(imputed_lagged_targets, columns = lagged_targets.iloc[:,:6].columns)
    
    #Actual target. The end_date is my target column.
    main_train = data[data[datecol] == end_date]
    main_target = main_train.groupby(['PCA_comp','Distrito'])['Precio_m2'].median().reset_index().rename(columns={'Precio_m2':'target'})
    #Merge final dataframe
    macro_lagged = macro_lags.merge(lagged_targets, on='PCA_comp',how='left')
    final_df = macro_lagged.merge(main_target, on=['PCA_comp','Distrito'],how='left').dropna()
    
    return final_df

def make_training_dataframe(data, window_size = 60, agg_dictionary = np.mean):
    
    """
    Make the entire dataframe for training.
    
    Per PCA and district
    """
    
    macroeconomics_indx_col = ['PBI ', 'Ratio adul-joven','TI Trimestral', 'Tasa hipotecaria Trimestral', 
                           'CaptBurs Trimestral','INB']
    lista_df = []
    
    #Making train dataset with expanding window approach
    for n in range(0,window_size):
        dates_array = np.sort(data['Fecha'].unique())[n:n+5]
        sample_df = make_dataframe_with_lags(data, start_date = dates_array[0], end_date=dates_array[-1],
                                     agg_dictionary = np.mean,
                                    columns_to_pivot=macroeconomics_indx_col)
        lista_df.append(sample_df)    
    train_data = pd.concat(lista_df).reset_index(drop=True)
    #print('TRAIN_DATA: From {} to {}'.format(train_data['Fecha'].min(), train_data['Fecha']))
    #Making test dataset with the next period.
    
    testing_dates_array = np.sort(data['Fecha'].unique())[n+1:n+1+5]
    
    assert len(testing_dates_array) == 5
    
    testing_data = make_dataframe_with_lags(data, start_date = testing_dates_array[0], 
                                                end_date = testing_dates_array[-1], agg_dictionary = np.mean,
                                               columns_to_pivot=macroeconomics_indx_col).reset_index(drop=True)

    #print(f'LAST DATE TRAIN:{dates_array[-1]}')
    #print(f'TESTING DATE: {testing_dates_array[-1]}')
    
    return train_data, testing_data, testing_dates_array[-1]