class Servicio:

    def __init__(self, id_servicio, nombre, descripcion, duracion, precio):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.descripcion = descripcion
        self.duracion = duracion
        self.precio = precio

    def mostrar_datos(self):
        print("----- SERVICIO -----")
        print("ID:", self.id_servicio)
        print("Nombre:", self.nombre)
        print("Descripción:", self.descripcion)
        print("Duración:", self.duracion, "minutos")
        print("Precio: $", self.precio)