from ScrapingStructure import ScrapingStructure
from InmuebleCrawler import InmuebleCrawler
from ScrapingUtils import enviar_archivo_por_email

import pandas as pd
import numpy as np
import re

if __name__ == '__main__':
    
    for diccionario_estructura in ScrapingStructure.UrbaniaStructure():
        pagina_principal = diccionario_estructura['url']
        paginas_final = diccionario_estructura['max_page']

        temp_crawler = InmuebleCrawler(pagina_principal = pagina_principal,\
            num_paginas=(0, paginas_final))

        dicc_crawler = temp_crawler.almacenamiento_de_busquedas()

        dataframe = pd.DataFrame(dicc_crawler).T

        print(dataframe.shape, "EL SHAPE")

        dataframe['Precio'] = dataframe['Precio'].str.replace('\'','')
        dataframe['Precio'] = dataframe['Precio'].str.replace(',','')
        
        dataframe['MONEDA'] = dataframe['Precio'].str.extract('({})'.format('|'.join(['S/','USD'])),
        flags=re.IGNORECASE, expand=False).str.upper().fillna(np.nan)

        dataframe['Barrio'] = dataframe['Barrio'].str.replace("'", '')
        dataframe['Ciudad'] = dataframe['Ciudad'].str.replace("'",'')

        dataframe['Anunciante'] = dataframe['Anunciante'].str.extract("('name': '(.*?)')")[1]

        dataframe.to_csv(diccionario_estructura['Tipo']+'.csv', index=False)

        enviar_archivo_por_email(namefile = diccionario_estructura['Tipo']+'.csv')