# ProcesarCSV_Falcon: `procesar_csv.py`

Script para procesar un archivo CSV de gran tamaño en una base de datos SQLite.

## Introducción

El script `procesar_csv.py` es una herramienta diseñada para procesar un archivo CSV y convertirlo en una base de datos SQLite. A continuación, se explica cómo utilizar este script de manera efectiva.

## Requisitos Previos

- Python 3.x instalado en el sistema.
  - Ver archivo `requirements.txt` para ver los paquetes necesarios para el script.
- Archivo CSV que se desea procesar.

## Ejecución del Script

Para ejecutar el script, simplemente ejecute el comando siguiente en la terminal:
```bash
python procesar_csv.py [opciones] archivo_csv
```

## Opciones y Parámetros

El script admite las siguientes opciones y parámetros:

```bash
usage: procesar_csv.py [-h] [--db_name DB_NAME] [-f] [-c CHUNKSIZE] [-p] [-v] archivo_csv

.\procesar_csv.py: Procesa un archivo CSV y lo convierte en una base de datos SQLite

positional arguments:
  archivo_csv           Nombre del archivo CSV a procesar

options:
  -h, --help            Muestra esta ayuda y sale
  --db_name DB_NAME     Nombre del archivo de base de datos SQLite a generar (por defecto, se genera a partir del nombre del archivo CSV)
  -f, --force           Reescribe el archivo de base de datos si ya existe
  -c CHUNKSIZE, --chunksize CHUNKSIZE
                        Número de filas a procesar por parte, recomendable en caso de archivos grandes (50 por defecto)
  -p, --progress        Muestra el progreso de la inserción de filas
  -v, --verbose         Muestra información de todo el proceso
```
## Ejemplo de Uso

Supongamos que tenemos un archivo CSV llamado `datos.csv` que contiene información sobre clientes, y deseamos procesar esta información para obtener una base de datos en formato SQLite. Podemos ejecutar el script de la siguiente manera:
```bash
python procesar_csv.py --db_name datos_en_sqlite.db datos.csv
```
Esto procesará el archivo `datos.csv` y generará un nuevo archivo llamado `datos_en_sqlite.db` que se puede usar para interactuar con la base de datos.

## Notas Adicionales

- Asegúrese de que el archivo CSV esté en el mismo directorio que el script, o especifique la ruta completa al archivo.
- Se creará un nuevo archivo de base de datos, eliminando el archivo existente si se especifica la opción `--force`.
 