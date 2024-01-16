from procs import P30, Prov, Evaluar
from rich.console import Console
from rich.prompt import Prompt
from procs.DictsAndLists1x import lista

# from procs.DictsAndLists2x import lista
import pandas as pd
import timeit


def sintys():
    # Timear el proceso
    ticg = timeit.default_timer()

    # Inicializamos la consola de rich
    console = Console(log_path=False)

    # Tiulo
    console.rule(f"[bold red]SINTyS STATS")

    datos = Prompt.ask("usar pandas 2.0?)", default="n")
    if datos in ("y", "s", "S", "Y"):
        ver = 1
    else:
        ver = 0

    engine = ["c", "pyarrow", "python"]
    backend = ["numpy_nullable", "pyarrow"]

    # Leemos el p30.
    paquete30 = P30.lectura("SINTYS.tar.gz", engine[ver], backend[ver])

    # Juntamos las variables para usar del dict.
    # Si por alguna razon no existe el dataframe, lo rellena de uno vacio pero con
    # las mismas columnas para evitar errores.
    # fmt: off
    var = paquete30.get("B00", pd.DataFrame(columns=lista[0]["dtype"].keys())) # type: ignore
    dat = paquete30.get("DATOS", pd.DataFrame(columns=lista[1]["dtype"].keys())) # type: ignore
    bar = paquete30.get("EMBARCACIONES", pd.DataFrame(columns=lista[2]["dtype"].keys()))# type: ignore
    avi = paquete30.get("AERONAVES", pd.DataFrame(columns=lista[3]["dtype"].keys())) # type: ignore 
    dep = paquete30.get("EMPLEO_DEPENDIENTE", pd.DataFrame(columns=lista[4]["dtype"].keys())) # type: ignore
    ind = paquete30.get("EMPLEO_INDEPENDIENTE", pd.DataFrame(columns=lista[5]["dtype"].keys()))# type: ignore
    fal = paquete30.get("FALLECIDOS", pd.DataFrame(columns=lista[6]["dtype"].keys())) # type: ignore
    inm = paquete30.get("INMUEBLES", pd.DataFrame(columns=lista[7]["dtype"].keys()))# type: ignore
    jub = paquete30.get("JUBILACIONES_PENSIONES", pd.DataFrame(columns=lista[8]["dtype"].keys())) # type: ignore
    aut = paquete30.get("PADRON_AUTOMOTORES", pd.DataFrame(columns=lista[9]["dtype"].keys())) # type: ignore
    jur = paquete30.get("PERSONAS_JURIDICAS", pd.DataFrame(columns=lista[10]["dtype"].keys()))# type: ignore
    pnc = paquete30.get("PNC", pd.DataFrame(columns=lista[11]["dtype"].keys())) # type: ignore
    rub = paquete30.get("RUBPS", pd.DataFrame(columns=lista[12]["dtype"].keys()))# type: ignore
    asg = paquete30.get("ASIGNACIONES", pd.DataFrame(columns=lista[13]["dtype"].keys()))# type: ignore
    # Evaluamos.
    eval_stats = Evaluar.stats(dat, jub, dep, jur, fal, aut, inm, 112500)
    # Stats
    # prov_stats = Prov.stats(dat, pnc, var, jub, dep, asg, fal, jur, rub)

    # Armamos las tabs del excel y lo exportamos.
    with console.status("Exportando Excel evaluaciones...", spinner="aesthetic"):
        tic = timeit.default_timer()
        writer = pd.ExcelWriter("out/Evaluacion_P30.xlsx", engine="xlsxwriter")
        # stats_prov.to_excel(writer, sheet_name="Stats globales")
        eval_stats[0].to_excel(writer, sheet_name="Efectores fuera del marco legal")  # type: ignore
        eval_stats[1].to_excel(writer, sheet_name="Detalle Muebles")  # type: ignore
        eval_stats[2].to_excel(writer, sheet_name="Detalle Inmuebles")  # type: ignore
        writer.close()
    console.log(f"Exportando Excel evaluaciones...[green]HECHO en {tic - timeit.default_timer()}")

    datos = Prompt.ask("Armar excel datos?(puede tardar mucho si es un P30)", default="n")
    if datos in ("y", "s", "S", "Y"):
        # Armamos un excel con todos los datos para su emjor lectura
        with console.status("Exportando Excel datos...", spinner="aesthetic"):
            tic = timeit.default_timer()
            writerF = pd.ExcelWriter("out/Datos_P30.xlsx", engine="xlsxwriter")
            var.to_excel(writerF, sheet_name="varios")
            dat.to_excel(writerF, sheet_name="datos")
            bar.to_excel(writerF, sheet_name="barcos")
            avi.to_excel(writerF, sheet_name="aviones")
            dep.to_excel(writerF, sheet_name="dependientes")
            ind.to_excel(writerF, sheet_name="independientes")
            fal.to_excel(writerF, sheet_name="fallecidos")
            inm.to_excel(writerF, sheet_name="inmuebles")
            jub.to_excel(writerF, sheet_name="jubilados")
            aut.to_excel(writerF, sheet_name="automotores")
            jur.to_excel(writerF, sheet_name="juridicos")
            pnc.to_excel(writerF, sheet_name="pensiones no contrib")
            rub.to_excel(writerF, sheet_name="programas sociales")
            asg.to_excel(writerF, sheet_name="asignaciones familiares")
            writerF.close()
        console.log(f"Exportando Excel datos...[green]HECHO en {tic - timeit.default_timer()}")
    else:
        pass
    # fmt: on
    console.log(f"PROCESO...[green]COMPLETADO en {ticg - timeit.default_timer()}")
    input("Presione [ENTER] para salir.")
    return 0
