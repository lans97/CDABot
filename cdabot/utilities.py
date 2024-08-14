import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
from matplotlib.patches import Wedge
import mplcyberpunk
import pytz
import matplotlib.dates as mdates
import plotly.express as px

import pandas as pd
import pytz

from datetime import datetime, timedelta
import numpy as np
import json
from googletrans import Translator

import os
import re
from io import BytesIO
from PIL import Image

from cdabot import smability
from secretos import sensores

import logging

logging.basicConfig(level=logging.ERROR)

file_handler = logging.FileHandler('cdaBot.log')
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger().addHandler(file_handler)


def sensor_avg_last_24hrs(device: str, idSensor: int) -> float:
    end = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - timedelta(days=1)
    try:
        data = smability.get_data(sensores[device], (idSensor, ), start, end)[0]
        if (len(data) > 0):
            sum = 0.0
            for el in data:
                sum += float(el["Data"])
            return sum/len(data)
        else:
            raise Exception("No data from API")

    except Exception as e:
        logging.error(e)
        return None

def sensor_data_per_day(device: str, idSensor: int, n_days_ago: int = 1) -> list:
    start = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=n_days_ago)
    if n_days_ago == 0:
        end = datetime.today()
    else:
        end = start + timedelta(days=1)

    try:
        data = smability.get_data(sensores[device], (idSensor, ), start, end)[0]
        if (len(data) > 0):
            return data
        else:
            raise Exception("No data from API")

    except Exception as e:
        logging.error(e)
        return None


def sensor_avg_per_day(device: str, idSensor: int, n_days_ago: int = 0) -> float:
    try:
        data = sensor_data_per_day(device, idSensor, n_days_ago)
        sum = 0.0
        for el in data:
            sum += float(el["Data"])
        return sum/len(data)

    except Exception as e:
        logging.error(e)
        return None

def analyze_environment(device: str) -> str:
    # Obtener el promedio de las 24 horas de cada uno de los sensores
    pm25 = sensor_avg_last_24hrs(device, 9)  # P.M. 2.5
    if pm25 == None:
        return None
    pm10 = sensor_avg_last_24hrs(device, 8)  # P.M. 10
    if pm10 == None:
        return None
    ozone = sensor_avg_last_24hrs(device, 7)  # Ozono
    if ozone == None:
        return None
    co = sensor_avg_last_24hrs(device, 2)  # CO
    if co == None:
        return None
    temperature = sensor_avg_last_24hrs(device, 12)  # Temperatura
    if temperature == None:
        return None
    humidity = sensor_avg_last_24hrs(device, 3)  # Humedad
    if humidity == None:
        return None

    # Calcular los valores correspodientes para la obtencion de un resumen, se llama a las fuciones correspondientes
    pm25eval = evaluate_pm25(pm25)
    pm10eval = evaluate_pm10(pm10)
    ozonoeval = evaluate_ozone(ozone)
    coeval = evaluate_co(co)
    temperaturaeval = evaluate_temperature(temperature)
    humedadeval = evaluate_humidity(humidity)

    # Calcular el total de calidad de aire
    total = pm25eval + pm10eval + ozonoeval + coeval + temperaturaeval + humedadeval
    calidadA = calculate_quality(total)

    return calidadA


def insert_line_breaks(text, line_length=60):
    lines = []
    current_position = 0
    while current_position < len(text):
        end_position = min(current_position + line_length, len(text))
        if end_position < len(text) and text[end_position] != ' ':
            # AttributeError: 'str' object has no attribute 'rfindtranslated_descrip'
            space_position = text.rfindtranslated_descrip(' ', current_position, end_position)
            if space_position != -1:
                end_position = space_position
            else:
                space_position = text.find(' ', end_position)
                if space_position != -1:
                    end_position = space_position

        lines.append(text[current_position:end_position])
        current_position = end_position + 1

    return '\n'.join(lines)


