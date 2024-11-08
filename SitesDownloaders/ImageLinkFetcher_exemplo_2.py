import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# this a code for dowloads from "https://nome do site/g/(number of manga)/"

class ImageLinkFetcher_exemplo_2:
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
        time.sleep(3)

        thumbnails_container = driver.find_element(By.ID, 'thumbnail-container')
        thumbnails = thumbnails_container.find_elements(By.CSS_SELECTOR, 'a.gallerythumb img')

        for thumbnail in thumbnails:
            img_src = thumbnail.get_attribute('data-src')
            if img_src:
                img_src = img_src.replace('https://t', 'https://i').rstrip('t.png') + '.png' if img_src.endswith('.png') else img_src.replace('https://t', 'https://i').rstrip('t.jpg') + '.jpg'
                self.image_links.append(img_src)

        driver.quit()

    def get_image_links(self):
        return self.image_links
