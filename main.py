import mysql.connector as conector
import bs4
from bs4 import BeautifulSoup
import requests
import openpyxl
from tkinter import *
from tkinter import ttk


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
        cursor.execute(ql_insertar_datos, values)
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


def ventana_mostrar():
    ventana2 = Tk()
    menu_ventana = Menu(ventana2)
    ventana2.title("Ventana para mostrar los datos")
    ventana2.config(menu=menu_ventana)
    ventana2.geometry("800x400")
    ventana2.resizable(True, True)
    luchadores = consultar_datos()
    tv = ttk.Treeview(ventana2)

    tv['columns'] = ("id", "nombre", "apodo", "peso", "ratio", "cara")

    tv.column("#0", width=0, anchor=CENTER)
    tv.column("id", width=40, anchor=CENTER)
    tv.column("nombre", width=100, anchor=CENTER)
    tv.column("apodo", width=100, anchor=CENTER)
    tv.column("peso", width=100, anchor=CENTER)
    tv.column("ratio", width=100, anchor=CENTER)
    tv.column("cara", width=100, anchor=CENTER)

    tv.heading("#0", text="", anchor=CENTER)
    tv.heading("id", text="Id", anchor=CENTER)
    tv.heading("nombre", text="Nombre", anchor=CENTER)
    tv.heading("apodo", text="Apodo", anchor=CENTER)
    tv.heading("peso", text="Peso", anchor=CENTER)
    tv.heading("ratio", text="Ratio", anchor=CENTER)
    tv.heading("cara", text="Cara", anchor=CENTER)

    tv.pack()
    ventana2.mainloop()





def aplicacion_luchadores():
    root = Tk()
    menu_principal = Menu(root)
    root.title("Luchadores UFC")
    root.config(menu=menu_principal)
    root.geometry("800x0")
    root.resizable(True, True)

    barra_menu = Menu(menu_principal, tearoff=0)
    barra_menu1 = Menu(menu_principal, tearoff=0)
    barra_menu2 = Menu(menu_principal, tearoff=0)

    menu_principal.add_cascade(label="Cargar", menu=barra_menu)
    barra_menu.add_command(label="Luchadores", command=lambda: insertar_datos())

    menu_principal.add_cascade(label="Eliminar", menu=barra_menu1)
    barra_menu1.add_command(label="Luchadores", command=lambda: eliminar_datos())

    menu_principal.add_cascade(label="Mostrar", menu=barra_menu2)
    barra_menu2.add_command(label="Luchadores", command=lambda: ventana_mostrar())

    root.mainloop()



aplicacion_luchadores()