def categoria_aire_f(device: str) -> str:

    d0 = datetime.today()
    try:
        data = smability.get_data(sensores[device], (1001, ), d0, d0)[0]
    except Exception as e:
        logging.error(e)
        return None


    if len(data[0]) < 1:
        return None

    json_data = data[0]["Data"]

    data_dict = json.loads(json_data)

    descrip = data_dict["Description"]
    descripSalud = data_dict["Health"]
    descripData = data_dict["Data"]
    descrip = str(descrip)
    descripSalud = str(descripSalud)
    descripData = int(descripData)

    descrip = str(descrip)

    # Translate the description to Spanish
    translator = Translator()
    translated_descrip = translator.translate(descrip, dest='es').text
    translated_descrip2 = translator.translate(descripSalud, dest='es').text

    colores = data_dict["Color"]
    colores = str(colores)

    combined_info = ''
    value_to_annotate = 0

    # Definicio de caracteristicas por código de color

    if colores == "#00E400":
        combined_info = translated_descrip
        value_to_annotate = descripData
    elif colores == "#00E400":
        combined_info = translated_descrip
        value_to_annotate = descripData
    elif colores == "#FF7E00":
        combined_info = translated_descrip
        value_to_annotate = descripData
    elif colores == "#FF0000":
        combined_info = translated_descrip
        value_to_annotate = descripData
    elif colores == "#8F3F97":
        combined_info = translated_descrip
        value_to_annotate = descripData
    elif colores == "#7E0023":
        combined_info = translated_descrip + translated_descrip2
        value_to_annotate = descripData

    contaminante1 = data_dict["lastPM25"]
    contaminante2 = data_dict["lastPM10"]
    contaminante3 = data_dict["lastO3"]
    contaminante4 = data_dict["lastCO"]

    contaminante1 = str(contaminante1)
    contaminante2 = str(contaminante2)
    contaminante3 = str(contaminante3)
    contaminante4 = str(contaminante4)

    # Definicion del texto

    tweet_text = f"Reporte de contaminantes({d0}):\nConcentración - AQI\n{contaminante1}\n{contaminante2}\n{contaminante3}\n{contaminante4}"

    mpl.rcParams['text.color'] = 'white'

    translated_descrip_jump = insert_line_breaks(combined_info)

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'aspect': 'equal'}, facecolor='#212946')

    # Creación de la gráfica, variación de colores y ranfo
    cmap = mpl.colors.ListedColormap(['#00E400', '#FFFF00', '#FF7E00', '#FF0000', '#8F3F97', '#7E0023'])
    bounds = [0, 50, 100, 150, 200, 300, 500]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # Graficar en forma de dona
    for i in range(len(bounds) - 1):
        wedge = Wedge(center=(0.5, 0.5), r=0.45, theta1=(bounds[i] / 500) * 180, theta2=(bounds[i + 1] / 500) * 180,
                      width=0.15, facecolor=cmap.colors[i], transform=ax.transAxes)
        ax.add_patch(wedge)

    # Parametros de la aguja
    needle_angle = (descripData / 500) * 180
    ax.plot([0.5, 0.5 + 0.4 * np.cos(np.radians(needle_angle))],
            [0.5, 0.5 + 0.4 * np.sin(np.radians(needle_angle))],
            transform=ax.transAxes, color='white', lw=3)

    # Añadir el texto y los ejes
    ax.set_title('Air Quality Index (AQI)', color='white', fontsize=15)
            
    ax.text(0.5, 0.31, translated_descrip_jump, transform=ax.transAxes,
            ha='center', va='center', color='white', fontsize=12)
            
    ax.text(0.5, 0.47, f'⚠ Peligroso                                                               Saludable 😀', transform=ax.transAxes,
            ha='center', va='center', color='white', fontsize=10, fontname='Arial Unico, MS')

    # Aspecto visual del radio
    ax.set_aspect('equal')
    ax.axis('off')

    footer_text = f'\nGenerado por Smability Data Analyzer, consulta: {d0}'
    fig.text(0.13, 0.2, footer_text, ha='left', fontsize=6, color='white', fontfamily='sans-serif')

    # Aplicación del logo
    img = Image.open('cdabot/Recursos/logo.jpg')
    img.thumbnail((100, 100))
    fig.figimage(img, xo=70, yo=530, alpha=1)

    plt.savefig('images/graph.png')

    return tweet_text


