import subprocess
import os
from ImageSaver import ImageSaver
from LinkFetcherChooser import LinkFetcherChooser

url = "https://Exemplo.com/capitulo/3181/"

# Escolher qual LinkFetcher usar com base na URL
fetcher_chooser = LinkFetcherChooser(url)
link_fetcher = fetcher_chooser.choose_fetcher()

if link_fetcher:
    link_fetcher.fetch_image_links()
    image_links = link_fetcher.get_image_links()

    # Se houver links de imagens, salvá-los usando ImageSaver
    if image_links:
        save_folder = url
        image_saver = ImageSaver(image_links, save_folder)
        image_saver.save_images()
    else:
        print(f"Nenhuma imagem válida encontrada para a URL: {url}")
else:
    print(f"Fetcher não disponível para a URL: {url}")


# Caminho para o diretório onde mangaReader.py está localizado
mangas_dir = os.path.join(os.path.dirname(__file__), 'Mangas')

# Muda o diretório de trabalho para a pasta 'Mangas'
os.chdir(mangas_dir)

# Agora executa o mangaReader.py no diretório correto
subprocess.run(['python', 'mangaReader.py'])
