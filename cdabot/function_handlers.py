import asyncio
from aiogram import types, Dispatcher
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from aiogram.filters import Filter, CommandStart

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import cdabot.menu_handlers as menu_handlers
import cdabot

from io import BytesIO

from cdabot.routers import func_router, msgEq
from cdabot.utilities import *

from secretos import sensores

# Números sensores
pm25 = 9  # P.M. 2.5
pm10 = 8  # P.M. 10
ozono = 7  # Ozono
co = 2  # CO
temperatura = 12  # Temperatura
humedad = 3 # Humedad
radiacion = 27 #Radiacion
lluvia = 23 #Lluvia

# Actividad Resumen
@func_router.message(msgEq('📚 Resumen'))
async def resumen(message: Message):
    await message.answer("🤖🧮 Calculando resumen...")
    device = "IBERO3"
    result = analyze_environment(device)
    if result == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
    else:
        await message.answer(result)

# Actividad ICA
@func_router.message(msgEq('🚦 Categoria ICA'))
async def categoria_ICA(message: Message):
    await message.answer("🤖🧮 Calculando ICA...")
    device = "IBERO3"
    dato = categoria_aire_f(device)
    if dato == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
    else:
        image = FSInputFile('images/graph.png')
        await message.answer_photo(photo=image)
        await message.answer(dato)

# Actividad Temperatura Hoy
@func_router.message(msgEq('🌇 Hoy'))
async def temperatura_hoy(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "IBERO3"
    res = generar_grafica("IBERO3", temperatura, 1)
    if res == None:
        await message.answer(f"⚙ Una disculpa, parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Temperatura más alta: {max_value} °C")

# Actividad Temperatura Semanal
@func_router.message(msgEq('🌃 Semanal'))
async def temperatura_semanal(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "METEORO1"
    res = generar_grafica("METEORO1", temperatura, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)
    # Se envía el valor máximo
    await message.answer(f"Temperatura más alta: {max_value} °C")

# Actividad Humedad Hoy
@func_router.message(msgEq('🚿 Hoy'))
async def humedad_hoy(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "METEORO1"
    res = generar_grafica("METEORO1", lluvia, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)
    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} mm/hr")

# Actividad Humedad Semanal
@func_router.message(msgEq('🌊 Semanal'))
async def humedad_semanal(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "METEORO1"
    res = generar_grafica("METEORO1", lluvia, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} mm/hr")

# Actividad PM2.5 Hoy
@func_router.message(msgEq('🕒 Hoy'))
async def pm2_5_hoy(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "IBERO3"
    res = generar_grafica("IBERO3", pm25, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ug/m3")

# Actividad PM25 Semanal
@func_router.message(msgEq('📅 Semanal'))
async def pm2_5_semanal(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "IBERO3"
    res = generar_grafica("IBERO3", pm25, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ug/m3")

# Actividad PM10 Hoy
@func_router.message(msgEq('😤 Hoy'))
async def pm10_hoy(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "IBERO3"
    res = generar_grafica("IBERO3", pm10, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ug/m3")

# Actividad PM10 Semanal
@func_router.message(msgEq('🧹 Semanal'))
async def pm10_semanal(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "IBERO3"
    res = generar_grafica("IBERO3", pm10, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ug/m3")

# Actividad O3 Hoy
@func_router.message(msgEq('🕕 Hoy'))
async def o3_hoy(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "IBERO3"
    res = generar_grafica("IBERO3", ozono, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ppb")

# Actividad O3 Semanal
@func_router.message(msgEq('🕡 Semanal'))
async def o3_semanal(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "IBERO3"
    res = generar_grafica("IBERO3", ozono, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ppb")

# Actividad CO Hoy
@func_router.message(msgEq('🛵 Hoy'))
async def co_hoy(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "IBERO3"
    res = generar_grafica("IBERO3", co, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ppb")

# Actividad CO Semanal
@func_router.message(msgEq('✈️ Semanal'))
async def co_semanal(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "IBERO3"
    res = generar_grafica("IBERO3", co, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ppb")

# Actividad Radiacion Hoy
@func_router.message(msgEq('☀ Hoy'))
async def co_hoy(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "METEORO1"
    res = generar_grafica("METEORO1", radiacion, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} W/m2")

# Actividad Radiacion Semanal
@func_router.message(msgEq('😎 Semanal'))
async def co_semanal(message: Message):
    await message.answer("🤖🧮 Generando gráfica...")
    # Función para graficar
    device = "METEORO1"
    res = generar_grafica(device, radiacion, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} W/m2")

# Actividad Rosa Hoy
@func_router.message(msgEq('🪁 Hoy'))
async def co_semanal(message: Message):
    await message.answer("🤖🧮 Generando gif...")
    # Función para graficar
    device = "METEORO1"
    create_windrose_plot(device, 1)
    video1 = FSInputFile('cdabot/Rosa/animation.gif')
    await message.answer_animation(video1)

# Actividad Rosa Hoy
@func_router.message(msgEq('🪂 Semanal'))
async def co_semanal(message: Message):
    await message.answer("🤖🧮 Generando gif...")
    # Función para graficar
    device = "METEORO1"
    create_windrose_plot(device, 7)
    video1 = FSInputFile('cdabot/Rosa/animation.gif')
    await message.answer_animation(video1)

# Generar CSV
@func_router.message(msgEq('📥 Descargar CSV'))
async def gen_csv(message: Message):
    # Función para enviar descargable
    if len(os.listdir('files')) == 0:
        await message.answer("🤖 No ha generado ninguna solicitud. Elija algunas de las opciones que se encuentran en el menú.")
    else:    
        await message.answer("Enviando último reporte...")
        reporte = FSInputFile("files/latest.csv")
        await message.answer_document(document=reporte)

# Definición de submenu "¿Quienes somos?"
@func_router.message(msgEq("❓ ¿Quienes somos?"))
async def send_musicc(message: types.Message):
    await message.answer('¿Qué deseas conocer?')

# Definición de submenu "Dudas, calidad del aire"
@func_router.message(msgEq("🌐 Estacion Calidad del Aire"))
async def send_musicc(message: types.Message):
    await message.answer('¿Qué deseas conocer?')

# Definición de submenu "Dudas, estacion meteorológica"
@func_router.message(msgEq("📡 Estacion Meteorológica"))
async def send_musicc(message: types.Message):
    await message.answer('La estación de calidad del aire es un lugar equipado con uno o más instrumentos diseñados para medir de forma continua la concentración de contaminantes en el aire ambiente. Estas estaciones evalúan la calidad del aire en un área específica. Los contaminantes que se miden incluyen PM10, PM2,5, O3, CO')
    #await message.

def setup(dp: Dispatcher):
    dp.include_router(func_router)
