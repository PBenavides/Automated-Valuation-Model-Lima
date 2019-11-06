# Aca se contendran todos los métodos para preprocesar la data, cargar el modelo y correrlo

## La data debe ser un pandas.Series para poder correr el modelo y predecir con ella.
import pickle
import pandas as pd

def encode_cats(data):

    '''
    Esta función va a limpiar las variables que tengamos, es decir, 
    el cliente va a elegir "Lima" y eso se traducira a un número (1). 
    '''
    with open('provincias_dict.pickle', 'rb') as handle:
        dict_provincias = pickle.load(handle)

    with open('distritos_dict.pickle','rb') as handle:
        dict_distritos = pickle.load(handle)

    #Trabajare la data como un dataframe para poder transformarla con facilidad.
    clean_data = pd.DataFrame(data,index=[0])

    clean_data.Distrito = clean_data.Distrito.map(dict_distritos)
    clean_data.Provincia = clean_data.Provincia.map(dict_provincias)

    clean_data.Distrito = pd.to_numeric(clean_data.Distrito)
    clean_data.Provincia = pd.to_numeric(clean_data.Provincia)
    return clean_data

def make_prediction(data):
    '''
    Dada la data a leer, .

    Para esto, el input "data" tiene que tener la forma de un diccionario,
    que se va a convertir en un dataframe para poder trabajar con el modelo.
    '''
    
    data = encode_cats(data)
    model = pickle.load(open('model.sav','rb'))

    prediction = model.predict(data)

    return prediction

## La siguiente seccion es para testear si la prediccion corre correctamente
## Para inicializarlo tienes que correr predictor_api.py en la terminal

if __name__ == '__main__':
    from pprint import pprint
    print('Chequeando si la app funciona')
    print('La data de input es:')

    data = {'Area_constr_m2':180,'latitud':-12.1131,'longitud':-77.0009,'Area_total_m2':180,'Distrito':'Surquillo',
     'Provincia':'Lima','Dormitorios':3}
    

    prediction = make_prediction(data)
    print('Output:')
    pprint(prediction)
    print('El modelo si funciona, y toma como input un diccionario')