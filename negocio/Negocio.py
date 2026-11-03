import datos.Datos as db


def registrar_cliente(nombre, apellido, dni, telefono, email):
    return db.registrar_cliente(nombre, apellido, dni, telefono, email)


def registrar_profesional(
    nombre, apellido, dni, telefono, email, especialidad
):
    return db.registrar_profesional(
        nombre, apellido, dni, telefono, email, especialidad
    )


def registrar_servicio(nombre, descripcion, duracion, precio):
    return db.registrar_servicio(nombre, descripcion, duracion, precio)


def obtener_clientes():
    return db.obtener_clientes()


def obtener_profesionales():
    return db.obtener_profesionales()


def obtener_servicios():
    return db.obtener_servicios()


def reservar_turno(id_cliente, id_profesional, id_servicio, fecha, hora):
    if db.horario_ocupado(id_profesional, fecha, hora):
        raise ValueError("El profesional no está disponible en ese horario.")
    return db.registrar_turno(
        id_cliente, id_profesional, id_servicio, fecha, hora
    )


def obtener_turnos():
    return db.obtener_turnos()


def cancelar_turno(id_turno):
    return db.cancelar_turno(id_turno)