def generar_grafica(device: str, sensor: int, days: int = 1) -> tuple[str, float]:
    if not os.path.exists("images"):
        os.mkdir("images")

    if not os.path.exists("files"):
        os.mkdir("files")

    df = datetime.today().replace(minute=0, second=0, microsecond=0)
    d0 = df - timedelta(days=days)

    date_fmt = "%Y-%m-%d-%Hhrs"

    try:
        data = smability.get_data(sensores[device], (sensor, ), d0, df)[0]
        datacsv = pd.DataFrame(data)
    except Exception as e:
        logging.error(e)
        return None

    if len(data) < 1:
        return None

    y = np.array([float(d["Data"]) for d in data])
    x = np.array([datetime.strptime(d["TimeStamp"], "%Y-%m-%dT%H:%M:%S") for d in data])

    max_value = np.max(y)
    avg = np.mean(y)

    # Matplotlib setup
    plt.style.use('cyberpunk')
    fig, ax = plt.subplots(figsize=(10, 6))

    match sensor:
        case 9:
            # P.M. 2.5
            long_var = "P.M. 2.5"
            short_var = "PM25"
            units = "ug/m3"
        case 8:
            # P.M. 10
            long_var = "P.M. 10"
            short_var = "PM10"
            units = "ug/m3"
        case 7:
            # Ozono
            long_var = "OZONO"
            short_var = "O3"
            units = "ppb"
        case 2:
            # CO
            long_var = "MONÓXIDO DE CARBONO"
            short_var = "CO"
            units = "ppb"
        case 12:
            # Temperatura
            long_var = "TEMPERATURA"
            short_var = "Temperatura"
            units = "°C"
        case 23:
            # Lluvia
            long_var = "INTENSIDAD DE LLUVIA"
            short_var = "Lluvia"
            units = "mm/h"
        case 3:
            # Humedad
            long_var = "HUMEDAD"
            short_var = "Humedad"
            units = "%"
        case 27:
            # Radiación
            long_var = "RADIACIÓN"
            short_var = "Radiación"
            units = "W/m2"

    main_lbl = f"REPORTE: {long_var} \nDEL {d0.strftime('%Y-%m-%d')} AL {df.strftime('%Y-%m-%d')}"
    line_lbl = f"{short_var} [{units}]"
    avg_lbl = f"Promedio {short_var} [{units}]"

    # Encontrar el valor máximo
    max_index = np.argmax(y)
    min_index = np.argmin(y)
    max_value = y[max_index]
    min_value = y[min_index]

    ax.plot(x, y, "C0", label=line_lbl)
    ax.axhline(y=avg, color='#FE53BB', linestyle='--', label=avg_lbl)

    ax.set(xlim=(np.min(x), np.max(x)), ylim=((min_value*0.65), (max_value*1.1)), xlabel="Fecha (DD, HH, MM)", ylabel=f"{long_var} {units}")

    # Formato de la fecha en el eje x
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%D, %H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=30))
    fig.autofmt_xdate()
    plt.setp(ax.get_xticklabels(), fontsize=8)
    
    ax.yaxis.label.set_color("C0")

    # Leyenda
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels)
    mplcyberpunk.make_lines_glow()
    mplcyberpunk.add_underglow()

    # Determinar la posición de xytext
    mid_point = len(x) // 2
    if max_index > mid_point:
        coordt = (-180, -30)
    else:
        coordt = (20, -30)

    # Formato de valor máximo
    ax.annotate(f'Mayor valor: {max_value}{units}\nRecuperado el: {x[max_index]}', xy=(x[max_index], y[max_index]), xytext=coordt,
            textcoords='offset points', arrowprops=dict(arrowstyle="->", color='white', connectionstyle="arc3,rad=.2"))

    footer_text = f'Generado por Smability Data Analyzer, consulta: {d0}'
    fig.text(0.1, 0.1, footer_text, ha='left', fontsize=6, color='white', fontfamily='sans-serif')

    # Configuracion del logo
    img = Image.open('cdabot/Recursos/logo.jpg')
    img.thumbnail((100, 100))
    fig.figimage(img, xo=40, yo=540, alpha=1)

    plt.title(main_lbl, fontsize=25, fontweight='bold', fontfamily='sans-serif')
    fig.savefig("images/latest.png")

    fig.clear()
    img_path = "images/latest.png"

    csv_filename = "files/latest.csv"
    datacsv.to_csv(csv_filename, index=False)

    return (img_path, max_value)


