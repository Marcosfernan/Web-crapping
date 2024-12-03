import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.foorli.com.br/produtos'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

# Lista para armazenar informações dos produtos
products_info = []

# Loop através de várias páginas (caso haja paginação)
for page in range(1, 6):  # Ajuste o número de páginas conforme necessário
    try:
        response = requests.get(f'{url}?p={page}', headers=headers)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        soup = BeautifulSoup(response.content, 'lxml')

        # Buscando os elementos que possuem a classe especificada
        product_list = soup.find_all('a', class_='js-item-name item-name product-item_name')

        for item in product_list:
            product_data = {
                'href': item.get('href'),
                'title': item.get('title'),
                'data-product-id': item.get('data-product-id'),
                'product_name': item.text.strip()
            }
            products_info.append(product_data)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página {page}: {e}")
        continue

# Mostrando todos os dados extraídos antes de salvar no CSV
for product in products_info:
    print(f"Link: {product['href']}")
    print(f"Título: {product['title']}")
    print(f"ID do Produto: {product['data-product-id']}")
    print(f"Nome do Produto: {product['product_name']}")
    print('-' * 40)

# Salvando os dados em um arquivo CSV
csv_file = 'C:\\Users\\Jurandir\\SkyDrive\\Documents\\dd\\foorli_produtos.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['href', 'title', 'data-product-id', 'product_name'])
    writer.writeheader()
    writer.writerows(products_info)

print(f"Dados salvos no arquivo {csv_file}")