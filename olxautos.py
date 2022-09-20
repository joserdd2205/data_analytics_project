import csv
from scrapy.item import Field
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random

# Opciones del navegador
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opts)
driver.get("https://www.olxautos.com.mx/autos_c84")

# clickear botones un numero especifico de veces
for i in range(10):
    try:
        boton = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id= "btnLoadMore"]'))
        )
        boton.click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@data-aut-id="itemBox"]//span[@class="_1OBW-"]'))
        )
    except:
        break

links_autos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]//a')
links_paginas = []
# colocar todos los links en una lista
for href in links_autos:
    links_paginas.append(href.get_attribute('href'))

headercsv = ["marca", "modelo", "año", "precio", "mensualidad", "meses", "enganche", "combustible",
             "kilometraje", "transmision", "numero de puertas", "ubicacion"]
lista_de_autos = [headercsv]
fallos = 0
# acceder a cada link para obtener info
for link in links_paginas:
    while True:
        try:

            # Entrar al link
            driver.get(link)
            # Esperar de acuerdo a una distribucion uniforme entre 3 y 9 segundos
            time.sleep(random.uniform(3, 9))
            WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@data-aut-id="itemTitle"]'))
            )
            # Obtencion y limpieza de datos
            modelo_año = driver.find_element(By.XPATH, '//div[@data-aut-id="itemTitle"]').text
            marca, modelo, año = modelo_año.split(" ", 2)
            año = año.replace("(", "").replace(")", "")
            print(marca)
            print(modelo)
            print(año)
            precio = driver.find_element(By.XPATH, '//div[@data-aut-id="itemPrice"]').text
            precio = precio.replace("$ ", "").replace(",", "")
            print(precio)
            mensualidad = driver.find_element(By.XPATH, "//div[@data-aut-id='itemEmi']").text
            mensualidad, meses = mensualidad.replace("Mensualidad $ ", "").replace(",", "").split(" X ")
            print(mensualidad)
            print(meses)
            enganche = driver.find_element(By.XPATH,
                                           "//div[@data-aut-id='itemHitchAmount']//span[@class='_21VvJ']").text
            enganche = enganche.replace("$ ", "").replace(",", "")
            print(enganche)
            combkilotrans = driver.find_element(By.XPATH, "//div[@class='aOxkz']").text
            combustible, kilometraje, transmision = combkilotrans.split("\n")
            kilometraje = kilometraje.replace(" KM", "")
            print(combustible)
            print(kilometraje)
            print(transmision)
            componentes = driver.find_element(By.XPATH, "//div[@class='_3tLee']").text
            puertas = componentes.find(" pts")
            npuertas = componentes[puertas - 1:puertas]
            print(npuertas)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_1idEV"]//div[@class="_1gasz"]'))
            )
            varios = driver.find_elements(By.XPATH, '//div[@class="_1idEV"]//div[@class="_1gasz"]')
            ubicacion = varios[1].text
            print(ubicacion)
            # Agregar datos obtenidos a lista
            lista_de_autos.append(
                [marca, modelo, año, precio, mensualidad, meses, enganche, combustible, kilometraje, transmision,
                 npuertas,
                 ubicacion])
            driver.back()

        except:
            fallos += 1
            if fallos > 3:
                fallos = 0
                break
            print("fallo")
            continue
        break

    # escribir datos de la lista en csv
with open("/Users/jose/PycharmProjects/selenium/autos_seminuevos.csv", 'w', encoding="UTF-8") as f:
    writer = csv.writer(f)
    writer.writerows(lista_de_autos)
print(fallos)
