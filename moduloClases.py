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

class Cliente:
    def __init__(self,nombre,documento):
        self.nombre=nombre
        self.documento=documento
    def mostrar_informacion:
        print(f"Cliente: {self.nombre}")
        print(f"Documento: {self.documento}")
class Servicio:
    def __init__(self,nombre,precio,cantidad):
        self.nombre=nombre
        self.precio=precio
        self.cantidad=cantidad
    def subtotal(self):
        return self.precio*self.cantidad

class Estadia:
    # dos tipos de habitacion: Noche o Corta
    def __init__(self,cliente,tipo_habitacion, tipo_estadia, hora_ingreso, noches=1):
        self.cliente=cliente
        self.tipo_habitacion=tipo_habitacion
        self.tipo_estadia=tipo_estadia
        self.hora_ingreso=hora_ingreso
        self.noches=noches
        self.servicios=[]
    def calcular_hospedaje(self):
        if self.tipo_estadia=="Corta":
            return PRECIO_ESTADIA_CORTA
        return PRECIOS_NOCHE[self.tipo_habitacion]*self.noches
    def calcular_recargo(self,minutos_usados):
        if self.tipo_estadio=="Corta":
            limite=180 # son 3 horas
        else:
            limite= 1500+1440*(self.noches - 1)
        exceso=minuto_usados-limite
        fracciones=0
        while exceso>0:
            fracciones=fracciones+1
            exceso= exceso-60
        return fracciones*RECARGO_POR_HORA
    def agregar_servicio(self,nombre,precio,cantidad):
        servicio=Servicio(nombre,precio,cantidad)
        self.servicios.append(servicio)
    def quitar_servicio(self,indice):
        if 0 <=indice <len(self.servicios):
            return self.servicios.pop(indice)
        return None
    def calcular_total_servicios(self):
        total=0
        for servicio in self.servicios:
            total= total+servicio.subtotal()
            return total
    def calcular_total(self,minutos_usados):
        return (self.calcular_hospedaje()
                + self.calcular_recargo(minutos_usados)
                + self.calcular_total_servicios())
                

        
        


        
        

    
                            
        
