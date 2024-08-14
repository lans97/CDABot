from aiogram import types, Dispatcher
from aiogram.types import Message
from aiogram.filters import Filter, CommandStart
from cdabot.menus import *
from cdabot.routers import menu_router, msgEq

import os

# UI Handlers

# Inicio de la interfaz principal
@menu_router.message(CommandStart())
async def send_main_menu(message: types.Message):
    await message.answer('🐺 ¡Hola! Soy tu asistente meteorológico de la Universidad Iberoamericana. Mi objetivo es brindarte información detallada sobre el clima y el tiempo en nuestro campus y sus alrededores. Desde pronósticos diarios hasta datos climáticos históricos, estoy aquí para mantenerte informado y ayudarte a planificar tu día de manera eficiente. ¡Bienvenido y disfruta de la precisión meteorológica a tu alcance!')
    await message.answer('Este es el menú principal, selecciona con un boton aquello que deseas conocer:', reply_markup=menu_principal_inter.as_markup())

# Definición de submenu "Calidad del aire"
@menu_router.message(msgEq("🩺 Calidad del aire"))
async def send_submenu_r(message: types.Message):
    await message.answer('¿Qué deseas conocer? 🪁.', reply_markup=submenu_calidad_inter.as_markup())

# Definición de submenu "Estacion Mete"
@menu_router.message(msgEq("🌎 Estación meteorológica"))
async def send_submenu_o(message: types.Message):
    if os.path.isfile("images/latest.png"):
        os.remove("images/latest.png")
    if os.path.isfile("files/latest.csv"):
        os.remove("files/latest.csv")
    await message.answer('¿Qué dato es de tu interés? 🌎', reply_markup=submenu_estacion_inter.as_markup())

# Definición de submenu "Contaminantes"
@menu_router.message(msgEq("😷 Contaminantes"))
async def send_submenu_o(message: types.Message):
    if os.path.isfile("images/latest.png"):
        os.remove("images/latest.png")
    if os.path.isfile("files/latest.csv"):
        os.remove("files/latest.csv")
    await message.answer('¿Qué dato es de tu interés? ', reply_markup=submenu_conta_inter.as_markup())

# Definición de submenu "Temperatura"
@menu_router.message(msgEq("🌡 Temperatura"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar? 🌡', reply_markup=submenu_tempe_inter.as_markup())

# Definición de submenu "Humedad"
@menu_router.message(msgEq("💧 Lluvia"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_lluvia_inter.as_markup())

# Definición de submenu "PM25"
@menu_router.message(msgEq("😤 PM 2.5"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_pm25_inter.as_markup())

# Definición de submenu "PM10"
@menu_router.message(msgEq("🧹 PM 10"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_pm10_inter.as_markup())

# Definición de submenu "Ozono"
@menu_router.message(msgEq("🛡️ Ozono"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_o3_inter.as_markup())

# Definición de submenu "CO"
@menu_router.message(msgEq("🧯 Monóxido de carbono"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_co_inter.as_markup())
    
# Definición de submenu "Radiación"
@menu_router.message(msgEq("🌅 Radiación"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_rad_inter.as_markup())

# Definición de submenu "Viento"
@menu_router.message(msgEq("🌫 Viento"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_viento_inter.as_markup())

# Definición de submenu "Resumen"
@menu_router.message(msgEq("🏠 Menú inicial"))
async def send_hogar(message: types.Message):
    if os.path.isfile("images/latest.png"):
        os.remove("images/latest.png")
    if os.path.isfile("files/latest.csv"):
        os.remove("files/latest.csv")
    await message.answer('¿Qué te apetece conocer? 🔮', reply_markup=menu_principal_inter.as_markup())

# Definición de submenu "Musica"
@menu_router.message(msgEq("🎧 Ayuda"))
async def send_musicc(message: types.Message):
    await message.answer('¿Qué deseas conocer?',reply_markup=submenu_music_inter.as_markup())

def setup(dp: Dispatcher):
    dp.include_router(menu_router)
