#Clases
from moduloDatos import (PRECIOS_NOCHE, PRECIO_ESTADIA_CORTA, RECARGO_POR_HORA, HABITACIONES)

class Habitacion:
    def __init__(self, numero, tipo):
        self.numero = numero
        self.tipo = tipo
        self.estadia = None 

    def esta_disponible(self):
        return self.estadia is None

    def mostrar_estado(self):
        if self.esta_disponible():
            print(f"Habitacion {self.numero} ({self.tipo}): DISPONIBLE")
        else:
            nombre = self.estadia.cliente.nombre
            print(f"Habitacion {self.numero} ({self.tipo}): OCUPADA por {nombre}")


class Hostal:
    def __init__(self):
        self.habitaciones = []
        for numero, tipo in HABITACIONES.items():
            self.habitaciones.append(Habitacion(numero, tipo))
        self.huespedes_dia = 0
        self.ingresos_dia = 0

    def buscar_habitacion(self, numero):
        for habitacion in self.habitaciones:
            if habitacion.numero == numero:
                return habitacion
        return None

    def habitaciones_disponibles(self):
        return [h for h in self.habitaciones if h.esta_disponible()]

    def habitaciones_ocupadas(self):
        return [h for h in self.habitaciones if not h.esta_disponible()]
