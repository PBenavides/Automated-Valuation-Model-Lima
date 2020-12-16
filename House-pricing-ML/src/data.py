## Functions to Load, Preprocessing, and Handling Data.
## All the functions here need to be aproved by and documented by notebooks Delivered-*.ipynb

import pandas as pd
import os, glob
from utils import load_cfg
#In order to use yaml confg file, we'll make this functions.

config = load_cfg('conf.yaml')
conf_preproc = config['Preprocessing']

def read_train_data():
    """
    Function to read and concat training data that is split across multiples csv.
    """
    print(os.getcwd())
    os.chdir("project-template/input")
    print(os.getcwd())
    extension = 'csv'
    train_filenames = [i for i in glob.glob('*.{}'.format(extension)) if "train" in i]
    concat_df = pd.concat([pd.read_csv(file) for file in train_filenames])
    return concat_df

def preprocessing_data(df):
    """
    A simple preprocessing function.
    """

    #Dealing with Nans
    df['Edad'].fillna(int(df['Edad'].mean()), inplace=True)
    df['P_embarque'].fillna('S',inplace=True)
    df['P_embarque'].fillna(df['P_embarque'].mode(), inplace=True)
    df['Tarifa'].fillna(df['Tarifa'].mean(),inplace=True)
    df.drop(conf_preproc['cols_to_drop'],axis=1, inplace=True)
    #Dealing with outliers

    outliers_to_repl = df[df['Tarifa'] > df['Tarifa'].quantile(conf_preproc['threshold_outliers'])].index
    df.loc[outliers_to_repl, 'Tarifa'] = df['Tarifa'].quantile(conf_preproc['threshold_outliers'])

    #Feature Engineering
    df['Miembros_de_fam'] = df['Hermanos'] + df['Padres_hijos'] + 1
    df['Viaja_solo'] = 1 
    df['Viaja_solo'].loc[df['Miembros_de_fam'] > 1] = 0

    df['es_niño'] = 0
    df.loc[(df['Edad'])<15,'es_niño'] = 1

    #Labeling & Categorization

    if conf_preproc['encoding_technique'] == 'dummy':
        df = pd.get_dummies(df, columns=['P_embarque','Genero'])
    elif conf_preproc['endocing_technique'] == 'LabelEncoder':
        from sklearn.preprocessing import LabelEncoder
        for col in df.columns:
            if df[col].dtype == 'object':
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].values)
    else:
        print('We are replacing with labels with dictionary pre-defined values')
        cat_to_nums = {"P_embarque":  {"S": 2, "C": 1, "Q":0},
               "Genero": {"male":0,"niño":1,"female":2}}
        df.replace(cat_to_nums, inplace=True)
    #ReScaling data
    return df

if __name__ == '__main__':
    df = read_train_data()
    df_preproc = preprocessing_data(df)

    print(f'With the following configuration:\n \n {conf_preproc} \n \n \n ')
    
    print(f'The size: {df_preproc.size}\nThe head 1: {df_preproc.head(1)}')