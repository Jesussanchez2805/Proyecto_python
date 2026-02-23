"""
Módulo para gestionar solicitudes de préstamo de herramientas.
- Residentes pueden crear solicitudes.
- Administradores pueden aprobar o rechazar solicitudes.
  Al aprobar, se genera el préstamo automáticamente.
"""

from modulos.datos import (
    cargar_datos, guardar_datos,
    HERRAMIENTAS_FILE, USUARIOS_FILE, PRESTAMOS_FILE,
    SOLICITUDES_FILE, registrar_log
)
from modulos import Validacion_roles
from modulos.Validacion_roles import validar_permiso
from datetime import datetime

# Acceso dinámico: siempre leer Validacion_roles.usuario_actual en tiempo de ejecución,
# nunca importar la variable directamente (se copiaría el None inicial y no se actualizaría).


# ──────────────────────────────────────────────
# UTILIDADES INTERNAS
# ──────────────────────────────────────────────

def _generar_id_solicitud(solicitudes: dict) -> str:
    """Genera un ID único para la solicitud (SOL-001, SOL-002 …)."""
    if not solicitudes:
        return "SOL-001"
    ultimo = max(
        int(k.split("-")[1]) for k in solicitudes if k.startswith("SOL-")
    )
    return f"SOL-{ultimo + 1:03d}"


def _generar_id_prestamo(prestamos: dict) -> str:
    """Genera un ID único para el préstamo cuando se aprueba la solicitud."""
    if not prestamos:
        return "PRES-001" 
    numeros = []
    for k in prestamos:
        if k.startswith("PRES-"):
            try:
                numeros.append(int(k.split("-")[1]))
            except ValueError:
                pass
    ultimo = max(numeros) if numeros else 0
    return f"PRES-{ultimo + 1:03d}"


# ──────────────────────────────────────────────
# ACCIONES DE RESIDENTE
# ──────────────────────────────────────────────

def crear_solicitud():
    """Permite a un residente (o administrador) crear una solicitud de herramienta."""

    if not validar_permiso(["residente", "administrador"]):
        return

    herramientas = cargar_datos(HERRAMIENTAS_FILE)
    solicitudes  = cargar_datos(SOLICITUDES_FILE)

    if not herramientas:
        print("No hay herramientas registradas en el sistema.")
        return

    # Mostrar herramientas disponibles
    print("\n=== HERRAMIENTAS DISPONIBLES ===")
    print(f"{'ID':<12} {'Nombre':<22} {'Cantidad disponible':<22} {'Estado':<15}")
    print("-" * 75)
    for id_h, info in herramientas.items():
        if info["estado"] == "activa" and info["cantidad"] > 0:
            print(f"{id_h:<12} {info['nombre']:<22} {info['cantidad']:<22} {info['estado']:<15}")

    print()
    id_herramienta = input("ID de la herramienta que desea solicitar: ").strip()

    if id_herramienta not in herramientas:
        print(" Herramienta no encontrada.")
        return

    herramienta = herramientas[id_herramienta]

    if herramienta["estado"] != "activa":
        print(" La herramienta no está activa.")
        return

    try:
        cantidad = int(input("Cantidad que desea solicitar: "))
    except ValueError:
        print(" Cantidad inválida.")
        return

    if cantidad <= 0:
        print(" La cantidad debe ser mayor a 0.")
        return

    if herramienta["cantidad"] < cantidad:
        print(f" Solo hay {herramienta['cantidad']} unidad(es) disponible(s).")
        return

    fecha_inicio     = input("Fecha de inicio del préstamo (YYYY-MM-DD): ").strip()
    fecha_devolucion = input("Fecha estimada de devolución (YYYY-MM-DD): ").strip()
    motivo           = input("Motivo de la solicitud: ").strip()

    id_solicitud = _generar_id_solicitud(solicitudes)

    solicitudes[id_solicitud] = {
        "usuario"         : Validacion_roles.usuario_actual["id"],
        "herramienta"     : id_herramienta,
        "cantidad"        : cantidad,
        "fecha_inicio"    : fecha_inicio,
        "fecha_estimada_devolucion": fecha_devolucion,
        "motivo"          : motivo,
        "estado"          : "pendiente",   # pendiente | aprobada | rechazada
        "fecha_solicitud" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "observaciones_admin": ""
    }

    guardar_datos(solicitudes, SOLICITUDES_FILE)
    registrar_log("INFO", f"Solicitud creada: {id_solicitud} por usuario {Validacion_roles.usuario_actual['id']}")
    print(f"\n Solicitud {id_solicitud} enviada correctamente. Espere la aprobación del administrador.")


