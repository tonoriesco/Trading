#!/usr/bin/env python3
import json

# import yahoo_fin.stock_info
from yahoo_fin.stock_info import get_live_price
import time
import os
from datetime import datetime

with open("data.json") as data_json:
    var_read = json.load(data_json)


balance = var_read["balance"]
valor_stop = var_read["valor_stop"]
objetos_comprados = var_read["objetos_comprados"]
compra = var_read["compra"]
compras = var_read["compras"]
ventas_ganadoras = var_read["ventas_ganadoras"]
ventas_perdedoras = var_read["ventas_perdedoras"]
ganancia_total = var_read["ganancia_total"]
comision = var_read["comision"]
comisiones = var_read["comisiones"]
moneda = var_read["moneda"]
lastrun = var_read["lastrun"]


startTime = datetime.now()
var_write = {}

try:
    while True:
        precio_actual = get_live_price("BTC-USD")

        # Compra
        if objetos_comprados <= 0:
            objetos_comprados = compra / precio_actual
            balance -= compra + comision
            compras += 1
            comisiones += comision
            ganancia_total -= comision

        valor_btc_ahora = precio_actual * objetos_comprados

        # Venta ganancia
        if valor_btc_ahora > compra + (2 * valor_stop):
            balance += valor_btc_ahora - comision
            ganancia_total += valor_btc_ahora - compra
            objetos_comprados = 0
            ventas_ganadoras += 1
            comisiones += comision

        # Venta perdida
        if valor_btc_ahora < compra - valor_stop:
            balance += valor_btc_ahora - comision
            ganancia_total += valor_btc_ahora - compra
            objetos_comprados = 0
            ventas_perdedoras += 1
            comisiones += comision

        os.system("clear")
        print(
            f"Balance {balance:,.2f} EUR\n\
Precio {moneda} ahora: {precio_actual:,.2f} EUR\n\
{moneda} Comprados: {objetos_comprados:,.2f} {moneda}\n\
Valor {moneda} a la compra: {compra:,.2f} EUR\n\
Valor {moneda} ahora: {valor_btc_ahora:,.2f} EUR\n\
Compras: {compras}\n\
Comision por operacion: {comision:,.2f} EUR\n\
Comisiones Totales: {comisiones:,.2f} EUR\n\
Ventas Ganadoras: {ventas_ganadoras} \n\
Ventas Perdedoras: {ventas_perdedoras} \n\
Ganacias hasta ahora: {ganancia_total:,.2f} EUR\n\
Tiempo corriendo: {datetime.now() - startTime}\n\
        "
        )

        lastrun = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        var_write["balance"] = balance
        var_write["valor_stop"] = valor_stop
        var_write["objetos_comprados"] = objetos_comprados
        var_write["compra"] = compra
        var_write["compras"] = compras
        var_write["ventas_ganadoras"] = ventas_ganadoras
        var_write["ventas_perdedoras"] = ventas_perdedoras
        var_write["ganancia_total"] = ganancia_total
        var_write["comision"] = comision
        var_write["comisiones"] = comisiones
        var_write["moneda"] = moneda
        var_write["lastrun"] = lastrun

        with open("data.json", "w") as file_write:
            json.dump(var_write, file_write, indent=4)

        time.sleep(60)

except KeyboardInterrupt:
    pass

# instantiate an empty dict
team = {}

# add a team member
team["tux"] = {"health": 23, "level": 4}
team["beastie"] = {"health": 13, "level": 6}
team["konqi"] = {"health": 18, "level": 7}

with open("mydata.json", "w") as f:
    json.dump(team, f, indent=4)
