import glob
import shutil
import pandas as pd
from procs.console import console
import datetime

namesList2 = [
    "IdSolicitud",
    "IdTipoSolicitud",
    "CUIL",
    "CUILViejo",
    "apeYnom",
    "Apellidos",
    "Nombres",
    "FechaNacimiento",
    "IdPaisNacimiento",
    "Sexo",
    "Edad",
    "Telefono",
    "Email",
    "FechaUltAct",
    "Dependencia",
    "IdPrograma",
    "IdTipoEfector",
    "NombreAgrupamiento",
    "Matricula",
    "IdActividad",
    "NumeroRenaf",
    "IdCentroEducativo",
    "IdNivelEducativo",
    "NivelFinalizado",
    "UltimoAnioAprobado",
    "IdCoberturaSalud",
    "IdAccesoSalud",
    "IdDificultadSalud",
    "IdObraSocial",
    "IdTrabajoSemanaAnterior",
    "TrabajoInformalSemanaAnterior",
    "BuscoTrabajoUltimos30Dias",
    "IdTiempoBuscaTrabajo",
    "TrabajoAlgunaVez",
    "IdTrabajoInformal",
    "NombreTrabajoInformal",
    "IdIngresosEfector",
    "Ingresos",
    "ComparteViviendaGrupoFamiliar",
    "IdTipoVivienda",
    "TipoViviendaOtro",
    "IdMaterialPisoVivienda",
    "IdMaterialTechoVivienda",
    "AmbientesVivienda",
    "IdAguaProvieneVivienda",
    "IdAguaLlegaVivienda",
    "IdBanioVivienda",
    "IdDesagueVivienda",
    "ZonaInundableVivienda",
    "BasuralesVivienda",
    "AlumbradoPublicoVivienda",
    "PavimentoVivienda",
    "RecoleccionResiduosVivienda",
    "TransportePublicoVivienda",
    "IdProvincia",
    "Provincia",
    "domLocalidad",
    "domCalle",
    "domCalleAltura",
    "domPiso",
    "domDto",
    "domMunicipio",
    "domCodigoPostal",
    "IdMotivoRenuncia",
    "FechaFallecimiento",
    "MotivoOtro",
    "ADH_CUIL",
    "ADH_apeyNom",
    "ADH_Apellidos",
    "ADH_Nombres",
    "ADH_AdhiereObraSocial",
    "ADH_DatosAdp",
    "ADH_FechaNacimiento",
    "ADH_Sexo",
    "ADH_Edad",
    "ADH_IdCentroEducativo",
    "ADH_IdNivelEducativo",
    "ADH_NivelFinalizado",
    "ADH_ultimoAnioAprobado",
    "ADH_IngresoUltimos30Dias",
    "ADH_Ingresos",
    "ADH_IdParentesco",
    "VersionModeloDatos",
    "TelefonoFijo",
    "TelefonoCelular",
    "IdGenero",
    "domDomTorre",
    "domDomBarrioParaje",
    "domManzana",
    "domDomCasa",
    "domDomDistritoDpto",
    "InicioActividades",
    "CantIntegrantes",
    "IdLugarActividad",
    "IdModalidadTrabajo",
    "IdMotivoInscripcion",
    "MotivoInscripcionOtros",
    "Discapacidad",
    "CursaEstudios",
]


def fill_namestitulares(row):
    if (
        (row["Apellidos"] == "")
        or (row["Nombres"] == "")
        or (len(row["Apellidos"]) <= 2)
        or (len(row["Nombres"]) <= 2)
    ):
        surname_parts = row["apeYnom"].split()
        if len(surname_parts[0]) <= 2:
            surname = surname_parts[0] + " " + surname_parts[1]
            names = surname_parts[2:]
        else:
            surname = surname_parts[0]
            names = surname_parts[1:]
        row["Apellidos"] = surname
        row["Nombres"] = " ".join(names)
    return row


def fill_namesadh(row):
    if row["ADH_apeyNom"] == "":
        return row
    if (
        (row["ADH_Apellidos"] == "")
        or (row["ADH_Nombres"] == "")
        or (len(row["ADH_Apellidos"]) <= 2)
        or (len(row["ADH_Nombres"]) <= 2)
    ):
        surname_parts = row["ADH_apeyNom"].split()
        if len(surname_parts[0]) <= 2:
            surname = surname_parts[0] + " " + surname_parts[1]
            names = surname_parts[2:]
        else:
            surname = surname_parts[0]
            names = surname_parts[1:]
        row["ADH_Apellidos"] = surname
        row["ADH_Nombres"] = " ".join(names)
    return row


def run():
    console.log("Procesando somoso.")
    # Create a list of file paths
    file_list = glob.glob("*solicitudes*.txt")

    # Read all the files into a list of dataframes
    df_list = [
        pd.read_csv(
            file,
            delimiter="|",
            encoding="ansi",
            # error_bad_lines=True,
            # warn_bad_lines=True,
            names=namesList2,
            dtype=str,
            na_values="",
            na_filter=False,
        )
        for file in file_list
    ]

    # Concatenate the list of dataframes into a single dataframe
    df = pd.concat(df_list, axis=0, ignore_index=True)
    # Save the combined and cleaned dataframe to a csv file
    # df.to_csv("out//combined_solicitudes.txt", sep="|", index=False, header=None)
    # Replace all hash symbols with the letter "Ñ"
    df = df.applymap(lambda x: str(x).replace("#", "Ñ"))
    # Remove accents from all columns in the dataframe
    df = df.applymap(lambda x: str(x).replace("á", "a"))
    df = df.applymap(lambda x: str(x).replace("é", "e"))
    df = df.applymap(lambda x: str(x).replace("í", "i"))
    df = df.applymap(lambda x: str(x).replace("ó", "o"))
    df = df.applymap(lambda x: str(x).replace("ú", "u"))
    df = df.applymap(lambda x: str(x).replace("Á", "A"))
    df = df.applymap(lambda x: str(x).replace("É", "E"))
    df = df.applymap(lambda x: str(x).replace("Í", "I"))
    df = df.applymap(lambda x: str(x).replace("Ó", "O"))
    df = df.applymap(lambda x: str(x).replace("Ú", "U"))
    # Remover puntos y comas de lugares q deberian ser ints
    df["domCalleAltura"] = df["domCalleAltura"].str.replace(",", "")
    df["domCalleAltura"] = df["domCalleAltura"].str.replace(".", "")
    df = df.apply(fill_namestitulares, axis=1)
    df = df.apply(fill_namesadh, axis=1)
    # Save the combined and cleaned dataframe to a csv file
    fecha = datetime.datetime.now().strftime("%Y%d%m")

    df.to_csv(
        f"out//SOMOSO_Lote_{fecha}.txt",  # type: ignore
        sep="|",
        encoding="ANSI",
        index=False,
        na_rep="",
        header=None,  # type: ignore
    )
    print(file_list)
    for file in file_list:
        shutil.move(file, "in")
    console.log("Se efectuo la limpieza/combinacion con exito.")
    input("[Presione ENTER para continuar.]")

    return 0