def generar_grafica_alt(device: str, sensor: int, days: int = 1) -> tuple[str, float]:
    if not os.path.exists("images"):
        os.mkdir("images")

    if days < 1:
        days = 1

    df = datetime.today().replace(minute=0, second=0, microsecond=0)
    d0 = df - timedelta(days=days)

    date_fmt = "%Y-%m-%d-%Hhrs"

    matches = find_filename_pattern("images", rf"reporte-{device}-{sensor}-{d0.strftime(date_fmt)}-{df.strftime(date_fmt)}-[\d+\.\d+]+\.png")
    if len(matches) == 0:
        try:
            data = smability.get_data(sensores[device], (sensor, ), d0, df)[0]
            datacsv = pd.DataFrame(data)
        except Exception as e:
            logging.error(e)
            return None

        if len(data) < 1:
            return None

        y = np.array([float(d["Data"]) for d in data])
        x = np.array([datetime.strptime(d["TimeStamp"], "%Y-%m-%dT%H:%M:%S") for d in data])

        max_value = np.max(y)
        avg = np.mean(y)

        img_name = f"reporte-{device}-{sensor}-{d0.strftime(date_fmt)}-{df.strftime(date_fmt)}-{max_value}.png"

        # Matplotlib setup
        plt.style.use('cyberpunk')
        fig, ax = plt.subplots(figsize=(10, 6))

        match sensor:
            case 9:
                # P.M. 2.5
                long_var = "P.M. 2.5"
                short_var = "PM25"
                units = "ug/m3"
            case 8:
                # P.M. 10
                long_var = "P.M. 10"
                short_var = "PM10"
                units = "ug/m3"
            case 7:
                # Ozono
                long_var = "OZONO"
                short_var = "O3"
                units = "ppb"
            case 2:
                # CO
                long_var = "MONÓXIDO DE CARBONO"
                short_var = "CO"
                units = "ppb"
            case 12:
                # Temperatura
                long_var = "TEMPERATURA"
                short_var = "Temperatura"
                units = "°C"
            case 23:
                # Lluvia
                long_var = "INTENSIDAD DE LLUVIA"
                short_var = "Lluvia"
                units = "mm/h"
            case 3:
                # Humedad
                long_var = "HUMEDAD"
                short_var = "Humedad"
                units = "%"
            case 27:
                # Radiación
                long_var = "RADIACIÓN"
                short_var = "Radiación"
                units = "W/m2"

        main_lbl = f"REPORTE: {long_var} \nDEL {d0.strftime('%Y-%m-%d')} AL {df.strftime('%Y-%m-%d')}"
        line_lbl = f"{short_var} [{units}]"
        avg_lbl = f"Promedio {short_var} [{units}]"

        # Encontrar el valor máximo
        max_index = np.argmax(y)
        min_index = np.argmin(y)
        max_value = y[max_index]
        min_value = y[min_index]

        ax.plot(x, y, "C0", label=line_lbl)
        ax.axhline(y=avg, color='#FE53BB', linestyle='--', label=avg_lbl)

        ax.set(xlim=(np.min(x), np.max(x)), ylim=((min_value*0.65), (max_value*1.1)), xlabel="Fecha (DD, HH, MM)", ylabel=f"{long_var} {units}")
        
        csv_filename = f"cdabot/Descargables/reporte-{device}-{sensor}-{d0.strftime(date_fmt)}-{df.strftime(date_fmt)}-{max_value}.csv"
        datacsv.to_csv(csv_filename, index=False)
        
        # Formato de la fecha en el eje x
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%D, %H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        ax.xaxis.set_major_locator(MaxNLocator(nbins=30))
        fig.autofmt_xdate()
        plt.setp(ax.get_xticklabels(), fontsize=8)
        
        ax.yaxis.label.set_color("C0")

        # Leyenda
        handles, labels = ax.get_legend_handles_labels()
        plt.legend(handles, labels)
        mplcyberpunk.make_lines_glow()
        mplcyberpunk.add_underglow()

        # Determinar la posición de xytext
        mid_point = len(x) // 2
        if max_index > mid_point:
            coordt = (-180, -30)
        else:
            coordt = (20, -30)

        # Formato de valor máximo
        ax.annotate(f'Mayor valor: {max_value}{units}\nRecuperado el: {x[max_index]}', xy=(x[max_index], y[max_index]), xytext=coordt,
                textcoords='offset points', arrowprops=dict(arrowstyle="->", color='white', connectionstyle="arc3,rad=.2"))

        footer_text = f'Generado por Smability Data Analyzer, consulta: {d0}'
        fig.text(0.1, 0.1, footer_text, ha='left', fontsize=6, color='white', fontfamily='sans-serif')

        # Configuracion del logo
        img = Image.open('cdabot/Recursos/logo.jpg')
        img.thumbnail((100, 100))
        fig.figimage(img, xo=40, yo=540, alpha=1)

        plt.title(main_lbl, fontsize=25, fontweight='bold', fontfamily='sans-serif')
        fig.savefig("images/" + img_name)

        fig.clear()
        img_path = "images/" + img_name
    else:
        img_path = "images/" + matches[0]
        max_value = float(re.findall(rf"([\d+\.\d]+)\.png", matches[0])[0])


    return (img_path, max_value)

