import sys
from App import logic
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as lt


def new_logic():
    return logic.new_logic()

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")

def load_data(control):
    """
    Carga los datos
    """
    # Realizar la carga de datos
    print("Seleccionando archivo de datos...")
    
    # Mostrar opciones de archivos
    print("\nArchivos disponibles:")
    print("1. deliverytime_20.csv  (~15,200 registros)")
    print("2. deliverytime_40.csv  (~30,400 registros)")  
    print("3. deliverytime_60.csv  (~45,600 registros)")
    print("4. deliverytime_80.csv  (~60,800 registros)")
    print("5. deliverytime_100.csv (~76,000 registros)")
    
    # Permitir selección del usuario
    while True:
        try:
            choice = input("Selecciona una opción (1-5): ").strip()
            
            files = {
                '1': 'Data/deliverytime_20.csv',
                '2': 'Data/deliverytime_40.csv',
                '3': 'Data/deliverytime_60.csv',
                '4': 'Data/deliverytime_80.csv', 
                '5': 'Data/deliverytime_100.csv'
            }
            
            if choice in files:
                filename = files[choice]
                break
            else:
                print("Opción inválida. Por favor selecciona 1-5.")
                
        except KeyboardInterrupt:
            print("\nOperación cancelada.")
            return control
    
    # Cargar los datos usando la función de logic
    updated_control = logic.load_data(control, filename)
    
    if updated_control:
        print("¡Datos cargados exitosamente!")
        return updated_control
    else:
        print("Error al cargar los datos.")
        return control


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    print("\n" + "="*80)
    print("REQUERIMIENTO 1: CAMINO SIMPLE ENTRE DOS UBICACIONES")
    print("="*80)
    print("Algoritmo utilizado: BFS (Breadth-First Search)")
    print("="*80)

    if input("\n¿Deseas ver algunos nodos disponibles como referencia? (s/n): ").strip().lower() == 's':
        show_sample_nodes_for_testing(control)

    origin_id = input("\nID del punto de origen: ").strip()
    dest_id = input("ID del punto de destino: ").strip()

    if not origin_id or not dest_id:
        print("Los IDs no pueden estar vacíos.")
        return
    if origin_id == dest_id:
        print("El origen y destino no pueden ser iguales.")
        return

    print(f"\nBuscando camino desde '{origin_id}' hasta '{dest_id}'...")
    try:
        result = logic.req_1(control, origin_id, dest_id)
        if mp.contains(result, 'error'):
            print(f"\nERROR: {mp.get(result, 'error')}")
            print(f"Tiempo de ejecución: {mp.get(result, 'execution_time'):.2f} ms")
            return

        print(f"\nTiempo de ejecución: {mp.get(result, 'execution_time'):.2f} ms")
        if not mp.get(result, 'path_exists'):
            print(f"\n{mp.get(result, 'message')}")
            return

        print("\n" + "="*80)
        print("CAMINO ENCONTRADO")
        print("="*80)
        print(f"Origen: {origin_id}")
        print(f"Destino: {dest_id}")
        print(f"Cantidad de puntos en el camino: {mp.get(result, 'path_length')}")
        print(f"Domiciliarios únicos en el camino: {mp.get(result, 'total_deliverers')}")
        print(f"Restaurantes en el camino: {mp.get(result, 'total_restaurants')}")
        print("\nSECUENCIA DEL CAMINO:\n" + "-" * 50)
        print(f"{'Paso':<5} {'ID del Nodo':<25} {'Coordenadas':<20}")
        print("-" * 50)

        for i in range(lt.size(mp.get(result, 'path_sequence'))):
            node_id = lt.get_element(mp.get(result, 'path_sequence'), i)
            print(f"{i+1:<5} {node_id:<25} ({node_id.replace('_', ', ')})")

        if mp.get(result, 'total_deliverers') > 0:
            print(f"\nDOMICILIARIOS EN EL CAMINO ({mp.get(result, 'total_deliverers')}):")
            print("-" * 40)
            for i, d in enumerate(lt.iterator(mp.get(result, 'deliverers')), 1):
                print(f"{d:<15}", end="\n" if i % 5 == 0 else "")
            print()
        else:
            print("\nNo se encontraron domiciliarios en el camino.")

        if mp.get(result, 'total_restaurants') > 0:
            print(f"\nRESTAURANTES EN EL CAMINO ({mp.get(result, 'total_restaurants')}):")
            print("-" * 70)
            print(f"{'No.':<3} {'ID del Restaurante':<25} {'Coordenadas':<20}")
            print("-" * 70)
            for i in range(lt.size(mp.get(result, 'restaurants'))):
                r = lt.get_element(mp.get(result, 'restaurants'), i)
                coords = f"({mp.get(r, 'latitude')}, {mp.get(r, 'longitude')})"
                print(f"{i+1:<3} {mp.get(r, 'id'):<25} {coords:<20}")
        else:
            print("\nNo se encontraron restaurantes en el camino.")

        print("\n" + "="*80)
        print("Búsqueda completada exitosamente")
        print("="*80)

    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        print("Por favor, verifica que los datos estén correctamente cargados.")

def show_sample_nodes_for_testing(control):
    print("\nNODOS DISPONIBLES PARA TESTING:")
    print("=" * 70)
    sample_nodes = logic.get_available_nodes_sample(control, 20)
    if lt.is_empty(sample_nodes):
        print("No se encontraron nodos en el grafo.")
        print("Asegúrate de haber cargado los datos primero (Opción 1 del menú).")
        print("=" * 70)
        return

    print(f"{'No.':<3} {'ID del Nodo':<30} {'Tipo':<12} {'Coordenadas':<25}")
    print("-" * 70)
    rest_count, deli_count = 0, 0
    for i in range(lt.size(sample_nodes)):
        node = lt.get_element(sample_nodes, i)
        node_id = mp.get(node, 'id')
        node_type = mp.get(node, 'type')
        coords = f"({mp.get(node, 'latitude')}, {mp.get(node, 'longitude')})"
        print(f"{i+1:<3} {node_id:<30} {node_type:<12} {coords:<25}")
        if node_type == 'restaurant': rest_count += 1
        else: deli_count += 1

    print("-" * 70)
    print(f"Total: {lt.size(sample_nodes)} nodos ({rest_count} restaurantes, {deli_count} destinos)")
    print("\nCopia y pega los IDs para probar el requerimiento.")
    print("=" * 70)
    
    
def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
