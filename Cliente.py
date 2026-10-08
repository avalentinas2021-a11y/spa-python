from Persona import Persona


class Cliente(Persona):

    def __init__(self, id_cliente, nombre, apellido, dni, telefono, email):
        super().__init__(nombre, apellido, dni, telefono, email)
        self.id_cliente = id_cliente

    def mostrar_datos(self):
        print("----- CLIENTE -----")
        print("ID:", self.id_cliente)
        print("Nombre:", self.nombre)
        print("Apellido:", self.apellido)
        print("DNI:", self.dni)
        print("Teléfono:", self.telefono)
        print("Email:", self.email)