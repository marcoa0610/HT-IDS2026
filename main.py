#Main

def mostrar_menu():
    print("===== HOSTAL TROPICANA =====")
    print("1. Check-in")
    print("2. Check-out")
    print("3. Ver estado de habitaciones")
    print("4. Servicios adicionales")
    print("5. Reporte diario")
    print("6. Salir")
    return input("Digite que opción quiere: ")


from moduloClases import Hostal
from moduloFunciones import check_in
from moduloFunciones import check_out
from moduloFunciones import reporteDiario

hostal = Hostal()
#Hola Alvin
while True:
    opcion = mostrar_menu()
    if opcion == "1":
        check_in(hostal)
    elif opcion == "2":
        check_out(hostal)
    elif opcion == "3":
        for habitacion in hostal.habitaciones:
            habitacion.mostrar_estado()
    elif opcion == "4":
        from moduloFunciones import gestionar_servicios
        gestionar_servicios(hostal)
    elif opcion == "5":
        reporteDiario(hostal)
    elif opcion == "6":
        print("Gracias por visitar Hostal Tropicana.")
        break
    else:
        print("Opcion invalida.")

