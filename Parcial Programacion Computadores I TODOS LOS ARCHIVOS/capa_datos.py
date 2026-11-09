# ============================================================
# CAPA DE DATOS (persistencia)
# Inventario Forestal Nacional - IDEAM
# Unica capa que lee y escribe los archivos de texto plano.
# Formato: un registro por linea, campos separados por "|".
# ============================================================

CARPETA = "datos/"
SEPARADOR = "|"

ARCH_CONGLOMERADOS = CARPETA + "conglomerados.txt"
ARCH_BRIGADAS = CARPETA + "brigadas.txt"
ARCH_INTEGRANTES = CARPETA + "integrantes.txt"
ARCH_INSPECCIONES = CARPETA + "inspecciones.txt"
ARCH_CONTEOS = CARPETA + "conteos.txt"
ARCH_MUESTRAS = CARPETA + "muestras.txt"


def leer_registros(ruta):
    """Lee un archivo y retorna una lista de registros (lista de campos)."""
    registros = []
    archivo = open(ruta, "r", encoding="utf-8")
    for linea in archivo:
        linea = linea.strip()
        if linea != "":
            registros.append(linea.split(SEPARADOR))
    archivo.close()
    return registros


def agregar_registro(ruta, campos):
    """Agrega un registro (lista de campos) al final del archivo."""
    archivo = open(ruta, "a", encoding="utf-8")
    archivo.write(SEPARADOR.join(campos) + "\n")
    archivo.close()


# ---------- Lectura de cada entidad (lista de diccionarios) ----------

def cargar_conglomerados():
    lista = []
    for r in leer_registros(ARCH_CONGLOMERADOS):
        lista.append({"codigo": r[0], "departamento": r[1], "municipio": r[2],
                      "latitud": float(r[3]), "longitud": float(r[4]),
                      "area_ha": float(r[5])})
    return lista


def cargar_brigadas():
    lista = []
    for r in leer_registros(ARCH_BRIGADAS):
        lista.append({"codigo": r[0], "nombre": r[1], "lider": r[2]})
    return lista


def cargar_integrantes():
    lista = []
    for r in leer_registros(ARCH_INTEGRANTES):
        lista.append({"brigada": r[0], "nombre": r[1], "rol": r[2]})
    return lista


def cargar_inspecciones():
    lista = []
    for r in leer_registros(ARCH_INSPECCIONES):
        lista.append({"codigo": r[0], "fecha": r[1],
                      "conglomerado": r[2], "brigada": r[3]})
    return lista


def cargar_conteos():
    lista = []
    for r in leer_registros(ARCH_CONTEOS):
        lista.append({"inspeccion": r[0], "subparcela": int(r[1]),
                      "fustales": int(r[2]), "latizales": int(r[3]),
                      "brinzales": int(r[4])})
    return lista


def cargar_muestras():
    lista = []
    for r in leer_registros(ARCH_MUESTRAS):
        lista.append({"codigo": r[0], "inspeccion": r[1],
                      "nombre_comun": r[2], "uso": r[3],
                      "nombre_cientifico": r[4]})
    return lista


# ---------- Escritura de cada entidad ----------

def guardar_inspeccion(insp):
    agregar_registro(ARCH_INSPECCIONES,
                     [insp["codigo"], insp["fecha"],
                      insp["conglomerado"], insp["brigada"]])


def guardar_conteo(c):
    agregar_registro(ARCH_CONTEOS,
                     [c["inspeccion"], str(c["subparcela"]),
                      str(c["fustales"]), str(c["latizales"]),
                      str(c["brinzales"])])


def guardar_muestra(m):
    agregar_registro(ARCH_MUESTRAS,
                     [m["codigo"], m["inspeccion"], m["nombre_comun"],
                      m["uso"], m["nombre_cientifico"]])
