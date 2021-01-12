import requests
import cfscrape
import re
import sys
from bs4 import BeautifulSoup

import time
import numpy as np

from ScrapingUtils import enviar_archivo_por_email

class InmuebleCrawler:
    """
    Esta clase tomará dos argumentos para tomarlos desde el ScrapingStructure:
    pagina_principal: De la página principal que se va a escrapear
    num_paginas: Del total de páginas que contiene.
    """
    
    name = 'inmueble'
    headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    num_anuncios_por_pagina = 24
    main_web = 'https://urbania.pe'
    
    avisoinfo_regex = {
    'Lat': r'((\'mapLat\':) ?-(\d+.\d+))',
    'Long':r'((\'mapLng\':) ?-(\d+.\d+))',
    'Direccion': r"(\'address\':\s?{(\"name\":\")(.*?)\")",
    'Descripcion':r'((\'description\'): ((".*?)"))',
    'Barrio':r'((\'neighborhood\')\s?:\s?((\'.*?)\'))',
    'Ciudad':r'((\'city\')\s?:\s?((\'\w+\')))',
    'Precio':r"(('price':?\s?)(('.*?)'))",
    'Anunciante': r"(('publisher'):\s?({(.*?)}))",
    #In regards of being another dict, this pattern will be inside the same AvisoInfo script.
    'json_general_features': r"(('generalFeatures')\s?:\s?(({\".*?)}}}))",
    'json_images': r"(('pictures')\s?:\s?(\[{\".*?)}\])"
    }
    
    ul_details = {
    'metros totales': 'icon-stotal',
    'metros cubierta': 'icon-scubierta',
    'numero banios':'icon-bano',
    'estacionamientos':'icon-cochera',
    'dormitorios':'icon-dormitorio',
    'antiguedad':'icon-antiguedad',
    'medio banio':'icon-toilete'
    }
    
    scraper = cfscrape.create_scraper()

    def __init__(self, pagina_principal, num_paginas):
        self.num_paginas = num_paginas #input de paginas
        self.pagina_principal = pagina_principal #inputs
        self.lista_links = [self.pagina_principal+str(i) for i in range(num_paginas[0],num_paginas[1])]
        self.dicc_scraping = {}
        
    def extraer_lista_links_internos(self):
        """
        Generator: Hace el request a la página principal y extrae los links internos 
        (especificacion de cada casa).
        
        """
        for link in self.lista_links:
            time.sleep(0.65)
            response = self.scraper.get(link, headers = self.headers)
            soup_pagina_principal = BeautifulSoup(response.text, "html.parser")
            posts_pagina = soup_pagina_principal.find_all('div',{'class','postingCardTop'})
            yield [self.main_web + i.find('a',{'class':'go-to-posting'}).attrs['href'] for i in posts_pagina]
    
    def busqueda_regex_en_soup(self, soup, regex_dict, link):
        """
        Para cada soup, busca las palabras y devuelve un diccionario.
        
        soup: html a buscar sobre.
        regex_dict: patrones regex por sobre los que buscar
        """

        dicc_inmueble = {}
        
        script_precioventa = soup.find('script', string=re.compile('avisoInfo'))
        ul_soup =soup.find('ul', {'class':'section-icon-features'})
        div_mantenimiento = soup.find('div',{'class':'block-expensas block-row'})

        regex_parser = re.compile(r'[\n\r\t]')
        dicc_inmueble['link'] = link
        if script_precioventa is not None:
            string_script = regex_parser.sub(' ',str(script_precioventa))
            for clase_datos, patron in self.avisoinfo_regex.items():
                match = re.search(patron, string_script)
                if match is None:
                    dicc_inmueble[clase_datos] = np.nan
                else:
                    dicc_inmueble[clase_datos] = match.group(3)
                    
        if ul_soup is not None:
            string_ul = regex_parser.sub(' ', str(ul_soup))
            general_regex_ul = r'((<i class="{}"></i>\s*?(\d+)))'

            for clase_datos, patt_complement in self.ul_details.items():
                patron = general_regex_ul.format(patt_complement)
                match = re.search(patron, string_ul)
                if match is None:
                    dicc_inmueble[clase_datos] = np.nan
                else:
                    dicc_inmueble[clase_datos] = match.group(3)

        if div_mantenimiento is not None:
            dicc_inmueble['Mantenimiento'] = div_mantenimiento.span.text
        else:
            dicc_inmueble['Mantenimiento'] = 0

        return dicc_inmueble
    
    def almacenamiento_de_busquedas(self):
        """
        Iteración por sobre los links y diccionario padre.
        """
        n=0
        Generator_links = self.extraer_lista_links_internos()
        try:
            while True:
                lista_links_internos_temp = next(Generator_links)
                for link_interno in lista_links_internos_temp:
                    n+=1
                    response = self.scraper.get(link_interno, headers = self.headers)
                    soup_pagina_inmueble = BeautifulSoup(response.text, "html.parser")
                    self.dicc_scraping[str(n)] = self.busqueda_regex_en_soup(soup=soup_pagina_inmueble,\
                                                                               regex_dict = self.avisoinfo_regex,
                                                                                       link=link_interno)
                    #Para version local.
                    sys.stdout.write(' {} '.format(n))
                    sys.stdout.flush()
                    time.sleep(0.854)
                print('\n')
        except:
            return self.dicc_scraping