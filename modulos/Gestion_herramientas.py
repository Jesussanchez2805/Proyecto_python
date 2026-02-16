
from modulos.datos import cargar_datos, guardar_datos, HERRAMIENTAS_FILE, registrar_log
from modulos.Validacion_roles import validar_permiso

def crear_herramienta():

    if not validar_permiso(["administrador"]):
        return
    
    datos = cargar_datos(HERRAMIENTAS_FILE)

    id_herramienta = input("Ingrese ID de la herramienta: ")

    # Validamos que no exista el ID
    if id_herramienta in datos:
        print("Ya existe una herramienta con ese ID.")
        return

    nombre = input("Nombre: ")
    categoria = input("Categoría: ")
    cantidad = int(input("Cantidad disponible: "))
    estado = input("Estado (activa, en reparación, fuera de servicio): ")
    valor = float(input("Valor estimado: "))

    # se crea diccionario de herramientas
    datos[id_herramienta] = {
        "nombre": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "estado": estado,
        "valor_estimado": valor
    }

    guardar_datos(datos, HERRAMIENTAS_FILE)
    registrar_log("INFO", f"Herramienta registrada correctamente: {id_herramienta}")
    print(" La herramienta se ha registrado correctamente.")



def listar_herramientas():

    datos = cargar_datos(HERRAMIENTAS_FILE)

    if not datos:
        print("No hay herramientas registradas.")
        return
    print(f"{'ID':<10} {'Nombre':<20} {'Categoria':<15} {'Cantidad disponible':<20} {'Estado':<20} {'Valor estimado':<15}")
    print("-" * 90)

    for id_herramienta, info in datos.items():
        print(f"{id_herramienta:<10} {info['nombre']:<20} {info['categoria']:<15} {info['cantidad']:<20} {info['estado']:<20} ${info['valor_estimado']:<15}")


def buscar_herramienta():

    datos = cargar_datos(HERRAMIENTAS_FILE)

    id_nombre = input("Ingrese nombre a buscar: ").strip().lower()

    for id_herramienta, info in datos.items():
        if id_nombre in id_herramienta or id_nombre == info["nombre"]:
            print("Herramienta encontrada:")
            print(f"{id_herramienta:<10} {info['nombre']:<20} {info['categoria']:<15} {info['cantidad']:<20} {info['estado']:<20} ${info['valor_estimado']:<15}")
            return
    else:
        
        print("No existe una herramienta con ese nombre.")


def actualizar_herramienta():

    datos = cargar_datos(HERRAMIENTAS_FILE)

    id_herramienta = input("Ingrese ID de la herramienta a actualizar: ")

    if id_herramienta not in datos:
        print("Herramienta no encontrada.")
        return

    print("Para no modificar el valor existe se deja espacio vacio.")

    nombre = input("Nuevo nombre: ")
    categoria = input("Nueva categoría: ")
    cantidad = input("Nueva cantidad disponible: ")
    estado = input("Nuevo estado: ")
    valor = input("Nuevo valor estimado: ")

    if nombre:
        datos[id_herramienta]["nombre"] = nombre
    if categoria:
        datos[id_herramienta]["categoria"] = categoria
    if cantidad:
        datos[id_herramienta]["cantidad"] = int(cantidad)
    if estado:
        datos[id_herramienta]["estado"] = estado
    if valor:
        datos[id_herramienta]["valor_estimado"] = float(valor)

    guardar_datos(datos, HERRAMIENTAS_FILE)
    print("Herramienta actualizada correctamente.")
    registrar_log("INFO", f"Herramienta actualizada correctamente: {id_herramienta}")


def eliminar_o_inactivar():

    if not validar_permiso(["administrador"]):
        return

    datos = cargar_datos(HERRAMIENTAS_FILE)

    id_herramienta = input("Ingrese ID de la herramienta: ")

    if id_herramienta not in datos:
        print("Herramienta no encontrada.")
        return

    opcion = input("¿Desea eliminar (E) o inactivar (I)? ").lower()

    if opcion == "e":
        del datos[id_herramienta]
        print("Herramienta eliminada.")
    elif opcion == "i":
        datos[id_herramienta]["estado"] = "fuera de servicio"
        print("Herramienta inactivada.")
    else:
        print("Opción inválida.")
        return

    guardar_datos(datos, HERRAMIENTAS_FILE)
    registrar_log("INFO", f"Herramienta eliminada o inactivada correctamente: {id_herramienta}")



def menu_herramientas():

    while True:
        print("""
===== SISTEMA DE HERRAMIENTAS =====
1. Crear herramienta
2. Listar herramientas
3. Buscar herramienta
4. Actualizar herramienta
5. Eliminar o inactivar herramienta
6. Salir
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_herramienta()
        elif opcion == "2":
            listar_herramientas()
        elif opcion == "3":
            buscar_herramienta()
        elif opcion == "4":
            actualizar_herramienta()
        elif opcion == "5":
            eliminar_o_inactivar()
        elif opcion == "6":
            print(" Saliendo del menu de herramientas...")
            break
        else:
            print(" Opción inválida.")