import cloudscraper


class Scraper:
    """
    asdasd
    """
    def __init__(self, apibase, cache_token, base_dir, ignore_cache):

        self.session = cloudscraper.create_scraper(
            browser={"browser":"firefox", "platform":"windows", "mobile":"False"}
        )

        self.apibase = apibase
        self.cache_token = cache_token
        self.base_dir = base_dir
        self.ignore_cache = ignore_cache
        self.cache_dir = base_dir / "_cache" / self.cache_token


    def get_cache_path_for_url(self, url):
        """
        """
        res = url
        