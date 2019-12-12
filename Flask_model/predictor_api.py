<<<<<<< HEAD
# Aca se contendran todos los métodos para preprocesar la data, cargar el modelo y correrlo

## La data debe ser un pandas.Series para poder correr el modelo y predecir con ella.
import pickle
import pandas as pd
import geohash2 as gh

def encoding_data(data):

    '''
    Esta función va a limpiar las variables que tengamos, es decir, 
    el cliente va a elegir "Lima" y eso se traducira a un número (1). 
    '''
    with open('provincias_dict.pickle', 'rb') as handle:
        dict_provincias = pickle.load(handle)

    with open('distritos_dict.pickle','rb') as handle:
        dict_distritos = pickle.load(handle)

    #Trabajare la data como un dataframe para poder transformarla con facilidad.
    encoded_data = pd.DataFrame(data,index=[0])
    
    encoded_data.Distrito = encoded_data.Distrito.map(dict_distritos)
    encoded_data.Provincia = encoded_data.Provincia.map(dict_provincias)

    encoded_data.Distrito = pd.to_numeric(encoded_data.Distrito)
    encoded_data.Provincia = pd.to_numeric(encoded_data.Provincia)

    return encoded_data

def get_longitude_latitude():
    
    return 0

def geohashing_data(data):
    encoded_data['geohash5'] = gh.encode(encoded_data.latitud, encoded_data.longitud, precision = 5)
    
    encoded_data['geohash6'] = gh.encode(encoded_data.latitud, encoded_data.longitud, precision = 6)
    
    return 0 

def feature_engineering(prefinal_data):

    pitucos = ['LaMolina','Asia','SantiagoDeSurco','SanBorja','Miraflores','SanIsidro','Barranco','SanBartolo',
           'Mancora']
    cuasi_pitucos = ['Lince','JesusMaria','SanMiguel','Chaclacayo','Brenia','Ate','LaPerla']
    prefinal_data['grupo_dist'] = 'No_es_pituco'
    prefinal_data.loc[prefinal_data['Distrito'].isin(pitucos),'grupo_dist'] = 'Es_pituco'
    prefinal_data.loc[prefinal_data['Distrito'].isin(cuasi_pitucos)],'grupo_dist'] = 'Es_cuasi_pituco'
    return 0 

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
=======
# Aca se contendran todos los métodos para preprocesar la data, cargar el modelo y correrlo

## La data debe ser un pandas.Series para poder correr el modelo y predecir con ella.
import pickle
import pandas as pd
import geohash2 as gh

def encoding_data(data):

    '''
    Esta función va a limpiar las variables que tengamos, es decir, 
    el cliente va a elegir "Lima" y eso se traducira a un número (1). 
    '''
    with open('provincias_dict.pickle', 'rb') as handle:
        dict_provincias = pickle.load(handle)

    with open('distritos_dict.pickle','rb') as handle:
        dict_distritos = pickle.load(handle)

    #Trabajare la data como un dataframe para poder transformarla con facilidad.
    encoded_data = pd.DataFrame(data,index=[0])
    
    encoded_data.Distrito = encoded_data.Distrito.map(dict_distritos)
    encoded_data.Provincia = encoded_data.Provincia.map(dict_provincias)

    encoded_data.Distrito = pd.to_numeric(encoded_data.Distrito)
    encoded_data.Provincia = pd.to_numeric(encoded_data.Provincia)

    return encoded_data

def get_longitude_latitude():
    
    return 0

def geohashing_data(data):
    encoded_data['geohash5'] = gh.encode(encoded_data.latitud, encoded_data.longitud, precision = 5)
    
    encoded_data['geohash6'] = gh.encode(encoded_data.latitud, encoded_data.longitud, precision = 6)
    
    return 0 

def feature_engineering(prefinal_data):

    pitucos = ['LaMolina','Asia','SantiagoDeSurco','SanBorja','Miraflores','SanIsidro','Barranco','SanBartolo',
           'Mancora']
    cuasi_pitucos = ['Lince','JesusMaria','SanMiguel','Chaclacayo','Brenia','Ate','LaPerla']
    prefinal_data['grupo_dist'] = 'No_es_pituco'
    prefinal_data.loc[prefinal_data['Distrito'].isin(pitucos),'grupo_dist'] = 'Es_pituco'
    prefinal_data.loc[prefinal_data['Distrito'].isin(cuasi_pitucos)],'grupo_dist'] = 'Es_cuasi_pituco'
    return 0 

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
>>>>>>> 6c7e231a3b7b588d456e0d9a8399d616b39739bf
    print('El modelo si funciona, y toma como input un diccionario')