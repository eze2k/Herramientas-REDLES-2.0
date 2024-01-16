from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem
from procs import (
    Keys,
    PaquetesSINTyS,
    SomosoCleaner,
    Remanentes,
    Paquetes2Excel,
    SumarPagos,
    noms,
    Sintys_stats,
    TADI,
)
from rich.console import Console
from rich import print


def main():
    somsoCL = FunctionItem("Somoso combinacion/limpieza.", SomosoCleaner.run)
    sumarPagos = FunctionItem("Sumar archivo pagos.", SumarPagos.run)
    remanentes = FunctionItem("Procesado de remanentes para enviar.", Remanentes.run)
    tadi = FunctionItem("TADI combinacion/limpieza.", TADI.run)

    sintysEncrypt = FunctionItem(
        "Encriptar archivos para SINTyS.", PaquetesSINTyS.runEncrypt
    )
    sintysDecrypt = FunctionItem(
        "Desencryptar archivos para SINTyS.", PaquetesSINTyS.runDecrypt
    )
    nomss = FunctionItem("NOMS a txt.", noms.go)
    sintys = FunctionItem("Sintys STATS.", Sintys_stats.sintys)

    sintysKeys = FunctionItem("Instalacion de llaves SINTyS.", Keys.run)

    # submenu PAQUETES
    submenu = ConsoleMenu("Paquetes a excel.", "Seleccione una opcion:")
    p02xlsx = FunctionItem("Paquete 0 a excel.", Paquetes2Excel.p02xlsx)
    p12xlsx = FunctionItem("Paquete 1 a excel.", Paquetes2Excel.p12xlsx)
    p52xlsx = FunctionItem("Paquete 5 a excel.", Paquetes2Excel.p52xlsx)
    p72xlsx = FunctionItem("Paquete 7 a excel.", Paquetes2Excel.p72xlsx)
    p82xlsx = FunctionItem("Paquete 8 a excel.", Paquetes2Excel.p82xlsx)
    somoso2xlsx = FunctionItem("SOMOSO a excel.", Paquetes2Excel.somoso2xlsx)

    submenu.append_item(p02xlsx)
    submenu.append_item(p12xlsx)
    submenu.append_item(p52xlsx)
    submenu.append_item(p72xlsx)
    submenu.append_item(p82xlsx)
    submenu.append_item(somoso2xlsx)
    paquetes2excel = SubmenuItem("Convertir paquetes a excel.", submenu)

    menu = ConsoleMenu("Herramientas REDLES 2", "Elija una opcion:")
    menu.append_item(somsoCL)
    menu.append_item(tadi)
    menu.append_item(remanentes)
    menu.append_item(sintysEncrypt)
    menu.append_item(sintysDecrypt)
    menu.append_item(paquetes2excel)
    menu.append_item(sumarPagos)
    menu.append_item(nomss)
    menu.append_item(sintys)
    menu.append_item(sintysKeys)
    menu.show()


if __name__ == "__main__":
    main()
