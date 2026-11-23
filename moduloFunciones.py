# Funciones
from datetime import datetime, time
from moduloClases import Cliente
from moduloClases import Estadia
from moduloDatos import SERVICIOS
from moduloDatos import SERVICIOS_UNICOS
from moduloDatos import PRECIOS_NOCHE
from moduloDatos import PRECIO_ESTADIA_CORTA


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

            if nombre_elegido in SERVICIOS_UNICOS:
                ya_cargado = any(s.nombre == nombre_elegido for s in estadia.servicios)
                if ya_cargado:
                    print("Este servicio ya fue cargado (solo puede ser uno).")
                    continue
                cantidad = 1
            else:
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


def check_in(hostal):
    print("\n===== CHECK-IN =====")
    if len(hostal.habitaciones_disponibles()) == 0:
        print("No hay habitaciones disponibles.")
        return
    while True:
        nombre = input("Nombre del huesped: ").strip().title()
        if nombre != "":
            break
        print("El nombre no puede estar vacio")
    while True:
        documento = input("Numero de documento: ").strip()
        if documento != "":
            break
        print("No puede estar vacio el documento")
    while True:
        print("Estos son los precios que manejamos si tu tipo estadia es noche:")
        for llave, valor in PRECIOS_NOCHE.items():
            print(f"{llave}: ${valor}")
        print(f"Este es el precio si su estadia es corta: ${PRECIO_ESTADIA_CORTA}")
        tipo_estadia = input("Tipo de estadia (Noche/Corta): ").strip().capitalize()
        if tipo_estadia == "Noche" or tipo_estadia == "Corta":
            break
        else:
            print("Tipo de estadia invalido.")

    # Las estadias cortas solo se asignan a habitaciones sencillas
    if tipo_estadia == "Corta":
        disponibles = [h for h in hostal.habitaciones_disponibles() if h.tipo == "Sencilla"]
        if not disponibles:
            print("No hay habitaciones sencillas disponibles para estadia corta.")
            return
    else:
        disponibles = hostal.habitaciones_disponibles()

    numeros_validos = [h.numero for h in disponibles]
    while True:
        print("Estas son las habitaciones disponibles:")
        for h in disponibles:
            print(f"{h.numero}: {h.tipo}")
        try:
            numero = int(input("Numero de habitacion: "))
        except ValueError:
            print("Debe ingresar un numero valido.")
            continue
        if numero not in numeros_validos:
            print("Esa habitacion no esta disponible para este tipo de estadia.")
            continue
        habitacion = hostal.buscar_habitacion(numero)
        break

    hora_ingreso = input("Hora de ingreso (HH:MM): ")
    try:
        hora = datetime.strptime(hora_ingreso, "%H:%M").time()
    except ValueError:
        print("Formato de hora invalido.")
        return
    if tipo_estadia == "Corta":
        if not (time(8, 0) <= hora <= time(19, 0)):
            print("Fuera de horario.")
            return
    noches = 1
    if tipo_estadia == "Noche":
        try:
            noches = int(input("Cantidad de noches: "))
        except ValueError:
            print("Debe ingresar un numero valido.")
            return
        if noches < 1:
            print("La cantidad de noches debe ser mayor a cero.")
            return
    cliente = Cliente(nombre, documento)
    estadia = Estadia(
        cliente,
        habitacion.tipo,
        tipo_estadia,
        hora_ingreso,
        noches
    )
    habitacion.estadia = estadia
    hostal.huespedes_dia += 1
    print("\n===== CHECK-IN EXITOSO =====")
    print(f"Huesped: {cliente.nombre.title()}")
    print(f"Documento: {cliente.documento}")
    print(f"Habitacion: {habitacion.numero}")
    print(f"Tipo de habitacion: {habitacion.tipo}")
    print(f"Tipo de estadia: {tipo_estadia}")
    print(f"Hora de ingreso: {hora_ingreso}")
    print(f"Tarifa base: ${estadia.calcular_hospedaje():.2f}")


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


def reporteDiario(hostal):
    print("\n--- REPORTE DIARIO ---")
    print(f"Huespedes registrados: {hostal.huespedes_dia}")
    print(f"Ingresos del dia: ${hostal.ingresos_dia:.2f}")
    print("\n- ESTADO DE HABITACIONES -")
    ocupadas = hostal.habitaciones_ocupadas()
    disponibles = hostal.habitaciones_disponibles()
    print(f"Habitaciones ocupadas: {len(ocupadas)}")
    print(f"Habitaciones disponibles: {len(disponibles)}")
    print(f"Total de habitaciones: {len(hostal.habitaciones)}")
    print("\n- DETALLE DE HABITACIONES -")
    for habitacion in hostal.habitaciones:
        habitacion.mostrar_estado()


def check_out(hostal):
    print("\n--- CHECK-OUT ---")
    habitacion = pedir_habitacion_ocupada(hostal)

    if habitacion is None:
        return

    estadia = habitacion.estadia

    hora_retiro = input("Hora de retiro (HH:MM): ")
    try:
        hora = datetime.strptime(hora_retiro, "%H:%M").time()
    except ValueError:
        print("Formato de hora invalido.")
        return

    hora_ingreso = datetime.strptime(
        estadia.hora_ingreso, "%H:%M"
    ).time()
    minutos_ingreso = (
        hora_ingreso.hour * 60 + hora_ingreso.minute
    )
    minutos_retiro = hora.hour * 60 + hora.minute

    if estadia.tipo_estadia == "Corta":
        minutos_usados = minutos_retiro - minutos_ingreso
        if minutos_usados < 0:
            minutos_usados = minutos_usados + 1440
    else:
        minutos_usados = (
            1440 * estadia.noches + minutos_retiro - minutos_ingreso
        )

    hospedaje = estadia.calcular_hospedaje()
    recargo = estadia.calcular_recargo(minutos_usados)
    servicios = estadia.calcular_total_servicios()
    total = estadia.calcular_total(minutos_usados)

    print("\n--- FACTURA ---")
    print(f"Huesped: {estadia.cliente.nombre}")
    print(f"Habitación: {habitacion.numero}")
    print(f"Tipo de Habitación: {habitacion.tipo}")
    print(f"Tipo de estadia: {estadia.tipo_estadia}")
    print(f"Hora de ingreso: {estadia.hora_ingreso}")
    print(f"Hora de Retiro: {hora_retiro}")
    print(f"\nHospedaje: ${hospedaje:.2f}")
    print(f"Recargo: ${recargo:.2f}")
    print(f"Servicios: ${servicios:.2f}")
    print(f"\nTOTAL A PAGAR: ${total:.2f}")

    pago = 0
    while pago < total:
        try:
            pago = float(input("Monto recibido: $"))
            if pago < total:
                print("El pago es insuficente.")
        except ValueError:
            print("Debe ingresar un monto válido.")

    cambio = pago - total
    print(f"\nPago recibido: ${pago:.2f}")
    print(f"Cambio: ${cambio:.2f}")

    habitacion.estadia = None
    hostal.ingresos_dia += total

    print("\nLa habitación fue liberada")
    print("--- CHECK-OUT ---")