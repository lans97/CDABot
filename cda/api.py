import logging
import mysql.connector
import secretos

from datetime import datetime

from typing import List, Dict, Iterable

# Logger configuration
logging.basicConfig(level=logging.ERROR)

file_handler = logging.FileHandler('cdaAPI.log')
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger().addHandler(file_handler)

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host=secretos.sqlcred['SQL_HOST'],
            user=secretos.sqlcred['SQL_USER'],
            password=secretos.sqlcred['SQL_PASSWORD'],
            database=secretos.sqlcred['SQL_DATABASE']
        )
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Database connection error: {e}")
        return None

def close_database_connection(conn):
    if conn:
        conn.close()

def execute_query(conn, query, params=None):
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result
    except mysql.connector.Error as e:
        logging.error(f"Query execution error: {e}")
        return None


def list_sensor(token: str) -> List[Dict[str, str]]:
    result = []

    conn = connect_to_database()
    if not conn:
        return result

    query = "SELECT Sensor.ID_Sensor, Sensor.Descript FROM Sensor, LEFT JOIN Device ON Sensor.ID_Device = Device.ID_Device"

    query_result = execute_query(conn, query)
    for row in query_result:
        result.append({"idSensor": str(row[0]), "description": str(row[1])})

    close_database_connection(conn)
    return result


def get_data(token: str, idSensor: Iterable[int], dtStart: datetime, dtEnd: datetime) -> List[List[Dict[str, str]]]:
    result = []

    conn = connect_to_database()
    if not conn:
        return result

    query = """
    SELECT Sample.Sample_Data, Sample.Time_Data
    FROM Sample
        LEFT JOIN Sensor ON Sample.ID_Sensor = Sensor.ID_Sensor
        LEFT JOIN Device on Sensor.ID_Device = Device.ID_Device
    WHERE Sample.Time_Data BETWEEN  %s AND %s
    AND Device.Token = %s
    AND Sensor.Sensor_No = %s
    ORDER BY Sample.Time_Data DESC
    """

    dtStart_str = dtStart.strftime('%Y-%m-%d %H:%M:%S')
    dtEnd_str = dtEnd.strftime('%Y-%m-%d %H:%M:%S')

    for sensor_no in idSensor:
        sensor_result = []

        query_result = execute_query(conn, query, (dtStart_str, dtEnd_str, token, sensor_no))
        if query_result is not None:
            for row in query_result:
                sensor_result.append({"Data": str(row[0]), "TimeStamp": str(row[1])})
            result.append(sensor_result)

    close_database_connection(conn)
    return result
