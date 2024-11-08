from concurrent.futures import ThreadPoolExecutor
import os
import time
import requests
import threading
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse

class ImageSaver:
    def __init__(self, image_links, url, max_threads=10):  # Adicionando o parâmetro max_threads
        # Extrair o nome da pasta da URL
        parent_folder = "Mangas/"  # Nome da pasta pai
        self.save_folder = os.path.join(parent_folder, self.extract_folder_name_from_url(url))
        self.image_links = image_links
        self.success_counter = []
        self.failure_counter = []

        self.success_counter_lock = threading.Lock()
        self.failure_counter_lock = threading.Lock()
        self.max_threads = max_threads  # Definindo o número máximo de threads

    @staticmethod
    def extract_folder_name_from_url(url):
        # Extraímos o caminho da URL e removemos qualquer barra extra no final
        path = urlparse(url).path.strip('/')
        # Usamos a última parte do caminho como nome da pasta
        folder_name = path.split('/')[-1]
        return folder_name

    class ImageLoader:
        def __init__(self, url, success_counter, failure_counter, save_path, success_counter_lock, failure_counter_lock, image_number):
            self.url = url
            self.retries = 15
            self.success_counter = success_counter
            self.failure_counter = failure_counter
            self.save_path = save_path
            self.success_counter_lock = success_counter_lock
            self.failure_counter_lock = failure_counter_lock
            self.image_number = image_number  # Nome da imagem baseado no número

        def run(self):
            for attempt in range(self.retries):
                try:
                    response = requests.get(self.url, timeout=10)
                    response.raise_for_status()
                    img_data = response.content
                    if self.is_valid_image(img_data):
                        self.save_image(img_data)
                        with self.success_counter_lock:
                            self.success_counter.append(self.url)
                        break
                    else:
                        print(f"Formato inválido para a imagem: {self.url}")
                        with self.failure_counter_lock:
                            self.failure_counter.append(self.url)
                        break
                except Exception as e:
                    print(f"Erro ao carregar a imagem: {self.url}. Tentativa {attempt + 1}. Erro: {e}")
                    if attempt == self.retries - 1:
                        with self.failure_counter_lock:
                            self.failure_counter.append(self.url)
                    time.sleep(1)

        def is_valid_image(self, img_data):
            try:
                image = Image.open(BytesIO(img_data))
                image.verify()
                return True
            except Exception:
                return False

        def save_image(self, img_data):
            # Formato do nome da imagem em sequência: 0001, 0002, 0003, etc.
            filename = f"{self.image_number:04d}.jpg"  # Adiciona zeros à esquerda para garantir 4 dígitos
            full_path = os.path.join(self.save_path, filename)
            with open(full_path, 'wb') as img_file:
                img_file.write(img_data)

    def save_images(self):
        # Cria a pasta onde as imagens serão salvas
        os.makedirs(self.save_folder, exist_ok=True)

        # Usando ThreadPoolExecutor para gerenciar threads
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            # Envia cada tarefa de download de imagem para execução
            futures = []
            for index, image_url in enumerate(self.image_links, start=1):
                loader = self.ImageLoader(image_url, self.success_counter, self.failure_counter, self.save_folder,
                                          self.success_counter_lock, self.failure_counter_lock, index)
                futures.append(executor.submit(loader.run))  # Adiciona a tarefa à pool de threads

            # Aguarda todas as tarefas serem concluídas
            for future in futures:
                future.result()  # Espera que o futuro termine (verifica se houve exceções)

        print(f"Tentativas bem-sucedidas: {len(self.success_counter)}")
        print(f"Tentativas malsucedidas: {len(self.failure_counter)}")
        if self.failure_counter:
            print("Imagens malsucedidas:")
            for url in self.failure_counter:
                print(url)