def mis_solicitudes():
    """Muestra las solicitudes del usuario en sesión."""

    if not validar_permiso(["residente", "administrador"]):
        return

    solicitudes = cargar_datos(SOLICITUDES_FILE)

    mis = {k: v for k, v in solicitudes.items() if v["usuario"] == Validacion_roles.usuario_actual["id"]}

    if not mis:
        print("\n No tienes solicitudes registradas.")
        return

    print("\n=== MIS SOLICITUDES ===")
    print(f"{'ID':<12} {'Herramienta':<15} {'Cant':<6} {'Fecha solicitud':<22} {'Estado':<12} {'Obs. Admin':<30}")
    print("-" * 100)
    for id_s, info in mis.items():
        print(
            f"{id_s:<12} {info['herramienta']:<15} {info['cantidad']:<6} "
            f"{info['fecha_solicitud']:<22} {info['estado'].upper():<12} "
            f"{info['observaciones_admin']:<30}"
        )


# ──────────────────────────────────────────────
# ACCIONES DE ADMINISTRADOR
# ──────────────────────────────────────────────

def listar_solicitudes_pendientes():
    """Lista todas las solicitudes con estado pendiente (vista de administrador)."""

    if not validar_permiso(["administrador"]):
        return

    solicitudes = cargar_datos(SOLICITUDES_FILE)
    usuarios    = cargar_datos(USUARIOS_FILE)

    pendientes = {k: v for k, v in solicitudes.items() if v["estado"] == "pendiente"}

    if not pendientes:
        print("\n No hay solicitudes pendientes.")
        return

    print("\n=== SOLICITUDES PENDIENTES ===")
    print(f"{'ID':<12} {'Usuario':<15} {'Nombre':<20} {'Herramienta':<15} {'Cant':<6} {'F. Inicio':<12} {'F. Devolución':<15} {'Motivo':<30}")
    print("-" * 130)

    for id_s, info in pendientes.items():
        nombre_usuario = usuarios.get(info["usuario"], {}).get("nombres", "Desconocido")
        print(
            f"{id_s:<12} {info['usuario']:<15} {nombre_usuario:<20} "
            f"{info['herramienta']:<15} {info['cantidad']:<6} "
            f"{info['fecha_inicio']:<12} {info['fecha_estimada_devolucion']:<15} "
            f"{info['motivo']:<30}"
        )


def listar_todas_solicitudes():
    """Lista TODAS las solicitudes sin importar su estado."""

    if not validar_permiso(["administrador"]):
        return

    solicitudes = cargar_datos(SOLICITUDES_FILE)
    usuarios    = cargar_datos(USUARIOS_FILE)

    if not solicitudes:
        print("\n No hay solicitudes registradas.")
        return

    print("\n=== TODAS LAS SOLICITUDES ===")
    print(f"{'ID':<12} {'Usuario':<15} {'Herramienta':<15} {'Cant':<6} {'Estado':<12} {'Fecha solicitud':<22} {'Obs. Admin':<30}")
    print("-" * 115)

    for id_s, info in solicitudes.items():
        print(
            f"{id_s:<12} {info['usuario']:<15} {info['herramienta']:<15} "
            f"{info['cantidad']:<6} {info['estado'].upper():<12} "
            f"{info['fecha_solicitud']:<22} {info['observaciones_admin']:<30}"
        )


