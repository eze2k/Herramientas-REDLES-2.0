import pandas as pd
from unidecode import unidecode
from procs.DictsAndLists1x import (
    provincias,
    somosoOS,
    paisesSOMOSO,
    somosoActividades,
    afipPAIS,
)
import numpy as np
import zipfile
import os
from procs.console import console

# import cchardet


def run():
    console.log("Procesando TADI")

    # detectamos la codificacion de los archivos
    # def detectar_codificacion(archivo):
    #     with open(archivo, "rb") as f:
    #         result = cchardet.detect(f.read())
    #     return result["encoding"]

    # cdp = detectar_codificacion("datos personales_data.csv")
    # try:
    #     cgf = detectar_codificacion("Detalle del grupo familiar_data.csv")
    # except Exception as E:
    #     pass
    cdp = "ansi"
    cgf = "ansi"
    try:
        # Cargar los datos de los postulantes y adherentes
        postulante_df = pd.read_csv(
            "datos personales_data.csv", dtype=str, delimiter=";", encoding=cdp
        )
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV: {e}")

        # Obtén el número de la línea defectuosa
        line_number = int(str(e).split(" ")[-1])

        # Lee solo la línea defectuosa
        with open("datos personales_data.csv", "r", encoding=cdp) as file:
            lines = file.readlines()
            defective_line = lines[
                line_number - 1
            ]  # Resta 1 porque las listas en Python son de base 0

        # Guarda la línea defectuosa en un nuevo archivo CSV
        with open("defective_line.csv", "w", encoding=cdp) as output_file:
            output_file.write(defective_line)
        console.log(
            "Error parseando datos, revisar 'defective_line.csv' para saber que linea fue."
        )
        input("Presione una tecla para continuar.")
        return 0

    try:
        adherente_df = pd.read_csv(
            "Detalle del grupo familiar_data.csv",
            dtype=str,
            delimiter=";",
            encoding=cgf,
        )
        adhpass = 1

    except Exception as E:
        # Definir las columnas
        columnas = [
            "Fecha de caratulación EE",
            "Número de EE",
            "Numero de Formulario GEDO",
            "CUIT; CUIL o CDI",
            "Tipo",
            "Tipo de documento(ADHERENTE)",
            "Número de Documento(ADHERENTE)",
            "Apellido(ADHERENTE)",
            "Nombre(ADHERENTE)",
            "Parentesco(ADHERENTE)",
            "Sexo(ADHERENTE)",
            "Fecha de Nacimiento(ADHERENTE)",
        ]
        print(
            "Se armo un adherentes vacio, si hay adherentes que cargar, esto es un error, verificar y emepzar de nuevo."
        )
        # Crear un DataFrame vacío con las columnas
        adherente_df = pd.DataFrame(columns=columnas)

    # Verificar coincidencias
    # print(postulante_df.columns)
    # print(adherente_df.columns)
    merged_df = pd.merge(
        postulante_df,
        adherente_df,
        left_on=postulante_df.columns[1],
        right_on=adherente_df.columns[1],
        how="inner",
    )

    if len(merged_df) > 0:
        adh = True
    else:
        adh = False

    postulante_df = postulante_df.apply(
        lambda x: x.str.upper() if x.dtype == "object" else x
    )
    adherente_df = adherente_df.apply(
        lambda x: x.str.upper() if x.dtype == "object" else x
    )

    # Obtener la lista de columnas
    columnas = postulante_df.columns
    columnasADH = adherente_df.columns

    # Iterar sobre cada columna y aplicar unidecode
    for columna in columnas:
        postulante_df[columna] = postulante_df[columna].apply(
            lambda x: unidecode(str(x)) if pd.notnull(x) else x
        )

    for columna in columnasADH:
        adherente_df[columna] = adherente_df[columna].apply(
            lambda x: unidecode(str(x)) if pd.notnull(x) else x
        )

    # Crear tres nuevas columnas con los valores extraídos
    postulante_df[
        ["Año de Expediente", "Numero de Exp", "Dependencia"]
    ] = postulante_df["Número de EE"].str.extract(r"-(\d{4})-(\d+)-(\S+)$")

    postulante_df = postulante_df.replace("SIN INFORMACION", np.nan)
    postulante_df = postulante_df.replace("s/n", np.nan)
    adherente_df = adherente_df.replace("SIN INFORMACION", np.nan)
    adherente_df = adherente_df.replace("s/n", np.nan)

    # Llenar celdas vacías en 'Código de Actividad' con valores de 'Código de Actividad(alternativo)'
    postulante_df["Código de Actividad"].fillna(
        postulante_df["Código de Actividad(alternativo)"], inplace=True
    )
    postulante_df = postulante_df.drop(columns=["Código de Actividad(alternativo)"])

    # arreglamos nombres largos
    postulante_df["Denominación Cooperativa"] = (
        postulante_df["Denominación Cooperativa"].astype(str).str[:49]
    )
    postulante_df["Denominación Proyecto Productivo"] = (
        postulante_df["Denominación Proyecto Productivo"].astype(str).str[:49]
    )
    ######################################
    # Fijar el año máximo a 2024
    ano_maximo_rompido = 2024

    # Función para corregir los años en el formato de fecha en un DataFrame
    def corregir_anos(df, columna, ano_maximo):
        for i, fecha_str in enumerate(df[columna]):
            if pd.notna(fecha_str) and isinstance(
                fecha_str, str
            ):  # Verificar que la fecha no sea nula y sea una cadena
                # Intentar convertir la fecha utilizando pd.to_datetime
                try:
                    fecha = pd.to_datetime(fecha_str, format="%d/%m/%Y")
                except pd.errors.OutOfBoundsDatetime:
                    # Si ocurre un error de OutOfBoundsDatetime, establecer la fecha como "1/1/2000"
                    df.at[i, columna] = "1/1/2000"
                    continue

                # Corregir años mayores a 2024 y años con menos de 4 cifras
                if (
                    fecha.year > ano_maximo
                    or fecha.year < 1930
                    or len(str(fecha.year)) < 4
                ):
                    df.at[i, columna] = "1/1/2000"

    # Corregir los años en los DataFrames
    corregir_anos(postulante_df, "Fecha de Nacimiento", ano_maximo_rompido)
    corregir_anos(adherente_df, "Fecha de Nacimiento(ADHERENTE)", ano_maximo_rompido)

    console.log("Arreglando fechas")

    # Removemos cualqueir informacion despues de la fecha,como horarios
    postulante_df["Fecha de caratulación EE"] = (
        postulante_df["Fecha de caratulación EE"].str.split().str[0]
    )
    postulante_df["Vencimiento del CERMI"] = postulante_df[
        "Vencimiento del CERMI"
    ].apply(lambda x: x.split()[0] if pd.notnull(x) else x)

    adherente_df["Fecha de caratulación EE"] = (
        adherente_df["Fecha de caratulación EE"].str.split().str[0]
    )
    postulante_df["Fecha de Nacimiento"] = (
        postulante_df["Fecha de Nacimiento"].str.split().str[0]
    )
    adherente_df["Fecha de Nacimiento(ADHERENTE)"] = (
        adherente_df["Fecha de Nacimiento(ADHERENTE)"].str.split().str[0]
    )

    # # Convertir las columnas de fecha al formato correcto
    postulante_df["Fecha de caratulación EE"] = pd.to_datetime(
        postulante_df["Fecha de caratulación EE"],
        format="%d/%m/%Y",  # Usa el formato correcto para tu fecha
    ).dt.strftime("%d/%m/%Y")

    postulante_df["Fecha de Nacimiento"] = pd.to_datetime(
        postulante_df["Fecha de Nacimiento"],
        format="%d/%m/%Y",
    ).dt.strftime("%d/%m/%Y")

    adherente_df["Fecha de Nacimiento(ADHERENTE)"] = pd.to_datetime(
        adherente_df["Fecha de Nacimiento(ADHERENTE)"],
        format="%d/%m/%Y",
    ).dt.strftime("%d/%m/%Y")

    postulante_df["Vencimiento del CERMI"] = pd.to_datetime(
        postulante_df["Vencimiento del CERMI"],
        format="%d/%m/%Y",
    ).dt.strftime("%d/%m/%Y")

    postulante_df = postulante_df.sort_values(
        by="Fecha de caratulación EE", ascending=True
    )

    # Assuming df is your DataFrame and you want to change 'old_column_name' to 'new_column_name'
    postulante_df = postulante_df.rename(columns={"CUIT persona en TAD": "CUIT"})
    adherente_df = adherente_df.rename(columns={"CUIT; CUIL o CDI": "CUIT"})

    postulante_df = postulante_df.drop(columns=["CUIT; CUIL o CDI"])

    # Función para ajustar los valores
    def ajustar_valor(valor):
        if len(valor) == 11:
            return valor[2:-1]
        else:
            return valor

    # Aplicar la función a la columna
    postulante_df["Nº Documento"] = postulante_df["Nº Documento"].apply(ajustar_valor)

    adherente_df["Número de Documento(ADHERENTE)"] = (
        adherente_df["Número de Documento(ADHERENTE)"]
        .astype(str)
        .apply(lambda x: x[:8] if len(x) >= 9 else x)
    )
    console.log("Arreglando Nombres y apellidos")
    # Remover espacios en blanco al principio y al final de nombres y apellidos, tambien espacios dobles en blanco
    postulante_df["Nombre"] = (
        postulante_df["Nombre"].str.strip().str.replace(r"\s+", " ", regex=True)
    )
    postulante_df["Apellido"] = (
        postulante_df["Apellido"].str.strip().str.replace(r"\s+", " ", regex=True)
    )
    adherente_df["Nombre(ADHERENTE)"] = (
        adherente_df["Nombre(ADHERENTE)"]
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    adherente_df["Apellido(ADHERENTE)"] = (
        adherente_df["Apellido(ADHERENTE)"]
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    console.log("Arreglando Actividades y OS")
    # Limpiamos la actividad y la obra social
    postulante_df["Código de Actividad"] = postulante_df[
        "Código de Actividad"
    ].str.extract(r"(\d+)")
    postulante_df["Obra social elegida"] = postulante_df[
        "Obra social elegida"
    ].str.extract(r"(\d+)")
    console.log("Arreglando Codificaciones")
    # Codificamos
    adherente_df["Tipo"] = adherente_df["Tipo"].replace(
        {"ALTA": "1", "MODIFICACION": "2", "BAJA": "3"}
    )
    postulante_df["Provincia"] = postulante_df["Provincia"].replace(provincias)
    postulante_df["País de Origen"] = postulante_df["País de Origen"].replace(afipPAIS)
    postulante_df["País de Origen"] = postulante_df["País de Origen"].replace(
        {"REPUBLICA DOMINICANA": "209"}
    )

    # Reemplazar varlores para que sean compatibles con las tablas SOMOSO
    postulante_df["Tipo de Trámite"] = postulante_df["Tipo de Trámite"].replace(
        {"ALTA": "1", "MODIFICACION": "2", "BAJA": "3"}
    )
    postulante_df["Tipo Documento"] = postulante_df["Tipo Documento"].replace(
        {
            "CI - CEDULA DE IDENTIDAD": "96",
            "CU - CUIT": "96",
            "DU - DOCUMENTO UNICO": "96",
            "LC - LIBRETA CIVICA": "96",
            "LE - LIBRETA DE ENROLAMIENTO": "96",
            "OT - OTROS": "96",
            "PA - PASAPORTE": "96",
        }
    )

    postulante_df["Género"] = postulante_df["Género"].replace(
        {
            "MUJER": "1",
            "VARON": "2",
            "TRAVESTI": "4",
            "TRANSGENERO": "5",
            "TRANSEXUAL": "5",
            "MUJER TRANS": "6",
            "VARON TRANS": "7",
            "OTRO": "9",
        }
    )

    adherente_df["Tipo de documento(ADHERENTE)"] = adherente_df[
        "Tipo de documento(ADHERENTE)"
    ].replace(
        {
            "CI - CEDULA DE IDENTIDAD": "96",
            "CU - CUIT": "96",
            "DU - DOCUMENTO UNICO": "96",
            "LC - LIBRETA CIVICA": "96",
            "LE - LIBRETA DE ENROLAMIENTO": "96",
            "OT - OTROS": "96",
            "PA - PASAPORTE": "96",
        }
    )

    # arreglo parentescos
    adherente_df["Parentesco(ADHERENTE)"] = adherente_df["Parentesco(ADHERENTE)"].apply(
        lambda x: "3"
        if isinstance(x, str) and x.startswith("H")
        else "2"
        if isinstance(x, str) and x.startswith("C") or x.startswith("E")
        else "3"
    )
    console.log("Arreglando celdas nulas y vacias")
    # Aplica la limpieza solo a las celdas que no son nulas o vacías
    postulante_df["Domicilio Fiscal - Código Postal"] = postulante_df[
        "Domicilio Fiscal - Código Postal"
    ].str.replace(r"\D", "", regex=True)
    postulante_df["Domicilio Fiscal - Código Postal"].replace("", "0", inplace=True)

    postulante_df["Domicilio Fiscal - Número"] = postulante_df[
        "Domicilio Fiscal - Número"
    ].str.replace(r"\D", "", regex=True)
    postulante_df["Domicilio Fiscal - Número"].replace("", "0", inplace=True)
    postulante_df["Domicilio Fiscal - Número"] = postulante_df[
        "Domicilio Fiscal - Número"
    ].str[:5]

    postulante_df["Matrícula Cooperativa"] = (
        postulante_df["Matrícula Cooperativa"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
    )

    postulante_df["Domicilio Fiscal - Sector"] = (
        postulante_df["Domicilio Fiscal - Sector"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
    )
    postulante_df["Domicilio Fiscal - Sector"] = (
        postulante_df["Domicilio Fiscal - Sector"].astype(str).str[:5]
    )

    postulante_df["Domicilio Fiscal - Manzana"] = (
        postulante_df["Domicilio Fiscal - Manzana"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
    )
    postulante_df["Domicilio Fiscal - Manzana"] = (
        postulante_df["Domicilio Fiscal - Manzana"].astype(str).str[:5]
    )

    postulante_df["Domicilio Fiscal - Departamento"] = (
        postulante_df["Domicilio Fiscal - Departamento"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
    )
    postulante_df["Domicilio Fiscal - Departamento"] = (
        postulante_df["Domicilio Fiscal - Departamento"].astype(str).str[:5]
    )

    postulante_df["Domicilio Fiscal - Piso"] = (
        postulante_df["Domicilio Fiscal - Piso"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
    )
    postulante_df["Domicilio Fiscal - Piso"] = (
        postulante_df["Domicilio Fiscal - Piso"].astype(str).str[:5]
    )

    postulante_df["Domicilio Fiscal - Torre"] = (
        postulante_df["Domicilio Fiscal - Piso"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
    )
    postulante_df["Domicilio Fiscal - Torre"] = (
        postulante_df["Domicilio Fiscal - Piso"].astype(str).str[:5]
    )
    ################# LIMPIEZA DE DUPLICADOS Y DNI ERRONEOS ############################
    console.log("LIMPIEZA DE DUPLICADOS Y DNI ERRONEOS")
    # Identificar y guardar duplicados
    duplicados = postulante_df[postulante_df.duplicated(subset="CUIT", keep=False)]

    # Filtrar para quedarse solo con la fila más reciente
    postulante_df = postulante_df.sort_values(
        by=["CUIT", "Fecha de caratulación EE"], ascending=[True, False]
    ).drop_duplicates(subset="CUIT")

    # Crear el informe de borrados por duplicados
    informe_borrados_duplicados = duplicados[
        ~duplicados["Número de EE"].isin(postulante_df["Número de EE"])
    ]
    informe_borrados_duplicados["Motivo de Borrado"] = "Duplicado"

    # Identificar y guardar inconsistencias CUIT-DNI
    def tiene_inconsistencia(row):
        cuit = str(row["CUIT"])
        dni = str(row["Nº Documento"])
        return not (cuit[2:-1] == dni)

    inconsistencias = postulante_df[postulante_df.apply(tiene_inconsistencia, axis=1)]

    # Crear el informe de borrados por inconsistencia
    informe_borrados_inconsistencia = postulante_df.loc[inconsistencias.index].copy()
    informe_borrados_inconsistencia["Motivo de Borrado"] = "Inconsistencia CUIT-DNI"

    # Borrar las líneas con inconsistencias en postulante_df
    postulante_df = postulante_df.drop(inconsistencias.index)

    # Unir ambos informes
    informe_borrados = pd.concat(
        [informe_borrados_duplicados, informe_borrados_inconsistencia]
    )
    console.log("Guardando informe_borrados.xlsx")
    # Guardar informe_borrados como un archivo Excel
    informe_borrados.to_excel("SOMOSOTAD\\informe_borrados.xlsx", index=False)

    # Filtrar el df adherente_df eliminando las filas con "Número de EE" en común con el informe_borrados
    adherente_df = adherente_df[
        ~adherente_df["Número de EE"].isin(informe_borrados["Número de EE"])
    ]

    ####################################################################################

    # Actualizar la columna "Obra social elegida" en postulante_df según la condición en "¿Es jubilado?"
    postulante_df.loc[
        postulante_df["¿Es jubilado?"] == "SI", "Obra social elegida"
    ] = "500807"

    ################## LIMPIEZA DE DATOS MAL CARGADOS ##########################
    console.log("Guardando csvs y zips")
    try:
        # Verificar si el subdirectorio SOMOSOTAD existe, si no, crearlo
        subdirectory = "SOMOSOTAD"
        if not os.path.exists(subdirectory):
            os.makedirs(subdirectory)

        # Guardar el nuevo DataFrame como CSV
        adherente_df.to_csv("SOMOSOTAD\\adherentes.csv", sep="|", index=False)
        postulante_df.to_csv("SOMOSOTAD\\postulantes.csv", sep="|", index=False)

        # Definir los nombres de los archivos CSV y el nombre del archivo ZIP
        if adh is True:
            csv_files = ["SOMOSOTAD/postulantes.csv", "SOMOSOTAD/adherentes.csv"]
        else:
            csv_files = ["SOMOSOTAD/postulantes.csv"]
        zip_file = "SOMOSOTAD/postulantes_TAD.zip"

        # Crear un archivo ZIP y agregar los archivos CSV
        with zipfile.ZipFile(zip_file, "w") as zipf:
            for csv_file in csv_files:
                zipf.write(csv_file, arcname=csv_file.split("/")[-1])

        # armamos el envio a webservice
        postulante_df["CUIT"].to_csv(
            "SOMOSOTAD\\para_webservice.csv", index=False, header=False, sep="\t"
        )
        console.log(f"Archivos {csv_files} comprimidos en {zip_file}")
    except Exception as e:
        print(f"{e} \nHay problemas en la creacion de archivos.")
        input("Presiene [ENTER] para salir.")
        return 0

    input("\n[Presione ENTER para continuar.]")
