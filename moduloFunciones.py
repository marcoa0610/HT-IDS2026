#Funciones
# Funciones
from moduloDatos import SERVICIOS

def pedir_habitacion_ocupada(hostal):
    try:
        numero_hab = int(input("Numero de habitacion: "))
    except ValueError:
        print("Debe ingresar un numero valido.")
        return None

    habitacion = hostal.buscar_habitacion(numero_hab)
    if habitacion is None:
        print("Esa habitacion no existe.")
        return None
    if habitacion.esta_disponible():
        print("Esa habitacion no tiene huesped.")
        return None
    return habitacion

def gestionar_servicios(hostal):
    habitacion = pedir_habitacion_ocupada(hostal)
    if habitacion is None:
        return

    estadia = habitacion.estadia
    nombres = []
    for servicio in SERVICIOS:
        nombres.append(servicio)
    opcion_quitar = len(nombres) + 1

    while True:
        print("\n--- SERVICIOS ADICIONALES ---")
        print(f"Habitacion {habitacion.numero} - {estadia.cliente.nombre}")
        numero = 1
        for nombre in nombres:
            precio = SERVICIOS[nombre]
            print(f"{numero}. {nombre} - ${precio:.2f}")
            numero += 1
        print(f"{opcion_quitar}. Quitar un cargo")
        print("0. Volver al menu principal")
        try:
            opcion = int(input("Opcion: "))
        except ValueError:
            print("Opcion invalida.")
            continue

        if opcion == 0:
            print("Volviendo al menu principal...")
            break
        elif opcion == opcion_quitar:
            quitar_cargo(estadia)
        elif 1 <= opcion <= len(nombres):
            nombre_elegido = nombres[opcion - 1]
            try:
                cantidad = int(input("Cantidad: "))
            except ValueError:
                cantidad = 0

            if cantidad < 1:
                print("Cantidad invalida.")
            else:
                estadia.agregar_servicio(nombre_elegido, SERVICIOS[nombre_elegido], cantidad)
                print(f"Servicio agregado. Subtotal de servicios: ${estadia.calcular_total_servicios():.2f}")
        else:
            print("Opcion invalida.")

def quitar_cargo(estadia):
    if len(estadia.servicios) == 0:
        print("Esta habitacion no tiene servicios cargados.")
        return
    print("\n--- CARGOS DE LA HABITACION ---")
    numero = 1
    for servicio in estadia.servicios:
        print(f"{numero}. {servicio.nombre} x{servicio.cantidad} = ${servicio.subtotal():.2f}")
        numero += 1
    try:
        numero_cargo = int(input("Numero del cargo a quitar: "))
    except ValueError:
        print("Dato invalido.")
        return
    quitado = estadia.quitar_servicio(numero_cargo - 1)
    if quitado is None:
        print("Ese cargo no existe.")
    else:
        print(f"Cargo quitado: {quitado.nombre}. Subtotal de servicios: ${estadia.calcular_total_servicios():.2f}")


  
  
