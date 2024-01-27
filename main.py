import os
import requests
import base64
import csv
import hashlib
import json
import random
import string
import secrets
import uuid
from datetime import datetime
from urllib.parse import quote

# Les constantes 

URL = "https://dummyjson.com/products"
FIRST_NAME = 'Doumbia' 
LAST_NAME = 'Ayouba'
DOWNLOAD_FOLDER = "Downloads"

# Les fonctions

def encode_to_base64(data):
    """Encode la donnée reçu en base64"""
    return base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')

def hash_images_urls(images_urls):
    """Hashe tous les URLs des images et les concatène avec '!::!' en utilisant MD5"""
    concatenated_urls = '!::!'.join(images_urls)
    return hashlib.md5(concatenated_urls.encode('utf-8')).hexdigest()

def generate_secure_password(length=8):
    """Génère un mot de passe aléatoire à partir d'une source cryptographiquement sûre."""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_non_secure_password(length=8):
    """Génère un mot de passe aléatoire à partir d'une source pas cryptographiquement sûre."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def transform_product(product):
    """Prend les données d'un produit (dictionnaire) et retourne un nouveau dictionnaire avec des colonnes en plus"""
    product['my_date'] = datetime.now().isoformat()
    product['my_json_data_in_base64'] = encode_to_base64(product)
    product['my_encoded_thumbnail'] = quote(product['thumbnail'])
    product['uuid_version_4'] = str(uuid.uuid4())
    product['all_these_images_urls_hashes'] = hash_images_urls(product['images'])
    product['very_safe_password'] = generate_secure_password()

    product['totally_not_safe_password'] = generate_non_secure_password()

    return product


# ETL
try:
    response = requests.get(URL)
    response.raise_for_status()  # Soulever une erreur HTTP si c'est le cas 

    data_extracted = response.json() 

    if not os.path.exists(DOWNLOAD_FOLDER): # Si jamais le dossier "Download" n'existe pas on la crée
        os.makedirs(DOWNLOAD_FOLDER)

    file_name = f"Downloads/{FIRST_NAME}_{LAST_NAME}_MY_FILE.csv" # Constitution du nom du fichier avec le nom et le prénom

    # Si la réponse n'est pas vide commencer la transformation
    if data_extracted:
        products_list = data_extracted['products']

        # liste pour constituer les lignes de produits (avec transformation)
        transformed_products = []

        for product in products_list:
            transformed_product = transform_product(product)
            transformed_products.append(transformed_product)

        # Ajouter les lignes de données de chaque produits dans le fichier CSV
        file_name = f"Downloads/{FIRST_NAME}_{LAST_NAME}_MY_FILE.csv"
        with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=transformed_products[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(transformed_products)

    else:
        print("Aucune donnée fournie.")

except requests.exceptions.RequestException as e:
    print(f"Erreur lors de l'extraction via l'api : {e}")
except json.JSONDecodeError as e:
    print(f"Erreur lors du décodage de la donnée reçu par l'api : {e}")
except Exception as e:
    print(f"Une erreur est survenue : {e}")