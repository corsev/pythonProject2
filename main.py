import mysql.connector as conector
import bs4
from bs4 import BeautifulSoup
import requests
import openpyxl


def cargar_todas_paginas():
    soups = []
    num_pag = 0
    for a in range(71):
        url_todas = "https://www.ufcespanol.com/athletes/all?filters%5B0%5D=status%3A23&gender=All&search=&page=" + str(
            num_pag) + '"'
        pagina = requests.get(url_todas)
        soup = BeautifulSoup(pagina.text, "html.parser")
        soups.append(soup)
        num_pag += 1

    return soups


def cargar_datos():
    soups = cargar_todas_paginas()
    lista_datos_luchadores = list()
    lista_cara = list()
    lista_nombre = list()
    lista_apodo = list()
    lista_peso = list()
    lista_ratio = list()
    for soup in soups:

        datos_obtener_frontal = soup.findAll("div", {"class": "c-listing-athlete-flipcard__front"})

        # Creamos la plantilla del diccionario con los datos del luchador a buscar

        luchador = {
            "cara": "",
            "nombre": "",
            "apodo": "",
            "peso": "",
            "ratio": "",
            # "cuerpo" : "",
        }

        # Buscamos los elementos de los luchadores de la parte delantera y lo guardamos en el diccionario

        for elemento in datos_obtener_frontal:
            cara = "\"Sin imagen\""
            if elemento.find("div", {"class": "layout__region layout__region--content"}) is not None:
                cara = elemento.find("div", {"class": "layout__region layout__region--content"}).find("img").attrs[
                    "src"]

            nombre = str(elemento.find("div", {"class": "c-listing-athlete__text"}).find("span",
                                                                                         "c-listing-athlete__name").text.replace(
                '\n', ' ').lstrip().rstrip())
            apodo = "\"Sin apodo\""
            if elemento.find("div", {
                "class": "field field--name-nickname field--type-string field--label-hidden"}) is not None:
                apodo = elemento.find("div", {
                    "class": "field field--name-nickname field--type-string field--label-hidden"}).find("div", {
                    "class": "field__item"}).text
            peso = elemento.find("div", {
                "class": "field field--name-stats-weight-class field--type-entity-reference field--label-hidden field__items"}).find(
                "div", {"class": "field__item"}).text
            ratio = elemento.find("div", {"class": "c-listing-athlete__text"}).find("span", {
                "class": "c-listing-athlete__record"}).text

            # Guardamos los datos extraidos y los metemos en diccionarios y listas

            luchadores_datos = luchador.copy()
            luchadores_datos["cara"] = cara
            luchadores_datos["nombre"] = nombre
            luchadores_datos["apodo"] = apodo
            luchadores_datos["peso"] = peso
            luchadores_datos["ratio"] = ratio
            lista_cara.append(cara)
            lista_nombre.append(nombre)
            lista_apodo.append(apodo)
            lista_peso.append(peso)
            lista_ratio.append(ratio)

            # Guardamos el diccionario en una lista para guardar a todos los luchadores
            lista_datos_luchadores.append(luchadores_datos)

        # Creamos un excel con todos los datos de los jugadores

        wb = openpyxl.Workbook()
        ruta = 'Luchadores UFC.xlsx'
        hoja = wb.active
        hoja.title = "Datos Luchadores"
        hoja.append(('Nombre', 'Apodo', 'Peso', 'Ratio', 'Cara'))

        fila = 2

        col_cara = 5
        col_nombre = 1
        col_apodo = 2
        col_peso = 3
        col_ratio = 4

        for caras, nombres, apodos, pesos, ratios in zip(lista_cara, lista_nombre, lista_apodo, lista_peso,
                                                         lista_ratio):
            hoja.cell(column=col_cara, row=fila, value=caras)
            hoja.cell(column=col_nombre, row=fila, value=nombres)
            hoja.cell(column=col_apodo, row=fila, value=apodos)
            hoja.cell(column=col_peso, row=fila, value=pesos)
            hoja.cell(column=col_ratio, row=fila, value=ratios)
            fila += 1

            # wb.save(filename=ruta)

    return lista_datos_luchadores


def conectar_bbdd():
    conexion = conector.connect(user='root',
                                password='1234',
                                host='localhost',
                                database='luchadores_ufc',
                                autocommit=True)

    return conexion


def insertar_datos():
    conexion = conectar_bbdd()
    cursor = conexion.cursor()
    datos_luchadores = cargar_datos()
    ql_insertar_datos = "INSERT INTO luchadores (nombre,apodo,peso,ratio,cara) VALUES (%s, %s, %s, %s, %s)"
    for luchador in datos_luchadores:
        values = [luchador["nombre"], luchador["apodo"], luchador["peso"], luchador["ratio"], luchador["cara"]]
        cursor.execute(ql_insertar_datos,values)
    print("Se han metido todos los datos")
    cursor.close()

def eliminar_datos():
    conexion = conectar_bbdd()
    cursor = conexion.cursor()
    eliminar = "DELETE FROM luchadores"
    cursor.execute(eliminar)
    print("Se han eliminado todos los datos")
    cursor.close()

def consultar_datos():
    lista_datos_luchadores = list()
    conexion = conectar_bbdd()
    cursor = conexion.cursor()
    consultar_todo = "SELECT * FROM luchadores"
    cursor.execute(consultar_todo)
    datos = cursor.fetchall()
    for ids, nombres, apodos, pesos, ratios, caras in datos:
        luchador = {"id": ids, "cara": caras, "nombre": nombres, "apodo": apodos, "peso": pesos, "ratio": ratios}
        lista_datos_luchadores.append(luchador)

    print("Se han recuperado todos los datos")
    cursor.close()

    return lista_datos_luchadores