def aprobar_solicitud():
    """
    Aprueba una solicitud pendiente.
    - Descuenta el stock de la herramienta.
    - Crea automáticamente el registro de préstamo.
    """

    if not validar_permiso(["administrador"]):
        return

    listar_solicitudes_pendientes()

    solicitudes  = cargar_datos(SOLICITUDES_FILE)
    herramientas = cargar_datos(HERRAMIENTAS_FILE)
    prestamos    = cargar_datos(PRESTAMOS_FILE)

    id_solicitud = input("\nIngrese el ID de la solicitud a APROBAR: ").strip()

    if id_solicitud not in solicitudes:
        print(" Solicitud no encontrada.")
        return

    solicitud = solicitudes[id_solicitud]

    if solicitud["estado"] != "pendiente":
        print(f" Esta solicitud ya fue procesada (estado: {solicitud['estado']}).")
        return

    id_herramienta = solicitud["herramienta"]
    cantidad       = solicitud["cantidad"]

    # Validaciones antes de aprobar
    if id_herramienta not in herramientas:
        print(" La herramienta ya no existe en el sistema.")
        return

    herramienta = herramientas[id_herramienta]

    if herramienta["estado"] != "activa":
        print(" La herramienta ya no está activa.")
        return

    if herramienta["cantidad"] < cantidad:
        print(f" Stock insuficiente. Disponible: {herramienta['cantidad']}, solicitado: {cantidad}.")
        return

    obs = input("Observaciones del administrador (opcional): ").strip()

    # Descontar stock
    herramientas[id_herramienta]["cantidad"] -= cantidad
    guardar_datos(herramientas, HERRAMIENTAS_FILE)

    # Crear préstamo automáticamente
    id_prestamo = _generar_id_prestamo(prestamos)
    prestamos[id_prestamo] = {
        "usuario"                  : solicitud["usuario"],
        "herramienta"              : id_herramienta,
        "cantidad"                 : cantidad,
        "fecha_inicio"             : solicitud["fecha_inicio"],
        "fecha_estimada_devolucion": solicitud["fecha_estimada_devolucion"],
        "estado"                   : "activo",
        "observaciones"            : f"Generado desde solicitud {id_solicitud}. {obs}"
    }
    guardar_datos(prestamos, PRESTAMOS_FILE)

    # Actualizar estado de la solicitud
    solicitudes[id_solicitud]["estado"]               = "aprobada"
    solicitudes[id_solicitud]["observaciones_admin"]  = obs
    guardar_datos(solicitudes, SOLICITUDES_FILE)

    registrar_log("INFO", f"Solicitud {id_solicitud} APROBADA por {Validacion_roles.usuario_actual['id']}. Préstamo generado: {id_prestamo}")
    print(f"\n Solicitud {id_solicitud} aprobada. Préstamo {id_prestamo} generado automáticamente.")


def rechazar_solicitud():
    """Rechaza una solicitud pendiente sin afectar el stock."""

    if not validar_permiso(["administrador"]):
        return

    listar_solicitudes_pendientes()

    solicitudes = cargar_datos(SOLICITUDES_FILE)

    id_solicitud = input("\nIngrese el ID de la solicitud a RECHAZAR: ").strip()

    if id_solicitud not in solicitudes:
        print(" Solicitud no encontrada.")
        return

    solicitud = solicitudes[id_solicitud]

    if solicitud["estado"] != "pendiente":
        print(f" Esta solicitud ya fue procesada (estado: {solicitud['estado']}).")
        return

    motivo_rechazo = input("Motivo del rechazo: ").strip()

    solicitudes[id_solicitud]["estado"]              = "rechazada"
    solicitudes[id_solicitud]["observaciones_admin"] = motivo_rechazo
    guardar_datos(solicitudes, SOLICITUDES_FILE)

    registrar_log("INFO", f"Solicitud {id_solicitud} RECHAZADA por {Validacion_roles.usuario_actual['id']}. Motivo: {motivo_rechazo}")
    print(f"\n Solicitud {id_solicitud} rechazada correctamente.")


# ──────────────────────────────────────────────
# MENÚS
# ──────────────────────────────────────────────

def menu_solicitudes():
    """Menú principal de solicitudes. Muestra opciones según el rol del usuario."""

    while True:
        # Opciones comunes a todos los roles
        print("""
===== MENÚ DE SOLICITUDES DE HERRAMIENTAS =====
1. Crear nueva solicitud
2. Ver mis solicitudes""")

        # Opciones exclusivas del administrador
        es_admin = Validacion_roles.usuario_actual and Validacion_roles.usuario_actual["tipo"] == "administrador"
        if es_admin:
            print("""3. Ver solicitudes pendientes
4. Aprobar solicitud
5. Rechazar solicitud
6. Ver todas las solicitudes
7. Volver al menú principal""")
        else:
            print("3. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            crear_solicitud()
        elif opcion == "2":
            mis_solicitudes()
        elif opcion == "3":
            if es_admin:
                listar_solicitudes_pendientes()
            else:
                break
        elif opcion == "4" and es_admin:
            aprobar_solicitud()
        elif opcion == "5" and es_admin:
            rechazar_solicitud()
        elif opcion == "6" and es_admin:
            listar_todas_solicitudes()
        elif opcion == "7" and es_admin:
            break
        else:
            print(" Opción inválida.")
