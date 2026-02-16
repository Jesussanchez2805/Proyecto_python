
from modulos.datos import cargar_datos, guardar_datos, USUARIOS_FILE
from modulos.Validacion_roles import validar_permiso

def crear_usuario():

    if not validar_permiso(["administrador"]):
        return
    
    usuarios = cargar_datos(USUARIOS_FILE)

    id_usuario = input("Ingrese ID del usuario: ")

    if id_usuario in usuarios:
        print(" Ya existe un usuario con ese ID.")
        return

    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    telefono = input("Teléfono: ")
    direccion = input("Dirección: ")
    tipo = input("Tipo de usuario (residente, administrador): ")

    usuarios[id_usuario] = {
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "direccion": direccion,
        "tipo_usuario": tipo
    }

    guardar_datos(usuarios, USUARIOS_FILE)
    print(" Usuario registrado correctamente.")


def listar_usuarios():

    usuarios = cargar_datos(USUARIOS_FILE  )

    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print(f"{'ID':<10} {'Nombre':<20} {'Apellidos':<20} {'Teléfono':<15} {'Dirección':<25} {'Tipo de usuario':<15}")
    print("-" * 100)
    for id_usuario, info in usuarios.items():
        print(f"{id_usuario:<10} {info['nombres']:<20} {info['apellidos']:<20} {info['telefono']:<15} {info['direccion']:<25} {info['tipo_usuario']:<15}")

def buscar_usuario():

    usuarios = cargar_datos(USUARIOS_FILE)

    id_usuario = input("Ingrese ID o nombre del usuario a buscar: ").strip().lower()

    for id, info in usuarios.items():
        if id_usuario in id or id_usuario == info["nombres"].lower():
            print("Usuario encontrado:")
            print(f"{id:<10} {info['nombres']:<20} {info['apellidos']:<20} {info['telefono']:<15} {info['direccion']:<25} {info['tipo_usuario']:<15}")
            return
    else:
        print("Usuario no encontrado.")


def actualizar_usuario():

    usuarios = cargar_datos(USUARIOS_FILE)

    id_usuario = input("Ingrese ID del usuario a actualizar: ")

    if id_usuario not in usuarios:
        print(" Usuario no encontrado.")
        return

    print("Deje vacío si no desea cambiar el valor.")

    nombres = input("Nuevo nombre: ")
    apellidos = input("Nuevos apellidos: ")
    telefono = input("Nuevo teléfono: ")
    direccion = input("Nueva dirección: ")
    tipo = input("Nuevo tipo de usuario: ")

    if nombres:
        usuarios[id_usuario]["nombres"] = nombres
    if apellidos:
        usuarios[id_usuario]["apellidos"] = apellidos
    if telefono:
        usuarios[id_usuario]["telefono"] = telefono
    if direccion:
        usuarios[id_usuario]["direccion"] = direccion
    if tipo:
        usuarios[id_usuario]["tipo_usuario"] = tipo

    guardar_datos(usuarios, USUARIOS_FILE)
    print("Usuario actualizado correctamente.")


def eliminar_usuario():

    if not validar_permiso(["administrador"]):
        return
    
    usuarios = cargar_datos(USUARIOS_FILE)

    id_usuario = input("Ingrese ID del usuario a eliminar: ")

    if id_usuario not in usuarios:
        print("Usuario no encontrado.")
        return

    del usuarios[id_usuario]

    guardar_datos(usuarios, USUARIOS_FILE)
    print("Usuario eliminado correctamente.")



def menu_usuarios():

    while True:
        print("""
===== MENÚ GESTIÓN DE USUARIOS =====
1. Crear usuario
2. Listar usuarios
3. Buscar usuario
4. Actualizar usuario
5. Eliminar usuario
6. Volver al menú principal
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            listar_usuarios()
        elif opcion == "3":
            buscar_usuario()
        elif opcion == "4":
            actualizar_usuario()
        elif opcion == "5":
            eliminar_usuario()
        elif opcion == "6":
            break
        else:
            print(" Opción inválida.")
