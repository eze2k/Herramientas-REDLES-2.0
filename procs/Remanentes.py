import pandas as pd
import glob
from procs.console import console
import shutil


def run():
    try:
        rem = glob.glob("*Remanentes*")
        # Lee el archivo Excel
        archivo = pd.read_excel(rem[0], sheet_name=None)
        if len(archivo) == 0:
            console.log("No se ecnontro ningun remanente.")
            input("[Presione ENTER para continuar.]")
            return 0
        lista_datos = (
            []
        )  # Crea una lista vacía para almacenar los datos que cumplan las condiciones

        # Itera sobre cada hoja del archivo
        for nombre_hoja, df in archivo.items():
            # Recorre cada fila del DataFrame y verifica si la segunda columna contiene 'c', 'cc', o 'ccc'
            for i, fila in df.iterrows():
                if fila[1] in ["C", "CC", "CCC", "c", "cc", "ccc"]:
                    # Si la condición se cumple, agrega el dato de la sexta columna a la lista
                    lista_datos.append((fila[5]))

        # Guarda los resultados en un archivo de texto
        with open("out//dnis para reenviar.txt", "w") as archivo_texto:
            for dato in lista_datos:
                archivo_texto.write(str(dato) + "\n")
        shutil.move(rem[0], "in")
        console.log("Se efectuo la limpieza/combinacion con exito.")
        input("[Presione ENTER para continuar.]")
    except Exception as e:
        console.log(f"Error: {e}")
        input("[Presione ENTER para continuar.]")
    return 0
