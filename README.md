# CSV2SQLite

Script para procesar un archivo CSV de gran tamaño en una base de datos SQLite.

## Introducción

El script `procesar_csv.py` es una herramienta diseñada para procesar un archivo CSV y convertirlo en una base de datos SQLite.

Supongamos que tenemos un archivo CSV con muchas columnas y muchas filas (y con celdas muy grandes). Por su tamaño, al  intentar abrir el archivo con LibreOffice Calc o Excel, nos quedamos sin memoria o se paraliza el sistema. Este script nos permite procesar este archivo CSV y convertirlo en datos que se insertarán en una base de datos en formato SQLite, que podremos usar para interactuar con los datos más fácilmente que con LibreOffice Calc o Excel. 

A continuación, se explica cómo utilizar este script de manera efectiva.

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

Podemos ejecutar el script de la siguiente manera:
```bash
python procesar_csv.py --db_name datos_en_sqlite.db datos.csv
```
Esto procesará el archivo `datos.csv` y generará un nuevo archivo llamado `datos_en_sqlite.db` que se puede usar para interactuar con la base de datos.

### Limitar número de líneas

Para limitar el número de filas que se procesan por parte, puedes utilizar el parámetro `--chunksize`, en este caso con un valor de 10:

```bash
python procesar_csv.py --db_name datos_en_sqlite.db --chunksize 10 datos.csv
```

## Notas Adicionales

- Asegúrese de que el archivo CSV esté en el mismo directorio que el script, o especifique la ruta completa al archivo.
- Se creará un nuevo archivo de base de datos, eliminando el archivo existente si se especifica la opción `--force`.
- En la base de datos, se creará una única tabla con una primera columna `id` que será la clave primaria de la tabla y a continuación una columna por cada columna del archivo CSV; su tipo de dato será `TEXT` y su nombre de columna será el mismo de la columna del archivo CSV (incluyendo espacios). 