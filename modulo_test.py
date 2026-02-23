from modulos.datos import (
    cargar_datos, guardar_datos,
    HERRAMIENTAS_FILE,REPARACIONES_FILE)

def registrar_reparacion():
    herramientas = cargar_datos(HERRAMIENTAS_FILE)
    reparaciones = cargar_datos(REPARACIONES_FILE)


    if not herramientas:
        print("No hay herramientas registradas.")
        return
    
    if not reparaciones:
        print("No hay reparaciones registradas.")
        return
    
    print("====== INVENTARIO DE HERRAMIENTAS =======")
    print(f"{'ID':<10} {'Nombre':<20} {'Categoria':<15} {'Cantidad disponible':<20} {'Estado':<20} ")
    print("-" * 90)

    for id_herramienta, info in herramientas.items():
        print(f"{id_herramienta:<10} {info['nombre']:<20} {info['categoria']:<15} {info['cantidad']:<20} {info['estado']:<20} ")

    id_herramienta = input("\n\nIngrese ID de la herramienta a actualizar: ")

    if id_herramienta not in herramientas:
        print("Herramienta no encontrada.")
        return
    else:
        herramientas[id_herramienta]["estado"] = "en reparacion"

    fecha_inicio_reparacion = input("Ingrese la fecha de inicio de reparacion YYYY-MM-DD: ").strip()
    if fecha_inicio_reparacion == "":
        print("Campo vacìo. Digite fecha de reparacion")
        return
    fecha_estimada_fin = input("Ingrese la fecha estimada de fin de reparacion YYYY-MM-DD: ").strip()
    if fecha_estimada_fin == "":
        print("Campo vacìo. Digite fecha de reparacion")
        return
    observaciones = input("Observaciones: ")

    reparaciones[id_herramienta] = {
        "nombre": herramientas[id_herramienta]['nombre'],
        "fecha_inicio": fecha_inicio_reparacion,
        "fecha_estimada_fin": fecha_estimada_fin,
        "observaciones": observaciones
        }

    print("\n HERRAMIENTA REGISTRADA EN REPARACION. ")
    
    print("\n\n")
    print("=== HERRAMIENTAS EN REPARACION ===\n")
    print(f"{'ID':<10} {'Nombre':<20} {'Inicio':<20} {'Fin est.':<20} {'Observaciones':<15}")
    print("-"*80,"\n")
    
    for id, info in reparaciones.items():
        print(f"{id:<10} {info['nombre']:<20} {info['fecha_inicio']:<20} {info['fecha_estimada_fin']:<20} {info['observaciones']:<15}")
    
    guardar_datos(reparaciones, REPARACIONES_FILE)
    guardar_datos(herramientas, HERRAMIENTAS_FILE)

registrar_reparacion()