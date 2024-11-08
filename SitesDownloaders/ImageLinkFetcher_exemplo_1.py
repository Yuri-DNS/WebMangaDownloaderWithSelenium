import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# this a code for dowloads from "https://nome do site/capitulo/(Manga desjado)/"

class ImageLinkFetcher_exemplo_1:
    def __init__(self, url):
        self.url = url
        self.image_links = []

    def fetch_image_links(self):
        # Definir opções para o Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(self.url)
        time.sleep(3)  # Espera pela página carregar

        # Encontra todas as tags <img> com a classe ou outros atributos que identificam as imagens
        images = driver.find_elements(By.CSS_SELECTOR, 'img[loading="lazy"]')

        # Percorre todas as imagens e armazena os links no atributo 'src'
        for img in images:
            img_src = img.get_attribute('src')
            if img_src:
                self.image_links.append(img_src)

        driver.quit()

    def get_image_links(self):
        return self.image_links

