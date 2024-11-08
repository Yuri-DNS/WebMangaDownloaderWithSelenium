Este projeto oferece uma solução eficiente para baixar imagens de capítulos de mangás a partir de URLs específicas. Ele utiliza um sistema modular, onde diferentes *fetchers* (recolhedores de links) são escolhidos dinamicamente com base na URL fornecida, permitindo que o código seja facilmente adaptado a diferentes sites.

## Funcionalidades

- **LinkFetcherChooser**: Escolhe automaticamente o *fetcher* adequado para extrair links de imagens, dependendo da URL fornecida (suporta múltiplos sites).
- **ImageSaver**: Baixa as imagens extraídas e as salva em diretórios organizados, com suporte a downloads paralelos usando múltiplas threads para melhorar a performance.
- **Execução automática**: Após o download das imagens, o script executa um processo adicional (`mangaReader.py`) dentro de um diretório específico.

## Como Funciona

1. O código seleciona o *fetcher* adequado para a URL do mangá.
2. O *fetcher* coleta os links das imagens do capítulo.
3. As imagens são baixadas de forma eficiente com múltiplas threads.
4. O script executa `mangaReader.py` automaticamente no diretório correto.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Selenium**: Para acessar e interagir com páginas web dinamicamente.
- **Requests e Threads**: Para download eficiente de múltiplas imagens simultaneamente.
- **PIL (Pillow)**: Para verificar a validade das imagens.

Este repositório oferece uma maneira prática e escalável de automatizar o processo de download de mangás, com suporte a diferentes sites e flexibilidade na escolha das configurações.
