# import yahoo_fin.stock_info
from yahoo_fin.stock_info import get_live_price
import time
import os
from datetime import datetime

startTime = datetime.now()

balance = 1000000
compra = 100000
ganancia = 100
btc_comprados = 0
compras = 0
ventas_ganadoras = 0
ventas_perdedoras = 0
ganancia_total = 0
comision = 2
moneda = "BTC"

try:
    while True:
        precio_actual = get_live_price("BTC-USD")

        # Compra
        if btc_comprados <= 0:
            btc_comprados = compra / precio_actual
            balance -= compra
            compras += 1

        valor_btc_ahora = precio_actual * btc_comprados

        # Venta ganancia
        if valor_btc_ahora > compra + (2 * ganancia):
            balance += valor_btc_ahora
            ganancia_total += valor_btc_ahora - compra
            btc_comprados = 0
            ventas_ganadoras += 1

        # Venta perdida
        if valor_btc_ahora < compra - ganancia:
            balance += valor_btc_ahora
            ganancia_total -= compra - valor_btc_ahora
            btc_comprados = 0
            ventas_perdedoras += 1

        os.system("clear")
        print(
            f"Balance: {balance:,.2f} EUR\n\
Precio {moneda} ahora: {precio_actual:,.2f} EUR\n\
{moneda} Comprados: {btc_comprados:,.2f} {moneda}\n\
Valor {moneda} a la compra: {compra:,.2f} EUR\n\
Valor {moneda} ahora: {valor_btc_ahora:,.2f} EUR\n\
Compras: {compras}\n\
Ventas Ganadoras: {ventas_ganadoras} \n\
Ventas Perdedoras: {ventas_perdedoras} \n\
Ganacias hasta ahora: {ganancia_total:,.2f} EUR\n\
Tiempo corriendo: {datetime.now() - startTime}\n\
        "
        )

        time.sleep(10)

except KeyboardInterrupt:
    pass
