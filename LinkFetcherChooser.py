from SitesDownloaders.ImageLinkFetcher_exemplo_1 import ImageLinkFetcher_exemplo_1
from SitesDownloaders.ImageLinkFetcher_exemplo_2 import ImageLinkFetcher_exemplo_2


class LinkFetcherChooser:
    def __init__(self, url):
        self.url = url

    def choose_fetcher(self):
        if "mangaonline.biz" in self.url:
            return ImageLinkFetcher_exemplo_1(self.url)
        elif "nome_do_site_2.net" in self.url:
            return ImageLinkFetcher_exemplo_2(self.url)
        else:
            print("URL não suportada.")
            return None
