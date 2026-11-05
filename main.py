def datos_leer(nombre):
    archivo = open(nombre, "r", encoding="utf-8")
    lineas = archivo.readlines()
    archivo.close()
    filas = []
    for linea in lineas:
        linea = linea.strip()
        if linea != "":
            filas.append(linea.split(";"))
    return filas


def logica_buscar_conglomerado(id_conglomerado):
    filas = datos_leer("conglomerados.txt")
    for fila in filas:
        if fila[0] == id_conglomerado:
            return fila
    return None


def logica_buscar_brigada(id_brigada):
    filas = datos_leer("brigadas.txt")
    for fila in filas:
        if fila[0] == id_brigada:
            return fila
    return None


def logica_buscar_conteo(id_conglomerado):
    filas = datos_leer("conteos.txt")
    for fila in filas:
        if fila[0] == id_conglomerado:
            return fila
    return None


def logica_buscar_muestras(id_conglomerado):
    filas = datos_leer("muestras.txt")
    resultado = []
    for fila in filas:
        if fila[0] == id_conglomerado:
            resultado.append(fila)
    return resultado


def logica_total_arboles(conteo):
    total = int(conteo[1]) + int(conteo[2]) + int(conteo[3])
    return total


def presentacion_menu():
    print("====================================")
    print("   INVENTARIO FORESTAL NACIONAL")
    print("====================================")
    print("1. Consultar inspeccion")
    print("2. Salir")


def presentacion_mostrar_inspeccion(id_conglomerado):
    conglomerado = logica_buscar_conglomerado(id_conglomerado)
    if conglomerado == None:
        print("No existe el conglomerado", id_conglomerado)
        return

    brigada = logica_buscar_brigada(conglomerado[5])
    conteo = logica_buscar_conteo(id_conglomerado)
    muestras = logica_buscar_muestras(id_conglomerado)

    print("")
    print("--- DATOS DEL CONGLOMERADO ---")
    print("Codigo:", conglomerado[0])
    print("Departamento:", conglomerado[1])
    print("Municipio:", conglomerado[2])
    print("Latitud:", conglomerado[3])
    print("Longitud:", conglomerado[4])

    print("")
    print("--- DATOS DE LA BRIGADA ---")
    print("Brigada:", brigada[0])
    print("Jefe de brigada:", brigada[1])
    print("Integrantes:", brigada[2])
    print("Coinvestigador local:", brigada[3])

    print("")
    print("--- CONTEO DE ARBOLES ---")
    print("Fustales:", conteo[1])
    print("Latizales:", conteo[2])
    print("Brinzales:", conteo[3])
    print("Total:", logica_total_arboles(conteo))

    print("")
    print("--- MUESTRAS ---")
    if len(muestras) == 0:
        print("Sin muestras registradas")
    for m in muestras:
        print(m[1], "|", m[2], "|", m[3], "|", m[4])
    print("")


opcion = ""
while opcion != "2":
    presentacion_menu()
    opcion = input("Elija una opcion: ")
    if opcion == "1":
        codigo = input("Codigo del conglomerado (ej: C001): ")
        presentacion_mostrar_inspeccion(codigo)
    elif opcion == "2":
        print("Hasta luego")
    else:
        print("Opcion no valida")
