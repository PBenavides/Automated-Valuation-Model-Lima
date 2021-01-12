class ScrapingStructure():
    """
    Idealmente para otras páginas? 
    Idealmente para coger información según tipo de inmueble.
    """
    @staticmethod
    def UrbaniaStructure():
        base_link = 'https://urbania.pe/buscar/venta-de-{}?page='

        return [
            {
                'Tipo':'casas',
                'url': base_link.format('casas'),
                'max_page': 1
            },

            {
                'Tipo':'terrenos',
                'url': base_link.format('terrenos'),
                'max_page': 1
            },

            {
                'Tipo':'locales-comerciales',
                'url':base_link.format('locales-comerciales'),
                'max_page': 1
            }
        ]