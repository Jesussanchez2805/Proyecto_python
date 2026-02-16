from modulos.datos import cargar_datos, guardar_datos, USUARIOS_FILE,registrar_log
usuario_actual = None

def verificar_primer_inicio():


    usuarios = cargar_datos(USUARIOS_FILE)

    if not usuarios:
        print("""
==================================
PRIMER INICIO DEL SISTEMA
Debe crear el administrador principal
==================================
""")

        id_usuario = input("ID administrador: ")
        nombres = input("Nombres: ")
        apellidos = input("Apellidos: ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")

        usuarios[id_usuario] = {
            "nombres": nombres,
            "apellidos": apellidos,
            "telefono": telefono,
            "direccion": direccion,
            "tipo_usuario": "administrador"
        }

        guardar_datos(usuarios, USUARIOS_FILE)

        print(" Administrador principal creado correctamente.\n")

def iniciar_sesion():

    global usuario_actual

    usuarios = cargar_datos(USUARIOS_FILE)

    id_usuario = input("Ingrese su ID de usuario: ")

    if id_usuario not in usuarios:
        print("Usuario no encontrado.")
        return False

    usuario_actual = {
        "id": id_usuario,
        "tipo": usuarios[id_usuario]["tipo_usuario"],
        "nombre": usuarios[id_usuario]["nombres"]
    }

    print(f"Bienvenido {usuario_actual['nombre']} con tipo de usuario ({usuario_actual['tipo']})")
    return True

def validar_permiso(usuarios_permitidos):

    if usuario_actual is None:
        registrar_log("ERROR", "Intento de acceso sin iniciar sesión")
        print(" Debe iniciar sesión primero.")
        return False

    if usuario_actual["tipo"] not in usuarios_permitidos:
        registrar_log("ERROR", f"Usuario {usuario_actual['id']} intentó acceder sin permisos")
        print("No tiene permisos para realizar esta acción.")
        return False

    return True