# -*- coding: utf-8 -*-
"""
Este es un scraper para la página Urbania.pe
La información obtenida podrá será usada con fines meramente académicos.
Cualquier petición de de la compañia para eliminar este script deberá
ser enviada a fob534154@gmail.com  
Hecho por @PBenavides
"""

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
pd.set_option('display.max_columns', None)

#Llamaremos lista_links a la lista que contiene todas las páginas generales de Urbania

lista_links = []
for i in range(1,582):
    link = 'https://urbania.pe/buscar/venta-de-casas?page='+str(i)
    lista_links.append(link)

#LLameremos all_internal_link a los links de cada casas en específico
def extract_all_internal_links(lista_links):
    all_internal_link = []
    for link in tqdm(lista_links): #Para cada link en la lista_links
        response = requests.get(link) #Hago el request
        soup = BeautifulSoup(response.text, "html.parser") #Creo el objeto 
        internal_links = ['https://urbania.pe' + link_casa.attrs['href'] 
                          for link_casa in soup.find('div',{'class':'b-card-wrap js-card-list'}).find_all('a')]
#        Encuentro cada link de cada casa... 
        all_internal_link = all_internal_link + internal_links #Sumo los links que encontré a la lista general.
    return all_internal_link

def dict_casas_info(soup_cada_casa, i_ = 0):
    obj_dicc = soup_cada_casa.find('div',{'class':"b-leading-data-property u-flex-wrap"}).find_all(
            'div',{'class':"b-leading-data-service"}) 
    dict_casa_iter = {}
    for iter_ in obj_dicc: #Para cada par de datos (q serían keys & values)
        a = iter_.find_all('p')[0].text #Bótame el texto primero (key)
        b = iter_.find_all('p')[1].text #Bótame el texto segundo (value)
        dict_casa_iter[a] = b
    global dict_all_casas
    dict_all_casas['Casa'+str(i_)] = dict_casa_iter
    return dict_all_casas  

#LLena todos los valores nulos del diccionario para que se muestren en el dataframe
def fill_nan_vals_dict(dictionary):
    for dict_per_house in dictionary.values():
        if dict_per_house == {}:
            dict_per_house['NoTieneAlgunDatoExtra'] = 'NingunValor'
        else:
            pass

#Para hacerle el merge a los diccionarios
def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                pass
                #raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

# En este caso, soup_cada_casa hace referencia al soup que se creará más adelante cuando
# se itere por todas los links de las casas. 


dict_all_casas = {}
#La siguiente función se iterará por sobre cada casa (o link de casa)
#Retornará un diccionario de diccionarios (Por eso creamos dos dict)
dict_divs_info = {}
def scrap_div_info(soup_cada_casa, o_ = 0): #Para cada casa, sacame esta info.
    direccion_ = soup_cada_casa.find('div',{'class': 'b-ubication'}).find_all('p')[0].text
    if soup_cada_casa.find('div',{'class':'b-name-agent'}) == None:
        anunciante_ = 'No disponible'
    else:
        anunciante_ = soup_cada_casa.find('div',{'class':'b-name-agent'}).find_all('p')[0].text
    florito_ = soup_cada_casa.find('div',{'class':'b-section-content js-property-services'}).findNext('div').find('p').text
    fecha_pub = soup_cada_casa.find('div',{'class':'b-view-code'}).findNext('span').text
    precio = soup_cada_casa.find('p',{'class':'e-totalPrice'}).text
    #visitas_ = soup_cada_casa.find('div',{'class':'b-view-code'}).find_all('span')[1].text
    global dict_divs_info
    dict_SUB_divs_info = {'Direccion':direccion_,'Anunciante':anunciante_,'Descripcion_':florito_,
                          'Fecha_pub':fecha_pub, 'Precio': precio}
    dict_divs_info['Casa'+str(o_)] = dict_SUB_divs_info
    #fill_nan_vals_dict(dict_divs_info)
    return dict_divs_info

#Nos retornará un dict de dicts, con los mismos keys pero diferentes values (diccionarios también)

dict_feature_all_casas = {} #Si pongo esto dentro del loop siempre va a crear uno nuevo.
#Haré una función para obtener los ambientes de la casa.

