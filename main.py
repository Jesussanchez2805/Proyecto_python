"""
PUNTO DE ENTRADA DEL SISTEMA
Sistema Junta Comunal - Gestión de Herramientas
"""
from modulos.Gestion_usuarios import menu_usuarios
from modulos import Validacion_roles
from modulos.Gestion_herramientas import menu_herramientas
from modulos.Gestion_prestamos import menu_prestamos
from modulos.datos import registrar_log
from modulos.Consultas_Reportes import menu_reportes

def menu_principal():

    Validacion_roles.verificar_primer_inicio()

    if not Validacion_roles.iniciar_sesion():
        return

    registrar_log("INFO", f"Usuario inició sesión - ID: {Validacion_roles.usuario_actual['id']}")

    while True:

        print(f"""
===============================
SISTEMA COMUNITARIO DE PRESTAMOS DE HERRAMIENTAS
Usuario: {Validacion_roles.usuario_actual['nombre']} ({Validacion_roles.usuario_actual['tipo']})
===============================

1. Gestión de Herramientas
2. Gestión de Usuarios
3. Gestión de Préstamos
4. Consultas y Reportes
5. Cerrar sesión
6. Salir del sistema
""")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_herramientas()
        elif opcion == "2":
            menu_usuarios()
        elif opcion == "3":
            menu_prestamos()
        elif opcion == "4":
            menu_reportes()
        elif opcion == "5":
            registrar_log("INFORMACION", f"Cierre de sesión - ID: {Validacion_roles.usuario_actual['id']}")
            break
        elif opcion == "6":
            registrar_log("INFORMACION", "Sistema finalizado manualmente")
            print("Saliendo del sistema...")
            exit()
        else:
            print(" Opción inválida.")

if __name__ == "__main__":
    menu_principal()