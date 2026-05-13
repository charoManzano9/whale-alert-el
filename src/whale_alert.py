''' 
1 - Request a whale alert
2 - utilizar beautifulSoup para extraer informacion
3 - parsear la data que me devuelve el response 
4 - utilizar pandas para transformar la data a un dataframe 
5 - cargar el dataframe a un archivo csv YYYY-MM-DD
6 - subir el archivo csv a un bucket de minio
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://whale-alert.io/whales.html"
response = requests.get(url)
print(response)



