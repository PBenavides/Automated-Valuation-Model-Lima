# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests

lista_links = []
for i in range(1,553):
    link = 'https://urbania.pe/buscar/venta-de-casas?page='+str(i)
    lista_links.append(link)

all_internal_link = []
def extract_all_internal_links(lista_links):
    global all_internal_link
    for link in tqdm(lista_links):
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        internal_links = ['https://urbania.pe' + link.attrs['href'] 
                          for link in soup.find('div',{'class':'b-card-wrap js-card-list'}).find_all('a')]
        all_internal_link = all_internal_link + internal_links
    return all_internal_link

#all_internal_link = extract_all_internal_links(lista_links)

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
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

dict_all_casas = {}
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


dict_divs_info = {}
def scrap_div_info(soup_cada_casa, o_ = 0): #Para cada casa, sacame esta info.
    direccion_ = soup_cada_casa.find('div',{'class': 'b-ubication'}).find_all('p')[0].text
    anunciante_ = soup_cada_casa.find('div',{'class':'b-name-agent'}).find_all('p')[0].text
    florito_ = soup_cada_casa.find('div',{'class':'b-section-content js-property-services'}).findNext('div').find('p').text
    fecha_pub = soup_cada_casa.find('div',{'class':'b-view-code'}).findNext('span').text
    precio = soup_cada_casa.find('p',{'class':'e-totalPrice'}).text
    #visitas_ = soup_cada_casa.find('div',{'class':'b-view-code'}).find_all('span')[1].text
    global dict_divs_info
    dict_SUB_divs_info = {'Direccion':direccion_,'Anunciante':anunciante_,'Descripcion_':florito_,
                          'Fecha_pub':fecha_pub, 'Precio': precio}
    dict_divs_info['Casa'+str(o_)] = dict_SUB_divs_info
    fill_nan_vals_dict(dict_divs_info)
    return dict_divs_info


#Se esta reemplazando elm:section,a:features,lista_b:sub_feature
dict_feature_all_casas = {} #Si pongo esto dentro del loop siempre va a crear uno nuevo.
#Haré una función para obtener los ambientes de la casa.

def obtain_features_to_dict(soup_cada_casa,n_=0 ):  #Debería poner el n_ afuera de la función para iterar luego?
    obj_features_dicc = soup_cada_casa.find('section',{'class':'feature'})
    if obj_features_dicc == None:
        casa_interna_iterada = {}
        casa_interna_iterada['NoTieneData'] = 'SinValor'
    else:
        obj_features_dicc = obj_features_dicc.find_all('section') #Para cada casa selecciono su section
        n_ += 1 #A lo mejor es importante el número de casa
        casa_interna_iterada = {} #dict_3ro
        for section in obj_features_dicc:
            feature = section.find('h2').text #Este va a ser mi key de los servicios (features) que va a tener la data.
            sub_feature = [lisst.text for lisst in section.find_all('li',{'class':'b-section-item'})] #Serán los values 
            ##Entonces, segùn lo de arriba, para cada feature habrá una lista.
            casa_interna_iterada[feature] = sub_feature #Agrega cada feature con sus respectiva lista al diccionario
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
    
##Funcion General de scraping..............................

### Esta es la función principal.
#soup_list = [soup1,soup2,soup3]
dict_all_casas = {} #dict_1ro
dict_feature_all_casas = {} #dict_2do
dict_property_details = {}

def my_urbania_scrapper(all_internal_link):
    global dict_all_casas #dict_all_casas
    global dict_property_details
    global dict_feature_all_casas #Creo q no es necesario hacerlo global? #dict_all_casas_2
                #Para cada cuadro de información de cada casa
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
    prefinal_dict = merge(dict_all_casas,dict_feature_all_casas)
    final_dict = merge(prefinal_dict,dict_divs_info)
    final_final_dict = merge(final_dict, dict_property_details)
    final_df = pd.DataFrame.from_dict(final_final_dict,orient='index')
    final_df.to_csv('database_urbania.csv')



my_urbania_scrapper(all_internal_link)
