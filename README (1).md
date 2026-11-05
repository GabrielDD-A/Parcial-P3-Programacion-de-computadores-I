# Inventario Forestal Nacional

Parcial 3 - Programación I

## Integrantes

- Gabriel Diaz
- Paola Sanchez
- Saray Silva

## Descripción

Programa en Python para apoyar el Inventario Forestal Nacional (IFN) del IDEAM. Por ahora permite consultar una inspección: se ingresa el código de un conglomerado y el programa muestra los datos del conglomerado, de la brigada que lo visitó, el conteo de árboles y las muestras tomadas.

Este es un avance del trabajo, todavía no está terminado.

## Cómo ejecutarlo

1. Tener todos los archivos en la misma carpeta.
2. Abrir una terminal en esa carpeta.
3. Ejecutar:

```
python main.py
```

## Estructura

El programa está hecho en tres capas, todas en `main.py`:

- **Datos** (`datos_`): lee los archivos de texto.
- **Lógica** (`logica_`): busca la información y hace los cálculos.
- **Presentación** (`presentacion_`): menú y salida por consola.

## Archivos de datos

Cada línea es un registro y los campos van separados por `;`.

| Archivo | Contenido |
|---|---|
| `conglomerados.txt` | código, departamento, municipio, latitud, longitud, brigada |
| `brigadas.txt` | código, jefe, integrantes, coinvestigador local |
| `conteos.txt` | código del conglomerado, fustales, latizales, brinzales |
| `muestras.txt` | código del conglomerado, código de muestra, nombre común, uso, nombre científico |

## Lo que falta

- Registrar nuevas inspecciones
- Calcular la densidad de cobertura vegetal
- Validar mejor las entradas del usuario
