#!/usr/bin/env python3

# Procesa un archivo CSV y lo convierte en una base de datos SQLite
# Autor: Pedro Blanco (usando Codeium)

import os
import sys
import csv
import time
import sqlite3
import argparse

# Define los argumentos de entrada
parser = argparse.ArgumentParser(description=f'{sys.argv[0]}: Procesa un archivo CSV y lo convierte en una base de datos SQLite', add_help=False)
parser.add_argument('archivo_csv', help='Nombre del archivo CSV a procesar')
parser.add_argument('-h', '--help', action='help', help='Muestra esta ayuda y sale')
parser.add_argument('--db_name', help='Nombre del archivo de base de datos SQLite a generar (por defecto, se genera a partir del nombre del archivo CSV)')
parser.add_argument('-f', '--force', action='store_true', help='Reescribe el archivo de base de datos si ya existe')
parser.add_argument('-c','--chunksize', default=50, type=int, help='Número de filas a procesar por parte, recomendable en caso de archivos grandes (50 por defecto)')
parser.add_argument('-p','--progress', action='store_true', help='Muestra el progreso de la inserción de filas')
parser.add_argument('-v','--verbose',  action='store_true', help='Muestra información de todo el proceso')

args = parser.parse_args()

# Inicia el cronometro
start_time = time.time()

if args.verbose:
    args.progress = True

# Obtiene el nombre del archivo CSV y el nombre del archivo de base de datos SQLite
csv_file = args.archivo_csv

if args.verbose:
    print (f"[VERBOSE] Archivo CSV: {csv_file}")
    print (f"[VERBOSE] Chunksize (número de filas a procesar por parte): {args.chunksize}")

# Genera el nombre del archivo de base de datos a partir del nombre del archivo CSV
db_file = args.db_name or f'{args.archivo_csv[:-4]}.db'

if args.verbose:
    print (f"[VERBOSE] Archivo de base de datos: {db_file}")
    
# Verifica si el archivo de base de datos ya existe y si se debe reescribir
if os.path.exists(db_file):
    if args.force:
        os.remove(db_file)
        if args.verbose:
            print(f'[VERBOSE] El archivo existente de base de datos {db_file} ha sido eliminado (se ha usado la opción --force).')
    else:
        print(f'[ERROR] El archivo de base de datos {db_file} ya existe. Use --force para reescribirlo.')
        sys.exit(1)

# Conecta a la base de datos SQLite
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Abre el archivo CSV
with open(args.archivo_csv, 'r', buffering=1024*1024,encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"',doublequote=True)
    cabecera = next(reader)
    num_columns = len(cabecera)
    
    if args.verbose:
        print(f"[VERBOSE] Número de campos: {len(cabecera)}")
        print(f"[VERBOSE] Campos: {cabecera}")
    
    # Crea la tabla en la base de datos
    definicion_tabla = '''
        CREATE TABLE IF NOT EXISTS mi_tabla (
            id INTEGER PRIMARY KEY,
            {}
        )
    '''.format(', '.join([f'"{campo}" TEXT' for campo in cabecera]))
    
    cursor.execute( definicion_tabla )
    
    if args.verbose:
        sys.stdout.write ( f'[VERBOSE] Creando tabla en la base de datos: {definicion_tabla}' )
    
    if args.progress:
        sys.stdout.write ( f'[INFO] Insertando filas (de {args.chunksize} en {args.chunksize}) en la base de datos: _' )
    else:
        sys.stdout.write ( f'[INFO] Insertando filas (de {args.chunksize} en {args.chunksize}) en la base de datos (use --progress para mostrar el progreso): _' )
    sys.stdout.flush()

    # Procesa el archivo CSV por partes
    chunk = []
    num_lines = 0
    caracter_progreso = ['/', '-', '\\', '|']

    for fila in reader:
        chunk.append(fila)
        if len(chunk) >= args.chunksize:
            # Inserta los datos en la base de datos
            cursor.executemany('INSERT INTO mi_tabla VALUES (NULL, {})'.format(', '.join(['?'] * num_columns)), chunk)
            num_lines += len(chunk)
            if args.progress:
                sys.stdout.write('\b' + caracter_progreso[num_lines % 4] )
                # print ( '+', end='' )
                sys.stdout.flush()
            chunk = []

    # Inserta los datos restantes en la base de datos
    if chunk:
        cursor.executemany('INSERT INTO mi_tabla VALUES (NULL, {})'.format(', '.join(['?'] * num_columns)), chunk)
        num_lines += len(chunk)
        if args.progress:
            print ( '\b+' )
        print ( f'[INFO] Se han insertado {num_lines} filas en la base de datos.' )

# Detiene el cronometro
end_time = time.time()

# Imprime el tiempo de ejecución
if args.progress:
    print (f'[INFO] Tiempo de ejecución: {end_time - start_time:.2f} segundos')

# Cierra la conexión a la base de datos
conn.commit()
conn.close()
