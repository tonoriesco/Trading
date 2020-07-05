# import yahoo_fin.stock_info
from yahoo_fin.stock_info import get_live_price
import time
import os
from datetime import datetime
from save_data import (
    balance,
    compra,
    comision,
    valor_stop,
    btc_comprados,
    compras,
    ventas_ganadoras,
    ventas_perdedoras,
    ganancia_total,
    comisiones,
    moneda,
)


startTime = datetime.now()


try:
    while True:
        precio_actual = get_live_price("BTC-USD")

        # Compra
        if btc_comprados <= 0:
            btc_comprados = compra / precio_actual
            balance -= compra + comision
            compras += 1
            comisiones += comision
            ganancia_total -= comision

        valor_btc_ahora = precio_actual * btc_comprados

        # Venta ganancia
        if valor_btc_ahora > compra + (2 * valor_stop):
            balance += valor_btc_ahora - comision
            ganancia_total += valor_btc_ahora - compra
            btc_comprados = 0
            ventas_ganadoras += 1
            comisiones += comision

        # Venta perdida
        if valor_btc_ahora < compra - valor_stop:
            balance += valor_btc_ahora - comision
            ganancia_total += valor_btc_ahora - compra
            btc_comprados = 0
            ventas_perdedoras += 1
            comisiones += comision

        os.system("clear")
        print(
            f"Balance {balance:,.2f} EUR\n\
Precio {moneda} ahora: {precio_actual:,.2f} EUR\n\
{moneda} Comprados: {btc_comprados:,.2f} {moneda}\n\
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
        with open("save_data.py", "w") as f_variables:
            f_variables.write(
                f"balance = {balance}\n\
valor_stop = {valor_stop}\n\
btc_comprados = {btc_comprados}\n\
compra = {compra}\n\
compras = {compras}\n\
ventas_ganadoras = {ventas_ganadoras}\n\
ventas_perdedoras = {ventas_perdedoras} \n\
ganancia_total = {ganancia_total}\n\
comision = {comision}\n\
comisiones = {comisiones}\n\
moneda = \"{moneda}\"\n\
lastrun = \"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}\""
            )

        time.sleep(10)

except KeyboardInterrupt:
    pass
