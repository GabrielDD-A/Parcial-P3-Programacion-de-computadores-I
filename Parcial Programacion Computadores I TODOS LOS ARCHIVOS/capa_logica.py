# ============================================================
# CAPA LOGICA (reglas de negocio)
# No lee teclado ni imprime: recibe datos, valida y calcula.
# Se comunica hacia abajo solo con capa_datos.
# ============================================================

import capa_datos

USOS_VALIDOS = ["Medicinal", "Alimenticio", "Maderable"]
NUM_SUBPARCELAS = 5


# ---------------- Busquedas ----------------

def buscar_por_codigo(lista, codigo):
    """Busqueda secuencial. Retorna el diccionario o None."""
    for elemento in lista:
        if elemento["codigo"] == codigo:
            return elemento
    return None


def filtrar_por_campo(lista, campo, valor):
    """Retorna los elementos cuyo campo es igual a valor."""
    resultado = []
    for elemento in lista:
        if elemento[campo] == valor:
            resultado.append(elemento)
    return resultado


# ---------------- Calculos ----------------

def totalizar_conteo(conteos):
    """Suma fustales, latizales y brinzales de todas las subparcelas."""
    total = {"fustales": 0, "latizales": 0, "brinzales": 0, "arboles": 0}
    for c in conteos:
        total["fustales"] = total["fustales"] + c["fustales"]
        total["latizales"] = total["latizales"] + c["latizales"]
        total["brinzales"] = total["brinzales"] + c["brinzales"]
    total["arboles"] = total["fustales"] + total["latizales"] + total["brinzales"]
    return total


def calcular_densidad(total_arboles, area_ha):
    """Densidad de cobertura = arboles / hectarea."""
    if area_ha <= 0:
        return 0.0
    return round(total_arboles / area_ha, 2)


# ---------------- Consultas ----------------

def listar_inspecciones():
    return capa_datos.cargar_inspecciones()


def consultar_inspeccion(codigo):
    """Arma la informacion completa de una inspeccion.
    Retorna un diccionario, o None si el codigo no existe."""
    inspeccion = buscar_por_codigo(capa_datos.cargar_inspecciones(), codigo)
    if inspeccion is None:
        return None
    conglomerado = buscar_por_codigo(capa_datos.cargar_conglomerados(),
                                     inspeccion["conglomerado"])
    brigada = buscar_por_codigo(capa_datos.cargar_brigadas(),
                                inspeccion["brigada"])
    integrantes = filtrar_por_campo(capa_datos.cargar_integrantes(),
                                    "brigada", inspeccion["brigada"])
    conteos = filtrar_por_campo(capa_datos.cargar_conteos(),
                                "inspeccion", codigo)
    muestras = filtrar_por_campo(capa_datos.cargar_muestras(),
                                 "inspeccion", codigo)
    total = totalizar_conteo(conteos)
    densidad = 0.0
    if conglomerado is not None:
        densidad = calcular_densidad(total["arboles"], conglomerado["area_ha"])
    return {"inspeccion": inspeccion, "conglomerado": conglomerado,
            "brigada": brigada, "integrantes": integrantes,
            "conteos": conteos, "total": total, "densidad": densidad,
            "muestras": muestras}


def especies_por_departamento(departamento):
    """Especies (sin repetir) registradas en un departamento,
    con su uso y los municipios donde se encontraron."""
    conglomerados = capa_datos.cargar_conglomerados()
    inspecciones = capa_datos.cargar_inspecciones()
    muestras = capa_datos.cargar_muestras()
    especies = []
    for m in muestras:
        insp = buscar_por_codigo(inspecciones, m["inspeccion"])
        if insp is not None:
            cong = buscar_por_codigo(conglomerados, insp["conglomerado"])
            if cong is not None and \
               cong["departamento"].lower() == departamento.lower():
                existente = None
                for e in especies:
                    if e["nombre_cientifico"] == m["nombre_cientifico"]:
                        existente = e
                if existente is None:
                    especies.append({"nombre_cientifico": m["nombre_cientifico"],
                                     "nombre_comun": m["nombre_comun"],
                                     "uso": m["uso"],
                                     "municipios": [cong["municipio"]]})
                elif cong["municipio"] not in existente["municipios"]:
                    existente["municipios"].append(cong["municipio"])
    return especies


# ---------------- Validaciones ----------------

def es_fecha_valida(fecha):
    """Formato AAAA-MM-DD con mes 1-12 y dia 1-31."""
    partes = fecha.split("-")
    if len(partes) != 3:
        return False
    if len(partes[0]) != 4 or len(partes[1]) != 2 or len(partes[2]) != 2:
        return False
    if not (partes[0].isdigit() and partes[1].isdigit() and partes[2].isdigit()):
        return False
    mes = int(partes[1])
    dia = int(partes[2])
    return 1 <= mes <= 12 and 1 <= dia <= 31


def es_entero_no_negativo(texto):
    return texto.isdigit()


def existe_conglomerado(codigo):
    return buscar_por_codigo(capa_datos.cargar_conglomerados(), codigo) is not None


def existe_brigada(codigo):
    return buscar_por_codigo(capa_datos.cargar_brigadas(), codigo) is not None


def es_uso_valido(uso):
    return uso in USOS_VALIDOS


# ---------------- Generacion de codigos ----------------

def siguiente_codigo(lista, prefijo, digitos):
    """Genera el siguiente codigo consecutivo: I001 -> I002."""
    mayor = 0
    for elemento in lista:
        numero = int(elemento["codigo"][len(prefijo):])
        if numero > mayor:
            mayor = numero
    return prefijo + str(mayor + 1).zfill(digitos)


# ---------------- Registro ----------------

def registrar_inspeccion(fecha, cod_conglomerado, cod_brigada, conteos, muestras):
    """Valida y guarda una inspeccion con su conteo y muestras.
    conteos: lista de [fustales, latizales, brinzales] por subparcela.
    muestras: lista de [nombre_comun, uso, nombre_cientifico].
    Retorna (True, codigo) o (False, mensaje_de_error)."""
    if not es_fecha_valida(fecha):
        return (False, "Fecha invalida (use AAAA-MM-DD).")
    if not existe_conglomerado(cod_conglomerado):
        return (False, "El conglomerado no existe.")
    if not existe_brigada(cod_brigada):
        return (False, "La brigada no existe.")
    if len(conteos) != NUM_SUBPARCELAS:
        return (False, "Se requieren 5 subparcelas.")

    codigo = siguiente_codigo(capa_datos.cargar_inspecciones(), "I", 3)
    capa_datos.guardar_inspeccion({"codigo": codigo, "fecha": fecha,
                                   "conglomerado": cod_conglomerado,
                                   "brigada": cod_brigada})
    subparcela = 1
    for c in conteos:
        capa_datos.guardar_conteo({"inspeccion": codigo, "subparcela": subparcela,
                                   "fustales": c[0], "latizales": c[1],
                                   "brinzales": c[2]})
        subparcela = subparcela + 1
    for m in muestras:
        cod_muestra = siguiente_codigo(capa_datos.cargar_muestras(), "M", 4)
        capa_datos.guardar_muestra({"codigo": cod_muestra, "inspeccion": codigo,
                                    "nombre_comun": m[0], "uso": m[1],
                                    "nombre_cientifico": m[2]})
    return (True, codigo)
