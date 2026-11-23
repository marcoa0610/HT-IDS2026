#Main
from moduloClases import Hostal
from moduloFunciones import check_in, check_out, reporteDiario, gestionar_servicios
from moduloPersistencia import guardar_estado, cargar_estado


def mostrar_menu():
    print("===== HOSTAL TROPICANA =====")
    print("1. Check-in")
    print("2. Check-out")
    print("3. Ver estado de habitaciones")
    print("4. Servicios adicionales")
    print("5. Reporte diario")
    print("6. Salir")
    return input("Digite que opción quiere: ")


hostal = Hostal()
cargar_estado(hostal)  # recupera lo guardado en la ultima ejecucion

while True:
    opcion = mostrar_menu()
    if opcion == "1":
        check_in(hostal)
        guardar_estado(hostal)
    elif opcion == "2":
        check_out(hostal)
        guardar_estado(hostal)
    elif opcion == "3":
        for habitacion in hostal.habitaciones:
            habitacion.mostrar_estado()
    elif opcion == "4":
        gestionar_servicios(hostal)
        guardar_estado(hostal)
    elif opcion == "5":
        reporteDiario(hostal)
    elif opcion == "6":
        guardar_estado(hostal)
        print("Gracias por visitar Hostal Tropicana.")
        break
    else:
        print("Opcion invalida.")