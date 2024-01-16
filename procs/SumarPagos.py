import pandas as pd
from procs.console import console
import glob
import locale
from io import StringIO
import time


def COyPT(file):
    if "_CO" in file:
        programa = "CONAMI"
    elif "_PT" in file:
        programa = "POTENCIAR TRABAJO"

    console.rule(f"[bold red]{programa}")

    console.log(f"Leyendo archivo")
    df = pd.read_csv(file, encoding="ANSI", delimiter="|", decimal=",")
    console.log(f"Procesando archivo: {file}")

    locale.setlocale(locale.LC_ALL, "es_AR")

    monto = df["importe"].min()
    subsidioTotal = df["importe"].sum()
    cantAdh = df["adherentes"].sum()
    cantTitulares = df.shape[0]

    subsidioTitulares = cantTitulares * monto
    subsidioAdh = subsidioTotal - subsidioTitulares
    subsidioComparadoTotal = subsidioTitulares + subsidioAdh
    meta = cantAdh + cantTitulares

    locale.setlocale(locale.LC_ALL, "es_AR")
    console.print(f"{programa}:", style="bold red")
    print("PAGADO TOTAL:", locale.currency(subsidioTotal, grouping=True))
    print(f"TITULARES: {cantTitulares:n}")
    print("TITULARES PAGADO:", locale.currency(subsidioTitulares, grouping=True))
    print(f"ADH: {cantAdh:n}")
    print("ADH PAGADO:", locale.currency(subsidioAdh, grouping=True))
    print("ADH + TITULARES:", locale.currency(subsidioComparadoTotal, grouping=True))
    print(f"META: {meta:n}")
    time.sleep(1)


def OS(file):
    console.rule(f"[bold red]OBRAS SOCIALES")

    console.log(f"Leyendo archivo")
    df = pd.read_csv(file, encoding="ANSI", delimiter="|", decimal=",")
    console.log(f"Procesando archivo: {file}")

    locale.setlocale(locale.LC_ALL, "es_AR")
    monto = df["SUB"].min()
    subsidioTotal = df["SUB"].sum()
    cantTitulares = df.shape[0]
    cantAdh = df["ADHERENTES"].sum()
    subsidioAdh = cantAdh * monto
    subsidioTitulares = cantTitulares * monto
    subsidioComparadoTotal = subsidioAdh + subsidioTitulares
    meta = cantAdh + cantTitulares
    print("OBRAS SOCIALES:")
    print("PAGADO TOTAL:", locale.currency(subsidioTotal, grouping=True))
    print(f"TITULARES: {cantTitulares:n}")
    print("PAGO TITULARES:", locale.currency(subsidioTitulares, grouping=True))
    print(f"CANTIDAD ADHERENTES: {cantAdh:n}")
    print("PAGO ADHERENTES:", locale.currency(subsidioAdh, grouping=True))
    print("ADH + TITULARES:", locale.currency(subsidioComparadoTotal, grouping=True))
    print(f"META: {meta:n}")
    time.sleep(1)


def GEN(file):
    console.rule(f"[bold red]SUBSIDIO GENERAL")
    console.log(f"Leyendo archivo")
    with open(file, mode="r", encoding="ansi") as f:
        content = f.read()
    df = pd.read_fwf(
        StringIO(content),
        colspecs=((0, 99), (100, 111), (111, 117), (126, 132), (140, 147), (164, 168)),
        names=("etc", "cuit", "periodo", "OS", "importe", "adherentes"),
        dtype=str,
        skiprows=1,
        skipfooter=1,
    )
    console.log(f"Procesando archivo: {file}")
    periodo = df["periodo"].unique()
    console.log(f"Periodo de pagos: {periodo}")

    df["importe"] = df["importe"].apply(lambda x: float(x[:-2] + "." + x[-2:]))
    df["adherentes"] = df["adherentes"].astype(int)

    locale.setlocale(locale.LC_ALL, "es_AR")

    monto = df["importe"].min()
    subsidioTotal = df["importe"].sum()
    cantAdh = df["adherentes"].sum()
    cantTitulares = df.shape[0]

    subsidioTitulares = cantTitulares * monto
    subsidioAdh = subsidioTotal - subsidioTitulares
    subsidioComparadoTotal = subsidioTitulares + subsidioAdh
    meta = cantAdh + cantTitulares
    print("SUBSIDIO GENERAL:")
    print("PAGADO TOTAL:", locale.currency(subsidioTotal, grouping=True))
    print(f"TITULARES: {cantTitulares:n}")
    print("PAGO TITULARES:", locale.currency(subsidioTitulares, grouping=True))
    print(f"CANTIDAD ADHERENTES: {cantAdh:n}")
    print("PAGO ADHERENTES:", locale.currency(subsidioAdh, grouping=True))
    print("ADH + TITULARES:", locale.currency(subsidioComparadoTotal, grouping=True))
    print(f"META: {meta:n}")
    time.sleep(1)


def run():
    with console.status("Procesando", spinner="aesthetic"):
        ge = glob.glob("EFECTORES_SALIDA_*.txt")
        for file in ge:
            GEN(file)
        pt = glob.glob("mono_pt*")
        for file in pt:
            COyPT(file)
        co = glob.glob("mono_co*")
        for file in co:
            COyPT(file)
        os = glob.glob("Efectores_*.csv")
        for file in os:
            OS(file)

    input("\n[Presione ENTER para continuar.]")
