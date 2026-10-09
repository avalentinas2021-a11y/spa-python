class Persona:

    def __init__(self, nombre, apellido, dni, telefono, email):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.email = email

    def mostrar_datos(self):
        print("Nombre:", self.nombre)
        print("Apellido:", self.apellido)
        print("DNI:", self.dni)
        print("Teléfono:", self.telefono)
        print("Email:", self.email)