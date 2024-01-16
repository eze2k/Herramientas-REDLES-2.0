from pandasql import sqldf
from procs.console import console
from procs.Filtro import filtro
import pandas as pd
import timeit


def stats(dat, jub, dep, jur, fal, aut, inm, mvym):
    with console.status("Evaluando...", spinner="aesthetic"):
        tic = timeit.default_timer()
        muebles = filtro(aut, 2)
        inmuebles = filtro(inm, 1)
        # Create the "eval" dataframe with the desired columns
        eval_df = pd.DataFrame(
            columns=[
                "cuit",
                "ndoc",
                "deno",
                "sexo",
                "grado_confiab",
                "fnac",
                "FFALL",
                "Inmuebles",
                "Muebles",
                "Servicio_Domestico",
                "Dependiente",
                "Juridicas",
                "Jub_pen",
                "Fallecido",
            ]
        )

        # Copy the necessary columns from the "dat" dataframe
        eval_df[["cuit", "ndoc", "deno", "sexo", "grado_confiab", "fnac"]] = dat[
            ["cuit", "ndoc", "deno", "sexo", "grado_confiab", "fnac"]
        ]

        # Copy the "FFALL" column from the "fal" dataframe
        eval_df["FFALL"] = fal["FFALL"]

        # Check if a person appears in the "inmuebles" dataframe
        eval_df["Inmuebles"] = "No"
        eval_df.loc[inmuebles.index, "Inmuebles"] = "Si"

        # Check if a person appears in the "muebles" dataframe
        eval_df["Muebles"] = "No"
        eval_df.loc[muebles.index, "Muebles"] = "Si"

        # Check if a person appears in the "dep" dataframe with BASE as 105
        eval_df["Servicio_Domestico"] = "No"
        eval_df.loc[dep[dep["BASE"] == 105].index, "Servicio_Domestico"] = "Si"

        # Check if a person appears in the "dep" dataframe with MONTO greater than 87000
        eval_df["Dependiente"] = "No"
        eval_df.loc[dep[dep["MONTO"] > 87000].index, "Dependiente"] = "Si"

        # Check if a person appears in the "jur" dataframe
        eval_df["Juridicas"] = "No"
        eval_df.loc[jur.index, "Juridicas"] = "Si"

        # Check if a person appears in the "jub" dataframe with MONTO greater than 87000
        eval_df["Jub_pen"] = "No"
        eval_df.loc[jub[jub["MONTO"] > 87000].index, "Jub_pen"] = "Si"

        # Check if a person appears in the "fal" dataframe
        eval_df["Fallecido"] = "No"
        eval_df.loc[fal.index, "Fallecido"] = "Si"

        # Filter the dataframe to include only people with 'Si' in any evaluation column
        eval_df = eval_df[(eval_df.iloc[:, 7:] == "Si").any(axis=1)]
        console.log(f"Evaluando...[green]HECHO en {tic - timeit.default_timer()}")
    return (eval_df, muebles, inmuebles)

    # query = f"""
    #         SELECT
    #         distinct(dat.id_persona),
    #         dat.cuit,
    #         dat.ndoc,
    #         dat.deno,
    #         case when dat.sexo=1 then 'M' else 'F' end as sexo,
    #         dat.fnac,
    #         fal.FFALL,
    #         dat.grado_confiab,
    #         case when inm.id_persona is not null then 'Si' else 'No' end as Inmuebles,
    #         case when aut.id_persona is not null then 'Si' else 'No' end as Muebles,
    #         case when dep.base=105               then 'Si' else 'No' end as Servicio_Domestico,
    #         case when dep.monto > {mvym}         then 'Si' else 'No' end as Dependiente,
    #         case when jur.id_persona is not null then 'Si' else 'No' end as Juridicas,
    #         case when jub.monto > {mvym}         then 'Si' else 'No' end as Jub_pen,
    #         case when fal.id_persona is not null then 'Si' else 'No' end as Fallecido
    #         from dat
    #         left join muebles aut   on aut.ID_PERSONA = dat.id_persona
    #         left join inmuebles inm on inm.ID_PERSONA = dat.id_persona
    #         left join dep           on dep.ID_PERSONA = dat.id_persona
    #         left join jub           on jub.ID_PERSONA = dat.id_persona
    #         left join jur           on jur.ID_PERSONA = dat.id_persona
    #         left join fal           on fal.ID_PERSONA = dat.id_persona
    #         WHERE
    #         Inmuebles             ='Si'
    #         or Muebles            ='Si'
    #         or Servicio_Domestico ='Si'
    #         or Dependiente        ='Si'
    #         or Juridicas          ='Si'
    #         or Jub_pen            ='Si'
    #         or Fallecido          ='Si'
    #         """
    # eval = sqldf(query)
    # eval.set_index("id_persona", inplace=True)  # type: ignore
