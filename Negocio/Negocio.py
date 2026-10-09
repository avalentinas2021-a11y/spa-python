from Modelos.Cliente import Cliente
from Modelos.Profesional import Profesional
from Modelos.Servicio import Servicio
import Datos.Datos as db


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

def registrar_cliente(nombre, apellido, dni, telefono, email):
    db.ultimo_id_cliente += 1
    nuevo_cliente = Cliente(db.ultimo_id_cliente, nombre, apellido, dni, telefono, email)
    db.clientes.append(nuevo_cliente)

def registrar_profesional(nombre, apellido, dni, telefono, email, especialidad):
    db.ultimo_id_profesional += 1
    nuevo_profesional = Profesional(db.ultimo_id_profesional, nombre, apellido, dni, telefono, email, especialidad)
    db.profesionales.append(nuevo_profesional)

def registrar_servicio(nombre, descripcion, duracion, precio):
    db.ultimo_id_servicio += 1
    nuevo_servicio = Servicio(db.ultimo_id_servicio, nombre, descripcion, duracion, precio)
    db.servicios.append(nuevo_servicio)

# --- FUNCIONES DE LECTURA ---
def obtener_clientes():
    return db.clientes

def obtener_profesionales():
    return db.profesionales

def obtener_servicios():
    return db.servicios