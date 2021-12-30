from app.utils import load_discretizer, load_encoder
import pandas as pd

class Preprocessing_Pipeline():
    """
    data_dict: from the request.json.

    Primer Pipeline para procesar todos los datos de input.
    El input se espera que sea solo uno porque vendrá desde un formulario.
    Este input se aceptará como diccionario.
    """
    def __init__(self, data_dict):

        if 'MONEDA' in data_dict.keys(): pass
        else:
            data_dict['MONEDA'] = 1
        
        self.features_model = ['Barrio','Ciudad','Area_total',
        'NroBanios','Area_constr','MONEDA','Dormitorios','Antiguedad','Cocheras']
        self.data  = {feature: data_dict[feature] for feature in self.features_model}
        self.discretizer = load_discretizer()
        self.dict_encoder = load_encoder()

    def transform(self):
        
        dataframe = pd.DataFrame(data={0:self.data}).T.infer_objects()

        #Discretization
        dataframe['Area_constr_cat'] = self.discretizer.transform([dataframe['Area_constr'].values])[0][0]

        #Feature Engineering
        dataframe['areas_diff'] = dataframe['Area_total'] - dataframe['Area_constr']

        for col in ['Antiguedad','Cocheras','Dormitorios','NroBanios']:
            dataframe[col] = dataframe[col].astype('float32')

        #Encoding
        for col in dataframe.select_dtypes('object'):
            le = self.dict_encoder[col]
            dataframe[col] = le.transform(dataframe[col])

        return dataframe


class InputFeatures():

    def __init__(self, data_dict):

        self.lat = data_dict['lat']
        self.long = data_dict['long']