def obtain_features_to_dict(soup_cada_casa,n_=0 ):  
    obj_features_dicc = soup_cada_casa.find('section',{'class':'feature'}) #Entro al div grande sobre el que iteraré
    casa_interna_iterada = {} #dict_3ro
    if obj_features_dicc is None or len(obj_features_dicc) == 0:
        ##Hacer para condominios (con lo de interbank)
        casa_interna_iterada['EsCondominio'] = 'Si'
    else:
        obj_features_dicc2 = obj_features_dicc.find_all('section') #Para cada casa selecciono su section
        if len(obj_features_dicc2) != 0:
            for section in obj_features_dicc2:
                feature = section.find('h2').text #Este va a ser mi key de los servicios (features) que va a tener la data.
                sub_feature = [lisst.text for lisst in section.find_all('li',{'class':'b-section-item'})] #Serán los values 
                ##Entonces, segùn lo de arriba, para cada feature habrá una lista.
                casa_interna_iterada[feature] = sub_feature #Agrega cada feature con sus respectiva lista al diccionario
        else:
            pass #Agrego que no tiene data en features
    global dict_feature_all_casas #dict_2do
    dict_feature_all_casas['Casa'+str(n_)] = casa_interna_iterada #Mi diccionario de diccionarios {'Casa1:{'Servicios': [],...}
    fill_nan_vals_dict(dict_feature_all_casas)
    return dict_feature_all_casas #Me retorna el diccionario de diccionarios
dict_property_details = {}

def dict_property_info(soup_cada_casa, u_=0):
    global dict_property_details #A un dict de afuera
    obj_dicc2 = soup_cada_casa.find('div',{'class':'b-property-details u-flex-wrap'}).find_all(
        'div',{'class':"b-leading-data-service"}) #Busco la lista para iterar
    dict_casa_iter2 = {} #Creo un dict interno
    for iter_ in obj_dicc2:#itero
        key1 = iter_.find_all('p')[0].text #Saco mi key
        value1 = iter_.find_all('p')[1].text #Saco mi value
        dict_casa_iter2[key1] = value1 #Lo agrego al diccionario interno
    fill_nan_vals_dict(dict_casa_iter2)
    dict_property_details['Casa'+str(u_)] = dict_casa_iter2

##Acá voy a sacar los datos de longitud y latitud
def give_me_the_number(scr_list):
    for numb,script in enumerate(scr_list):
        str_scr = str(script)
        if str_scr.find('longitud') != -1:
            number_scr = numb
        else:
            pass
    return number_scr

def get_me_long_and_lat(cada_soup, a_ = 0):
    global long_lat_dict
    scr_list = cada_soup.find_all('script')
    number_scr = give_me_the_number(scr_list)
    scr_str = str(cada_soup.find_all('script')[number_scr]) #Acá ya tengo ubicado mi string.
    position = scr_str.find('longitud')
    long = scr_str[position+11:position+29]
    position2 = scr_str.find('latitud')
    lat = scr_str[position2+11:position2+29]
    dict_sub_info_long_lat = {'longitud': long, 'latitud' : lat} #Es un diccionario de sub información.
    long_lat_dict['Casa' + str(a_)] = dict_sub_info_long_lat #Este tipo de objeto es el que nos va a ordenar la info.


#Funcion General de scraping..............................
def my_urbania_scrapper(all_internal_link):
    global dict_all_casas #dict_all_casas
    global dict_property_details
    global dict_feature_all_casas #Creo q no es necesario hacerlo global? #dict_all_casas_2
    global long_lat_dict            #Para cada cuadro de información de cada casa
    for i,internal_link in tqdm(enumerate(all_internal_link)):
        response = requests.get(internal_link)
        soup_cada_casa = BeautifulSoup(response.text,"html.parser") #con esto ya no necesitaré listas.
        try:
            obtain_features_to_dict(soup_cada_casa,n_=i) ##recuerda que esta f(x) lo bota en dict_feature_all_casas##PabloBenavides
        except:
            pass
        try: 
            dict_casas_info(soup_cada_casa,i_=i) ##Recuerda que esta f(x) lo bota en dict_all_casas.
        except AttributeError: 
            pass 
        try:
            dict_property_info(soup_cada_casa, u_= i)
        except AttributeError:
            pass
        try:
            scrap_div_info(soup_cada_casa,o_=i) #Me lo bota en dict_divs_info
        except:
            pass
        try: 
            get_me_long_and_lat(soup_cada_casa, a_= i)
        except AttributeError:
            pass
    prefinal_dict = merge(dict_all_casas,dict_feature_all_casas)
    final_dict = merge(prefinal_dict,dict_divs_info)
    final_final_dict = merge(final_dict, dict_property_details)
    final_3_dict = merge(final_final_dict, long_lat_dict)
    final_df = pd.DataFrame.from_dict(final_3_dict,orient='index')
    final_df.to_csv('database_urbania_w_long_lat.csv')

### Esta es la función principal.
#soup_list = [soup1,soup2,soup3]
dict_all_casas = {} #dict_1ro
dict_feature_all_casas = {} #dict_2do
dict_property_details = {}
dict_property_details = {}
dict_divs_info={}
long_lat_dict = {}