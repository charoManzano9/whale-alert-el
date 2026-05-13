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
from datetime import datetime, timezone
from typing import List, Dict
from logging import Logger, FileHandler, Formatter, DEBUG

def whale_alert_extractor() -> Dict[str, List[str]] | None:
    
    logger = Logger("whale_alert_extractor_logger")
    file_handler = FileHandler('logs.log')
    logger.setLevel(DEBUG)
    logger.info("Iniciando")
    logger.addHandler(file_handler)
        
    url = "https://whale-alert.io/whales.html"
    try:
        response = requests.get(url)
        logger.debug(f'obteniendo informacion de {url}')
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.content, 'html.parser')
        table_rows = soup.select('table.table tbody tr')

        data = { 
                    "datetime_utc": [datetime.now(timezone.utc)] * len(table_rows), 
                    "crypto": [
                        row.find("th", {"scope": "row"}).find("img")["alt"].strip() 
                        if row.find("th", {"scope": "row"}).find("img") 
                        else row.find("th", {"scope": "row"}).get_text(strip=True) 
                        for row in table_rows
                    ],
                    "known": [row.find_all("td")[0].get_text(strip=True) for row in table_rows], 
                    "unknown": [row.find_all("td")[1].get_text(strip=True) for row in table_rows] 
                }
        logger.info(f'Datos extraidos: {len(data)} filas')
        return data
    except Exception as e:
        logger.error(f'Error al extraer los datos: {e}')
        return None

data = whale_alert_extractor()

whale_alert_df = pd.DataFrame(data)

whale_alert_df.to_csv(f"data/whales_{datetime.now().strftime('%Y-%m-%d')}.csv", index=False, encoding='utf-8')