# Se definen las direcciones de la rosa de los vientos
def map_angle_to_direction(angle):
    directions = ["N", "NE", "E", "SE", "S", "SO", "O", "NO", "NNE", "ENE", "ESE", "SSE", "SSO", "OSO", "ONO", "NNO"]
    angle_step = 360 / len(directions)
    normalized_angle = angle
    index = int(normalized_angle // angle_step)
    return directions[index]

# Se definen las direcciones de los chunks
def split_list(lst, chunk_size):
    chunks = [[] for _ in range((len(lst) + chunk_size - 1) // chunk_size)]
    for i, item in enumerate(lst):
        chunks[i // chunk_size].append(item)
    return chunks


# Se define la funcion que permite generar el GIF mediante una cantidad veariable de fotogramas
def create_windrose_plot(device: str, sensor: int, days: int = 1) -> tuple[str, float]:
    
    df = datetime.today().replace(minute=0, second=0, microsecond=0)
    d0 = df - timedelta(days=days)

    date_fmt = "%Y-%m-%d-%Hhrs"

    chunk_size = days * 46
    
    textRange = f'Solicitud del comportamiento del aire en las últimas {days*24} horas'
    
    alist = smability.get_data(sensores[device], (18, ), d0, df)[0]
    blist = smability.get_data(sensores[device], (19, ), d0, df)[0]

    alist_values = [item['Data'] for item in alist]
    blist_values = [item['Data'] for item in blist]
    fechas = [item['TimeStamp'] for item in alist]

    # Se extraen los datos de las listas
    df = pd.DataFrame({
        "axis": alist_values, 
        "velocidad": blist_values})

    # Se transfiere los valores flotantes
    df['axis'] = df['axis'].astype(float)

    # Se aplica una funcion de direccion
    df['direction'] = df['axis'].apply(map_angle_to_direction)

    # Fuerza a flotantes
    df['velocidad'] = df['velocidad'].astype(float)

    chunksa = split_list(df['direction'].tolist(), chunk_size)
    chunksb = split_list(df['velocidad'].tolist(), chunk_size)

    # Se definen los valores de los ejes en los que se comlacará la Rosa de los Vientos
    direction_labels = ["N", "NE", "E", "SE", "S", "SO", "O", "NO", "NNE", "ENE", "ESE", "SSE", "SSO", "OSO", "ONO", "NNO"]
    direction_angles = np.linspace(0, 360, len(direction_labels), endpoint=False)

    # Se aplica el color al mapeado
    i=0
    
    while i < len(chunksa):
        # Creación del apartado de frecuencia
        initial_value = 5
        dlist = [initial_value - 0.01 * j for j in range(len(chunksa[i]))]

        df_chunk = pd.DataFrame({
          "direction": chunksa[i],
          "Velocidad[m/s]": chunksb[i],
          "Cont": dlist
          })

        # Se crea una rosa de los vientos clasificandolos por su fuerza y direccion
        fig = px.bar_polar(df_chunk, r="Cont", theta="direction",
                       color="Velocidad[m/s]",  # Se usa el color en los valores de fuerza
                       color_continuous_scale=px.colors.sequential.Plasma,  # Uso de colormap
                       template="plotly_dark",
                       title=f'Rosa de los vientos. Hora: {fechas[(len(chunksa)+(len(chunksa)*i))]}',
                      start_angle= 0)
        fig.update_layout(
            images=[dict(
                source=Image.open('cdabot/Recursos/fondoRosa.png'),
                xref="paper", yref="paper",
                x=0.5, y=0.5,  # Posición del fondo
                sizex=1, sizey=1,  # Tamaño de la imagen
                xanchor="center", yanchor="middle",
                layer="below"
            )],
            annotations=[dict(
                x=0.5,
                y=-0.1,
                xref='paper',
                yref='paper',
                text=textRange,
                showarrow=False, font=dict(size=12, color="white"),
              align="center"
            )]
        )

        #footer_text = f'\nGenerado por Smability Data Analyzer, consulta: {start_time}'
        #fig.text(0.13, 0.2, footer_text, ha='left', fontsize=6, color='white', fontfamily='sans-serif')


        fig.write_image(file=f'cdabot/Rosa/graph_{i + 1}.png', format='png')
        i += 1

    tImagenes = os.listdir('cdabot/Rosa')
    listatImagenes = [os.path.join('cdabot/Rosa', f) for f in tImagenes if f.startswith('graph_') and f.endswith('.png')]
    # Ordenar la lista para asegurarse de que las imágenes están en el orden correcto
    listatImagenes.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
    # Abrir todas las imágenes
    listaImagen = [Image.open(file) for file in listatImagenes]

    # Guardar la animación como un GIF
    listaImagen[0].save(
        'cdabot/Rosa/animation.gif',
        save_all=True,
        append_images=listaImagen[1:],
        duration=500,
        loop=0
    )
    
    files = [f for f in os.listdir('cdabot/Rosa') if f.endswith('.png')]
    for file in files:
        os.remove(os.path.join('cdabot/Rosa', file))

# Funcion que permite la generacion de archivos de tipo CSV
def find_filename_pattern(directory: str, pattern: str) -> bool:
    matching_files = []
    for filename in os.listdir(directory):
        if re.match(pattern, filename):
            matching_files.append(filename)
    return matching_files

def evaluate_pm25(pm25):
    if pm25 < 12:
        return 1  # Bueno
    elif 12 <= pm25 <= 35.4:
        return 2  # Moderado
    elif 35.5 <= pm25 <= 55.4:
        return 3  # Insalubre para grupos sensibles
    else:
        return 4  # Insalubre para todos

def evaluate_pm10(pm10):
    if pm10 < 54:
        return 1  # Bueno
    elif 54 <= pm10 <= 154:
        return 2  # Moderado
    elif 155 <= pm10 <= 254:
        return 3  # Insalubre para grupos sensibles
    else:
        return 4  # Insalubre para todos

def evaluate_ozone(ozone):
    if ozone < 50:
        return 1  # Bueno
    elif 50 <= ozone <= 100:
        return 2  # Moderado
    elif 101 <= ozone <= 168:
        return 3  # Insalubre para grupos sensibles
    else:
        return 4  # Insalubre para todos

def evaluate_co(co):
    if co < 400:
        return 1  # Bueno
    elif 400 <= co <= 1000:
        return 2  # Moderado
    elif 1001 <= co <= 2000:
        return 3  # Insalubre para grupos sensibles
    else:
        return 4  # Insalubre para todos

def evaluate_temperature(temperature):
    if 20 <= temperature <= 25:
        return 1
    elif temperature > 25:
        return 2
    else:
        return 3

def evaluate_humidity(humidity):
    if 30 <= humidity <= 60:
        return 1
    else:
        return 2

def calculate_quality(total) -> str:
    if total < 11:
        return 'Resumen del día: Calidad buena 😀.'
    elif 11 <= total < 16:
        return 'Resumen del día: Calidad regular 😐.'
    else:
        return 'Resumen del día: Calidad mala 🙁.'
