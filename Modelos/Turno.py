class Turno:

    def __init__(
        self,
        id_turno,
        cliente,
        profesional,
        servicio,
        fecha,
        hora,
        estado
    ):
        self.id_turno = id_turno
        self.cliente = cliente
        self.profesional = profesional
        self.servicio = servicio
        self.fecha = fecha
        self.hora = hora
        self.estado = estado

    def mostrar_datos(self):
        print("----- TURNO -----")
        print("ID:", self.id_turno)
        print("Cliente:", self.cliente.nombre, self.cliente.apellido)
        print("Profesional:", self.profesional.nombre, self.profesional.apellido)
        print("Servicio:", self.servicio.nombre)
        print("Fecha:", self.fecha)
        print("Hora:", self.hora)
        print("Estado:", self.estado)

    def cancelar(self):
        self.estado = "Cancelado"