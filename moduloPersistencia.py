#Persistencia
import json
import os
from datetime import date
from moduloClases import Cliente, Estadia

# El archivo se crea junto a este modulo, sin importar desde donde se ejecute el programa
ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hostal_datos.json")


def guardar_estado(hostal):
    """Convierte el estado del hostal a un diccionario y lo escribe en JSON."""
    datos = {
        "fecha": date.today().isoformat(),
        "huespedes_dia": hostal.huespedes_dia,
        "ingresos_dia": hostal.ingresos_dia,
        "habitaciones": {},
    }
    for hab in hostal.habitaciones:
        est = hab.estadia
        if est is None:
            continue
        datos["habitaciones"][str(hab.numero)] = {
            "nombre": est.cliente.nombre,
            "documento": est.cliente.documento,
            "tipo_estadia": est.tipo_estadia,
            "hora_ingreso": est.hora_ingreso,
            "noches": est.noches,
            "servicios": [
                {"nombre": s.nombre, "cantidad": s.cantidad, "precio": s.precio}
                for s in est.servicios
            ],
        }
    # Se escribe a un archivo temporal y luego se reemplaza,
    # asi el archivo real nunca queda a medias si el programa se cierra al guardar.
    temporal = ARCHIVO + ".tmp"
    with open(temporal, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    os.replace(temporal, ARCHIVO)


def cargar_estado(hostal):
    """Lee el JSON (si existe) y reconstruye las estadias en el hostal."""
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        return  # primera ejecucion: no hay nada que cargar
    except (json.JSONDecodeError, OSError):
        print("No se pudo leer el archivo de datos. Se inicia vacio.")
        return

    # Los contadores "del dia" solo se conservan si el archivo es de hoy
    if datos.get("fecha") == date.today().isoformat():
        hostal.huespedes_dia = datos.get("huespedes_dia", 0)
        hostal.ingresos_dia = datos.get("ingresos_dia", 0)

    for numero, d in datos.get("habitaciones", {}).items():
        try:
            hab = hostal.buscar_habitacion(int(numero))
            if hab is None:
                continue
            cliente = Cliente(d["nombre"], d["documento"])
            est = Estadia(cliente, hab.tipo, d["tipo_estadia"], d["hora_ingreso"], d["noches"])
            for s in d["servicios"]:
                est.agregar_servicio(s["nombre"], s["precio"], s["cantidad"])
            hab.estadia = est
        except (KeyError, ValueError):
            print(f"No se pudo cargar la habitacion {numero}; se omite.")