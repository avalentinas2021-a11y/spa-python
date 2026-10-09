from Modelos.Persona import Persona


class Profesional(Persona):

    def __init__(
        self,
        id_profesional,
        nombre,
        apellido,
        dni,
        telefono,
        email,
        especialidad
    ):
        super().__init__(nombre, apellido, dni, telefono, email)
        self.id_profesional = id_profesional
        self.especialidad = especialidad

    def mostrar_datos(self):
        print("----- PROFESIONAL -----")
        print("ID:", self.id_profesional)
        print("Nombre:", self.nombre)
        print("Apellido:", self.apellido)
        print("DNI:", self.dni)
        print("Teléfono:", self.telefono)
        print("Email:", self.email)
        print("Especialidad:", self.especialidad)