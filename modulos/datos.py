"""
Este módulo se encarga de gestionar los datos json en
el disco
"""


HERRAMIENTAS_FILE = "herramientas.json"
USUARIOS_FILE     = "usuarios.json"
PRESTAMOS_FILE    = "prestamos.json"
SOLICITUDES_FILE  = "solicitudes.json"          # ← NUEVO
LOGS_FILE         = "logs.txt"
ROLES_PERMITIDOS  = ["administrador", "residente"]

import json
from datetime import datetime

def cargar_datos(nom_archivo):
    try:
        with open(nom_archivo, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}
    
def guardar_datos(datos, nom_archivo):
    try:
        with open(nom_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
    except Exception:
        datos = {}


def registrar_log(tipo, mensaje):

    # Obtenemos fecha y hora actual
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linea = f"[{fecha_hora}] {tipo} - {mensaje}\n"

    with open(LOGS_FILE, "a") as archivo:
        archivo.write(linea)
