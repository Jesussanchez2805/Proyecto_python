from modulos.datos import cargar_datos, guardar_datos, PRESTAMOS_FILE, HERRAMIENTAS_FILE, USUARIOS_FILE

def registrar_prestamo():

    prestamos = cargar_datos(PRESTAMOS_FILE)
    usuarios = cargar_datos(USUARIOS_FILE)
    herramientas = cargar_datos(HERRAMIENTAS_FILE)

    id_prestamo = input("Ingrese ID del préstamo: ")

    if id_prestamo in prestamos:
        print("Ya existe un préstamo con ese ID.")
        return

    id_usuario = input("ID del usuario: ")
    if id_usuario not in usuarios:
        print(" Usuario no existe.")
        return

    id_herramienta = input("ID de la herramienta: ")
    if id_herramienta not in herramientas:
        print(" Herramienta no existe.")
        return

    cantidad = int(input("Cantidad a prestar: "))

    herramienta = herramientas[id_herramienta]

    if herramienta["estado"] != "activa":
        print("La herramienta no está activa.")
        return

    if herramienta["cantidad"] < cantidad:
        print("No hay suficiente cantidad disponible.")
        return

    fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
    fecha_devolucion = input("Fecha estimada devolución (YYYY-MM-DD): ")
    observaciones = input("Observaciones: ")

    herramienta["cantidad"] -= cantidad

    guardar_datos(herramientas, HERRAMIENTAS_FILE)

    prestamos[id_prestamo] = {
        "usuario": id_usuario,
        "herramienta": id_herramienta,
        "cantidad": cantidad,
        "fecha_inicio": fecha_inicio,
        "fecha_estimada_devolucion": fecha_devolucion,
        "estado": "activo",
        "observaciones": observaciones
    }

    guardar_datos(prestamos, PRESTAMOS_FILE)
    print(" Préstamo registrado correctamente.")


def listar_prestamos():

    prestamos = cargar_datos(PRESTAMOS_FILE)

    if not prestamos:
        print("No hay préstamos registrados.")
        return
    
    print(f"{'ID':<10} {'Usuario':<20} {'Herramienta':<20} {'Cantidad':<15} {'Fecha inicio':<25} {'Fecha devolucion':<20} {'Estado':<15} {'Observaciones':<30}")

    for id_prestamo, info in prestamos.items():
        print(f"{id_prestamo:<10} {info['usuario']:<20} {info['herramienta']:<20} {info['cantidad']:<15} {info['fecha_inicio']:<25} {info['fecha_estimada_devolucion']:<20} {info['estado']:<15} {info['observaciones']:<30}")

def registrar_devolucion():

    prestamos = cargar_datos(PRESTAMOS_FILE)
    herramientas = cargar_datos(HERRAMIENTAS_FILE)

    id_prestamo = input("Ingrese ID del préstamo: ")

    if id_prestamo not in prestamos:
        print(" Préstamo no encontrado.")
        return

    prestamo = prestamos[id_prestamo]

    if prestamo["estado"] == "devuelto":
        print("Este préstamo ya fue devuelto.")
        return

    id_herramienta = prestamo["herramienta"]
    cantidad = prestamo["cantidad"]

    if id_herramienta not in herramientas:
        print(" La herramienta asociada ya no existe en el sistema.")
        return

    herramientas[id_herramienta]["cantidad"] += cantidad

    prestamo["estado"] = "devuelto"

    guardar_datos(herramientas, HERRAMIENTAS_FILE)
    guardar_datos(prestamos, PRESTAMOS_FILE)

    print(" Devolución registrada correctamente.")


def menu_prestamos():

    while True:
        print("""
===== MENÚ GESTIÓN DE PRÉSTAMOS =====
1. Registrar préstamo
2. Listar préstamos
3. Registrar devolución
4. Volver al menú principal
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_prestamo()
        elif opcion == "2":
            listar_prestamos()
        elif opcion == "3":
            registrar_devolucion()
        elif opcion == "4":
            break
        else:
            print(" Opción inválida.")