# Wrapper para API de Smability
from datetime import datetime
import requests
import logging

logger = logging.getLogger('smability_logger')
logger.setLevel(logging.ERROR)  # Set the logging level as needed

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('smability.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_data(token: str, sensors: tuple, date_0: datetime, date_f: datetime):
    """Get sensor measures from date_0 to date_f"""
    start = date_0.replace(microsecond=0)
    end = date_f.replace(microsecond=0)
    output = []
    url = 'http://smability.sidtecmx.com/smabilityapi/GetData?'
    for n in sensors:
        query = {'dtstart': start, 'dtend': end, 'token': token, 'idsensor': str(n)}
        logger.info(f"Getting data from {token}: {n}.")
        try:
            response = requests.get(url, params=query)
        except Exception as e:
            logger.error(e)
            return None
        data = response.json()
        if data is None:
            output.append({})
        else:
            if len(data) != 0:
                output.append(data)
            else:
                output.append({})
    return output

def list_sensor(token: str):
    """Get sensor description and IDs from a given device toke from a given device token"""
    url = 'http://smability.sidtecmx.com/smabilityapi/ListSensor?'
    query = {'token': token}
    try:
        response = requests.get(url, params=query)
    except Exception as e:
        logger.error(e)
        return None
    data = response.json()
    return data

def bio_box(token: str):
    """Get last data from sensor"""
    url = 'http://smability.sidtecmx.com/smabilityapi/BioBox?'
    query = {'token': token}
    try:
        response = requests.get(url, params=query)
    except Exception as e:
        logger.error(e)
        return None
    data = response.json()
    return data