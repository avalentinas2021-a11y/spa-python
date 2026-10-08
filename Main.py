from Cliente import Cliente
from Profesional import Profesional
from Servicio import Servicio
from Turno import Turno


# Listas donde vamos a guardar nuestros objetos
clientes = []
profesionales = []
servicios = []
turnos = []


# Contadores para generar los ID
ultimo_id_cliente = 0
ultimo_id_profesional = 0
ultimo_id_servicio = 0
ultimo_id_turno = 0


def registrar_cliente():
    global ultimo_id_cliente

    print("\n===== REGISTRAR CLIENTE =====")

    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    dni = input("DNI: ")
    telefono = input("Teléfono: ")
    email = input("Email: ")

    ultimo_id_cliente += 1

    cliente = Cliente(
        ultimo_id_cliente,
        nombre,
        apellido,
        dni,
        telefono,
        email
    )

    clientes.append(cliente)

    print("\nCliente registrado correctamente.")


def registrar_profesional():
    global ultimo_id_profesional

    print("\n===== REGISTRAR PROFESIONAL =====")

    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    dni = input("DNI: ")
    telefono = input("Teléfono: ")
    email = input("Email: ")
    especialidad = input("Especialidad: ")

    ultimo_id_profesional += 1

    profesional = Profesional(
        ultimo_id_profesional,
        nombre,
        apellido,
        dni,
        telefono,
        email,
        especialidad
    )

    profesionales.append(profesional)

    print("\nProfesional registrado correctamente.")


def registrar_servicio():
    global ultimo_id_servicio

    print("\n===== REGISTRAR SERVICIO =====")

    nombre = input("Nombre del servicio: ")
    descripcion = input("Descripción: ")
    duracion = int(input("Duración en minutos: "))
    precio = float(input("Precio: "))

    ultimo_id_servicio += 1

    servicio = Servicio(
        ultimo_id_servicio,
        nombre,
        descripcion,
        duracion,
        precio
    )

    servicios.append(servicio)

    print("\nServicio registrado correctamente.")


def ver_clientes():

    print("\n===== CLIENTES =====")

    if len(clientes) == 0:
        print("No hay clientes registrados.")
        return

    for cliente in clientes:
        cliente.mostrar_datos()
        print("------------------------")


def ver_profesionales():

    print("\n===== PROFESIONALES =====")

    if len(profesionales) == 0:
        print("No hay profesionales registrados.")
        return

    for profesional in profesionales:
        profesional.mostrar_datos()
        print("------------------------")


def ver_servicios():

    print("\n===== SERVICIOS =====")

    if len(servicios) == 0:
        print("No hay servicios registrados.")
        return

    for servicio in servicios:
        servicio.mostrar_datos()
        print("------------------------")


def reservar_turno():
    global ultimo_id_turno

    print("\n===== RESERVAR TURNO =====")

    if len(clientes) == 0:
        print("No hay clientes registrados.")
        return

    if len(profesionales) == 0:
        print("No hay profesionales registrados.")
        return

    if len(servicios) == 0:
        print("No hay servicios registrados.")
        return

    print("\nClientes disponibles:")

    for cliente in clientes:
        print(
            cliente.id_cliente,
            "-",
            cliente.nombre,
            cliente.apellido
        )

    id_cliente = int(input("Seleccione el ID del cliente: "))

    cliente_seleccionado = None

    for cliente in clientes:
        if cliente.id_cliente == id_cliente:
            cliente_seleccionado = cliente
            break

    if cliente_seleccionado is None:
        print("Cliente no encontrado.")
        return

    print("\nProfesionales disponibles:")

    for profesional in profesionales:
        print(
            profesional.id_profesional,
            "-",
            profesional.nombre,
            profesional.apellido,
            "-",
            profesional.especialidad
        )

    id_profesional = int(
        input("Seleccione el ID del profesional: ")
    )

    profesional_seleccionado = None

    for profesional in profesionales:
        if profesional.id_profesional == id_profesional:
            profesional_seleccionado = profesional
            break

    if profesional_seleccionado is None:
        print("Profesional no encontrado.")
        return

    print("\nServicios disponibles:")

    for servicio in servicios:
        print(
            servicio.id_servicio,
            "-",
            servicio.nombre,
            "- $",
            servicio.precio
        )

    id_servicio = int(
        input("Seleccione el ID del servicio: ")
    )

    servicio_seleccionado = None

    for servicio in servicios:
        if servicio.id_servicio == id_servicio:
            servicio_seleccionado = servicio
            break

    if servicio_seleccionado is None:
        print("Servicio no encontrado.")
        return

    fecha = input("Fecha (DD/MM/AAAA): ")
    hora = input("Hora (HH:MM): ")

    # Verificar si el profesional ya tiene un turno
    # en esa fecha y horario
    for turno in turnos:

        if (
            turno.profesional.id_profesional == id_profesional
            and turno.fecha == fecha
            and turno.hora == hora
            and turno.estado == "Activo"
        ):
            print("\nEl profesional no está disponible en ese horario.")
            return

    ultimo_id_turno += 1

    turno = Turno(
        ultimo_id_turno,
        cliente_seleccionado,
        profesional_seleccionado,
        servicio_seleccionado,
        fecha,
        hora,
        "Activo"
    )

    turnos.append(turno)

    print("\nTurno registrado correctamente.")


def ver_turnos():

    print("\n===== TURNOS =====")

    if len(turnos) == 0:
        print("No hay turnos registrados.")
        return

    for turno in turnos:
        turno.mostrar_datos()
        print("------------------------")


def cancelar_turno():

    print("\n===== CANCELAR TURNO =====")

    if len(turnos) == 0:
        print("No hay turnos registrados.")
        return

    for turno in turnos:

        print(
            "ID:",
            turno.id_turno,
            "|",
            turno.fecha,
            turno.hora,
            "|",
            turno.cliente.nombre,
            turno.cliente.apellido,
            "| Estado:",
            turno.estado
        )

    id_turno = int(input("\nSeleccione el ID del turno: "))

    for turno in turnos:

        if turno.id_turno == id_turno:

            if turno.estado == "Cancelado":
                print("El turno ya está cancelado.")
                return

            turno.cancelar()

            print("Turno cancelado correctamente.")
            return

    print("Turno no encontrado.")


def mostrar_menu():

    print("\n")
    print("========================================")
    print("       SISTEMA DE GESTIÓN SPA")
    print("========================================")
    print("1. Registrar cliente")
    print("2. Registrar profesional")
    print("3. Registrar servicio")
    print("4. Reservar turno")
    print("5. Ver clientes")
    print("6. Ver profesionales")
    print("7. Ver servicios")
    print("8. Ver turnos")
    print("9. Cancelar turno")
    print("0. Salir")
    print("========================================")


# ==============================
# PROGRAMA PRINCIPAL
# ==============================

while True:

    mostrar_menu()

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_cliente()

    elif opcion == "2":
        registrar_profesional()

    elif opcion == "3":
        registrar_servicio()

    elif opcion == "4":
        reservar_turno()

    elif opcion == "5":
        ver_clientes()

    elif opcion == "6":
        ver_profesionales()

    elif opcion == "7":
        ver_servicios()

    elif opcion == "8":
        ver_turnos()

    elif opcion == "9":
        cancelar_turno()

    elif opcion == "0":
        print("\nPrograma finalizado.")
        break

    else:
        print("\nOpción incorrecta.")