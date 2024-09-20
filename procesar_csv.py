#!/usr/bin/env python3

# Procesa un archivo CSV y lo convierte en una base de datos SQLite
# Autor: Pedro Blanco (usando Codeium)

import os
import sys
import csv
import sqlite3
import argparse

# Define los argumentos de entrada
parser = argparse.ArgumentParser(description='Procesa un archivo CSV y lo convierte en una base de datos SQLite')
parser.add_argument('archivo_csv', help='Nombre del archivo CSV a procesar')
parser.add_argument('--db_name', help='Nombre del archivo de base de datos SQLite a generar (por defecto, se genera a partir del nombre del archivo CSV)')
parser.add_argument('-f', '--force', action='store_true', help='Reescribe el archivo de base de datos si ya existe')
parser.add_argument('--chunksize', default=1000, type=int, help='Número de filas a procesar por parte')
parser.add_argument('--progress', default=False, type=int, help='Muestra el progreso de la inserción de filas')

args = parser.parse_args()

# Obtiene el nombre del archivo CSV y el nombre del archivo de base de datos SQLite
csv_file = args.archivo_csv
# Genera el nombre del archivo de base de datos a partir del nombre del archivo CSV
db_file = args.db_name or f'{args.archivo_csv[:-4]}.db'

# Verifica si el archivo de base de datos ya existe y si se debe reescribir
if os.path.exists(db_file) and not args.force:
    print(f'El archivo de base de datos {db_file} ya existe. Use --force para reescribirlo.')
    sys.exit(1)

# Conecta a la base de datos SQLite
conn = sqlite3.connect(args.db_name)
cursor = conn.cursor()

# Abre el archivo CSV
with open(args.archivo_csv, 'r', buffering=1024*1024,encoding='utf-8') as csvfile:
    num_columns = 63

    # Crea la tabla en la base de datos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mi_tabla (
            id INTEGER PRIMARY KEY,
            {}
        )
    '''.format(', '.join(['columna{} TEXT'.format(i) for i in range(1, num_columns + 1)])))
    
    reader = csv.reader(csvfile, delimiter=',', quotechar='"',doublequote=True)
    next(reader)  # Salta la primera fila (encabezados)

    print ( f'Insertando filas (de {args.chunksize} en {args.chunksize}) en la base de datos (use --progress para mostrar el progreso): ' )
    # Procesa el archivo CSV por partes
    chunk = []
    num_lines = 0
    for fila in reader:
        chunk.append(fila)
        if len(chunk) >= args.chunksize:
            # Inserta los datos en la base de datos
            cursor.executemany('INSERT INTO mi_tabla VALUES (NULL, {})'.format(', '.join(['?'] * num_columns)), chunk)
            num_lines += len(chunk)
            if args.progress:
                print ( '+', end='' )
            chunk = []

    # Inserta los datos restantes en la base de datos
    if chunk:
        cursor.executemany('INSERT INTO mi_tabla VALUES (NULL, {})'.format(', '.join(['?'] * num_columns)), chunk)
        num_lines += len(chunk)
        if args.progress:
            print ( '+' )
        print ( f'Se han insertado {num_lines} filas en la base de datos.' )
        

# Cierra la conexión a la base de datos
conn.commit()
conn.close()
