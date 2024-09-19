#!/usr/bin/env python3

# Procesa un archivo CSV y lo convierte en una base de datos SQLite
# Autor: Pedro Blanco (usando Codeium)

import csv
import sqlite3
import argparse

# Define los argumentos de entrada
parser = argparse.ArgumentParser(description='Procesa un archivo CSV y lo convierte en una base de datos SQLite')
parser.add_argument('archivo_csv', help='Nombre del archivo CSV a procesar')
parser.add_argument('--db_nombre', default='mi_base_de_datos.db', help='Nombre de la base de datos SQLite')
parser.add_argument('--chunksize', default=1000, type=int, help='Número de filas a procesar por parte')

args = parser.parse_args()

# Conecta a la base de datos SQLite
conn = sqlite3.connect(args.db_nombre)
cursor = conn.cursor()

# Crea la tabla en la base de datos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mi_tabla (
        id INTEGER PRIMARY KEY,
        {}
    )
'''.format(', '.join(['columna{} TEXT'.format(i) for i in range(1, 61)])))

# Abre el archivo CSV
with open(args.archivo_csv, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Salta la primera fila (encabezados)

    # Procesa el archivo CSV por partes
    chunk = []
    for fila in reader:
        chunk.append(fila)
        if len(chunk) >= args.chunksize:
            # Inserta los datos en la base de datos
            cursor.executemany('INSERT INTO mi_tabla VALUES (NULL, {})'.format(', '.join(['?'] * 60)), chunk)
            chunk = []

    # Inserta los datos restantes en la base de datos
    if chunk:
        cursor.executemany('INSERT INTO mi_tabla VALUES (NULL, {})'.format(', '.join(['?'] * 60)), chunk)

# Cierra la conexión a la base de datos
conn.commit()
conn.close()
