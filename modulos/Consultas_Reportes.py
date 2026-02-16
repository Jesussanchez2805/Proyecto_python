
from modulos.datos import cargar_datos, HERRAMIENTAS_FILE, PRESTAMOS_FILE
from datetime import datetime



def herramientas_stock_bajo():

    herramientas = cargar_datos(HERRAMIENTAS_FILE)

    print("\n=== HERRAMIENTAS CON STOCK BAJO ===")
    print(f" {"ID":<20} {"Nombre":<20} {"Cantidad disponible":<20} ")

    for id_herramienta, info in herramientas.items():
        if info["cantidad"] < 3:
            print(f"ID: {id_herramienta:<20} Nombre: {info['nombre']:<20} Cantidad disponible: {info['cantidad']:<20}")

def prestamos_activos_y_vencidos():

    prestamos = cargar_datos(PRESTAMOS_FILE)

    hoy = datetime.now().date()

    print("\n=== PRESTAMOS ACTIVOS Y VENCIDOS ===")
    print(f" {"ID":<20} {"Usuario":<20} {"Herramienta":<20} {"Estado":<20} {"Fecha estimada devolución":<20} ")

    for id_prestamo, info in prestamos.items():
        if info["estado"] == "activo":

            fecha_estimada = datetime.strptime(
                info["fecha_estimada_devolucion"],
                "%Y-%m-%d"
            ).date()

            if fecha_estimada < hoy:
                estado = "VENCIDO"
            else:
                estado = "ACTIVO"

            print(f"ID: {id_prestamo:<20} {info['usuario']:<20} {info['herramienta']:<20} estado: {estado:<20} {info['fecha_estimada_devolucion']:<20} ")

def historial_usuario():

    prestamos = cargar_datos(PRESTAMOS_FILE)

    id_usuario = input("Ingrese ID del usuario: ")

    print("\n=== HISTORIAL DE PRÉSTAMOS ===")
    print(f" {"ID Prestamo":<20} {"Herramienta":<20} {"Cantidad":<20} {"Estado":<20} {"Fecha inicio":<20} ")
    encontrado = False
    for id_prestamo, info in prestamos.items():
        if info["usuario"] == id_usuario:
            encontrado = True
        print(f"{id_prestamo:<20} {info['herramienta']:<20} {info['cantidad']:<20} {info['estado']:<20} {info['fecha_inicio']:<20} ")

    if not encontrado:
        print("No hay préstamos registrados para este usuario.")



def herramientas_mas_solicitadas():

    prestamos = cargar_datos(PRESTAMOS_FILE)

    conteo = {}

    for info in prestamos.values():
        id_herramienta= info["herramienta"]
        cantidad = info["cantidad"]

        if id_herramienta in conteo:
            conteo[id_herramienta] += cantidad
        else:
            conteo[id_herramienta] = cantidad

    ranking = sorted(conteo.items(), key=lambda x: x[1], reverse=True)

    print("\n=== HERRAMIENTAS MAS SOLICITADAS ===")

    for id_herramienta, total in ranking:
        print(f"Herramienta {id_herramienta} - Total solicitado: {total}")


def usuarios_mas_activos():

    prestamos = cargar_datos(PRESTAMOS_FILE)

    conteo = {}

    for info in prestamos.values():
        id_usuario = info["usuario"]
        cantidad = info["cantidad"]

        if id_usuario in conteo:
            conteo[id_usuario] += cantidad
        else:
            conteo[id_usuario] = cantidad

    ranking = sorted(conteo.items(), key=lambda x: x[1], reverse=True)

    print("\n=== USUARIOS QUE MÁS SOLICITAN HERRAMIENTAS ===")

    for id_usuario, total in ranking:
        print(f"Usuario {id_usuario} - Total solicitado: {total}")


def menu_reportes():

    while True:
        print("""
===== MENÚ CONSULTAS Y REPORTES =====
1. Herramientas con stock bajo
2. Préstamos activos y vencidos
3. Historial de préstamos por usuario
4. Herramientas más solicitadas
5. Usuarios más activos
6. Volver al menú principal
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            herramientas_stock_bajo()
        elif opcion == "2":
            prestamos_activos_y_vencidos()
        elif opcion == "3":
            historial_usuario()
        elif opcion == "4":
            herramientas_mas_solicitadas()
        elif opcion == "5":
            usuarios_mas_activos()
        elif opcion == "6":
            break
        else:
            print(" Opción inválida.")