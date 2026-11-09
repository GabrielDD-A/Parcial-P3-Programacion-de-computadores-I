# ============================================================
# CAPA DE PRESENTACION (interfaz de consola)
# Solo lee del teclado e imprime. Toda decision de negocio
# se delega a capa_logica. Nunca accede a los archivos.
# ============================================================

import capa_logica


def linea():
    print("-" * 60)


def leer_texto(mensaje):
    """Lee un texto que no puede quedar vacio."""
    texto = input(mensaje).strip()
    while texto == "":
        print("  ! El dato no puede estar vacio.")
        texto = input(mensaje).strip()
    return texto


def leer_entero(mensaje):
    """Lee un entero no negativo."""
    texto = input(mensaje).strip()
    while not capa_logica.es_entero_no_negativo(texto):
        print("  ! Debe ingresar un numero entero mayor o igual a 0.")
        texto = input(mensaje).strip()
    return int(texto)


def mostrar_menu():
    linea()
    print("   INVENTARIO FORESTAL NACIONAL - IDEAM")
    linea()
    print("1. Listar inspecciones")
    print("2. Consultar una inspeccion")
    print("3. Registrar nueva inspeccion")
    print("4. Especies por departamento")
    print("5. Salir")


# ---------------- Opcion 1 ----------------

def opcion_listar():
    inspecciones = capa_logica.listar_inspecciones()
    linea()
    if len(inspecciones) == 0:
        print("No hay inspecciones registradas.")
    else:
        print("CODIGO  FECHA        CONGLOMERADO  BRIGADA")
        for i in inspecciones:
            print(i["codigo"].ljust(8) + i["fecha"].ljust(13) +
                  i["conglomerado"].ljust(14) + i["brigada"])


# ---------------- Opcion 2 ----------------

def opcion_consultar():
    codigo = leer_texto("Codigo de la inspeccion (ej. I001): ").upper()
    datos = capa_logica.consultar_inspeccion(codigo)
    if datos is None:
        print("  ! No existe una inspeccion con codigo " + codigo)
        return
    insp = datos["inspeccion"]
    cong = datos["conglomerado"]
    brig = datos["brigada"]
    linea()
    print("INSPECCION " + insp["codigo"] + "   Fecha: " + insp["fecha"])
    linea()
    print("[CONGLOMERADO]")
    if cong is None:
        print("  (conglomerado no encontrado)")
    else:
        print("  Codigo: " + cong["codigo"])
        print("  Ubicacion: " + cong["municipio"] + ", " + cong["departamento"])
        print("  Centroide: lat " + str(cong["latitud"]) +
              ", lon " + str(cong["longitud"]))
        print("  Area muestreada: " + str(cong["area_ha"]) + " ha")
    print("[BRIGADA]")
    if brig is None:
        print("  (brigada no encontrada)")
    else:
        print("  " + brig["codigo"] + " - " + brig["nombre"])
        for p in datos["integrantes"]:
            print("    * " + p["nombre"] + " (" + p["rol"] + ")")
    print("[CONTEO POR SUBPARCELA]")
    print("  SUBP  FUSTALES  LATIZALES  BRINZALES")
    for c in datos["conteos"]:
        print("  " + str(c["subparcela"]).ljust(6) + str(c["fustales"]).ljust(10) +
              str(c["latizales"]).ljust(11) + str(c["brinzales"]))
    t = datos["total"]
    print("  TOTAL " + str(t["fustales"]).ljust(10) + str(t["latizales"]).ljust(11) +
          str(t["brinzales"]))
    print("  Total de arboles: " + str(t["arboles"]))
    print("  Densidad de cobertura: " + str(datos["densidad"]) + " arboles/ha")
    print("[MUESTRAS]")
    if len(datos["muestras"]) == 0:
        print("  (sin muestras)")
    for m in datos["muestras"]:
        print("  " + m["codigo"] + "  " + m["nombre_comun"] + " - " +
              m["nombre_cientifico"] + " [" + m["uso"] + "]")


# ---------------- Opcion 3 ----------------

def opcion_registrar():
    fecha = leer_texto("Fecha (AAAA-MM-DD): ")
    while not capa_logica.es_fecha_valida(fecha):
        print("  ! Fecha invalida.")
        fecha = leer_texto("Fecha (AAAA-MM-DD): ")
    cong = leer_texto("Codigo del conglomerado: ").upper()
    while not capa_logica.existe_conglomerado(cong):
        print("  ! El conglomerado no existe.")
        cong = leer_texto("Codigo del conglomerado: ").upper()
    brig = leer_texto("Codigo de la brigada: ").upper()
    while not capa_logica.existe_brigada(brig):
        print("  ! La brigada no existe.")
        brig = leer_texto("Codigo de la brigada: ").upper()

    conteos = []
    for s in range(1, capa_logica.NUM_SUBPARCELAS + 1):
        print("Subparcela " + str(s) + ":")
        f = leer_entero("  Fustales: ")
        l = leer_entero("  Latizales: ")
        b = leer_entero("  Brinzales: ")
        conteos.append([f, l, b])

    muestras = []
    n = leer_entero("Cantidad de muestras a registrar: ")
    for k in range(n):
        print("Muestra " + str(k + 1) + ":")
        comun = leer_texto("  Nombre comun: ")
        uso = leer_texto("  Uso (Medicinal/Alimenticio/Maderable): ").capitalize()
        while not capa_logica.es_uso_valido(uso):
            print("  ! Uso invalido.")
            uso = leer_texto("  Uso (Medicinal/Alimenticio/Maderable): ").capitalize()
        cientifico = leer_texto("  Nombre cientifico (laboratorio): ")
        muestras.append([comun, uso, cientifico])

    resultado = capa_logica.registrar_inspeccion(fecha, cong, brig, conteos, muestras)
    if resultado[0]:
        print("Inspeccion registrada con codigo " + resultado[1])
    else:
        print("  ! Error: " + resultado[1])


# ---------------- Opcion 4 ----------------

def opcion_especies():
    depto = leer_texto("Departamento: ")
    especies = capa_logica.especies_por_departamento(depto)
    linea()
    if len(especies) == 0:
        print("No hay especies registradas en " + depto)
    else:
        print("Especies registradas en " + depto + ": " + str(len(especies)))
        for e in especies:
            print("  " + e["nombre_comun"] + " (" + e["nombre_cientifico"] + ") [" +
                  e["uso"] + "] - Municipios: " + ", ".join(e["municipios"]))


# ---------------- Ciclo principal ----------------

def iniciar():
    opcion = ""
    while opcion != "5":
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            opcion_listar()
        elif opcion == "2":
            opcion_consultar()
        elif opcion == "3":
            opcion_registrar()
        elif opcion == "4":
            opcion_especies()
        elif opcion == "5":
            print("Fin del programa.")
        else:
            print("  ! Opcion invalida.")
