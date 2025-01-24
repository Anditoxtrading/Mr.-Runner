import config
import time
from pybit.unified_trading import HTTP
from decimal import Decimal, ROUND_DOWN, ROUND_FLOOR
import threading
import telebot

session = HTTP(
    testnet=False,
    api_key=config.api_key,
    api_secret=config.api_secret,
)

# DEFINIR PARAMETROS PARA OPERAR
amount_usdt = Decimal(50) # Monto en USDT 
distancia_porcentaje_sl = Decimal( 2/ 100) # Stop loss a un 2%, puedes modificarlo segun tu gestion.
Numero_de_posiciones= 1  # Numero de posiciones que quieres permitir abrir de forma simultanea
posiciones_con_stop = {}


bot_token = config.token_telegram
bot = telebot.TeleBot(bot_token)
chat_id = config.chat_id

def enviar_mensaje_telegram(chat_id, mensaje):
    try:
        bot.send_message(chat_id, mensaje, parse_mode='HTML')
    except Exception as e:
        print(f"No se pudo enviar el mensaje a Telegram: {e}")

def get_current_position(symbol):
    try:
        response_positions = session.get_positions(category="linear", symbol=symbol)
        if response_positions['retCode'] == 0:
            return response_positions['result']['list']
        else:
            print(f"Error al obtener la posición: {response_positions}")
            return None
    except Exception as e:
        print(f"Error al obtener la posición: {e}")
        return None


def get_open_positions_count():
    try:
        response_positions = session.get_positions(category="linear", settleCoin="USDT")
        if response_positions['retCode'] == 0:
            positions = response_positions['result']['list']
            open_positions = [position for position in positions if Decimal(position['size']) != 0]
            return len(open_positions)
        else:
            print(f"Error al obtener el conteo de posiciones abiertas: {response_positions}")
            return 0
    except Exception as e:
        print(f"Error al obtener el conteo de posiciones abiertas: {e}")
        return 0

        
def stop_ganancias(symbol): # Stop loss en ganancias
    try:
        # Obtener la lista de posiciones actuales
        positions_list = get_current_position(symbol)
        if not positions_list or len(positions_list) == 0:
            print(f"No hay posiciones abiertas para {symbol}.")
            return
        
        # Extraer información de la posición
        current_price = Decimal(positions_list[0]['avgPrice'])
        side = positions_list[0]['side']

        # Calcular el precio del stop loss según el lado de la posición
        distancia_porcentaje_ptr_decimal = Decimal(str(distancia_porcentaje_sl))
        if side == "Buy":
            price_sl = adjust_price(symbol, current_price * (Decimal(1) + distancia_porcentaje_ptr_decimal))
        elif side == "Sell":
            price_sl = adjust_price(symbol, current_price * (Decimal(1) - distancia_porcentaje_ptr_decimal))
        else:
            print(f"No se detecta el lado de la posicion {side}")
            return

        # Configurar el stop loss
        stop_loss_order = session.set_trading_stop(
            category="linear",
            symbol=symbol,
            stopLoss=str(price_sl), 
            slTriggerBy="LastPrice", 
            tpslMode="Full",
            slOrderType="Market",
        )

        # Enviar mensaje y mostrar resultado
        mensaje = f"Protección con stop loss en {symbol} colocado con éxito: {stop_loss_order}"
        enviar_mensaje_telegram(chat_id=chat_id, mensaje=mensaje)
        print(mensaje)
    
    except Exception as e:
        print(f"Error en stop_ganancias para {symbol}: {str(e)}")


def abrir_posicion_largo(symbol, base_asset_qty_final, distancia_porcentaje_sl):
    try:
        if get_open_positions_count() >= Numero_de_posiciones: 
            mensaje_count =("Se alcanzó el máximo posiciones abiertas. No se abrirá una nueva posición.")
            enviar_mensaje_telegram(chat_id=chat_id, mensaje=mensaje_count)
            print (mensaje_count)
            return

        positions_list = get_current_position(symbol)
        if positions_list and any(Decimal(position['size']) != 0 for position in positions_list):
            print("Ya hay una posición abierta. No se abrirá otra posición.")
            return

        response_market_order = session.place_order(
            category="linear",
            symbol=symbol,
            side="Buy",
            orderType="Market",
            qty=base_asset_qty_final,
        )
        Mensaje_market = f"Orden Market Long en {symbol} abierta con éxito: {response_market_order}"
        enviar_mensaje_telegram(chat_id=chat_id, mensaje=Mensaje_market)
        print(Mensaje_market)

        time.sleep(5)
        if response_market_order['retCode'] != 0:
            print("Error al abrir la posición: La orden de mercado no se completó correctamente.")
            return

        positions_list = get_current_position(symbol)
        current_price = Decimal(positions_list[0]['avgPrice'])

        price_sl = adjust_price(symbol, current_price * Decimal(1 - distancia_porcentaje_sl))
        stop_loss_order = session.set_trading_stop(
            category="linear",
            symbol=symbol,
            stopLoss=price_sl,
            slTriggerB="LastPrice",
            tpslMode="Full",
            slOrderType="Market",
        )
        mensaje_sl = f"Stop Loss para {symbol} colocado con éxito: {stop_loss_order}"
        enviar_mensaje_telegram(chat_id=chat_id, mensaje=mensaje_sl)
        print(mensaje_sl)
    except Exception as e:
        print(f"Error al abrir la posición: {e}")

def abrir_posicion_corto(symbol, base_asset_qty_final, distancia_porcentaje_sl):
    try:
        if get_open_positions_count() >= Numero_de_posiciones: 
            mensaje_count =("Se alcanzó el máximo posiciones abiertas. No se abrirá una nueva posición.")
            enviar_mensaje_telegram(chat_id=chat_id, mensaje=mensaje_count)
            print (mensaje_count)
            return

        positions_list = get_current_position(symbol)
        if positions_list and any(Decimal(position['size']) != 0 for position in positions_list):
            print("Ya hay una posición abierta. No se abrirá otra posición.")
            return

        response_market_order = session.place_order(
            category="linear",
            symbol=symbol,
            side="Sell",
            orderType="Market",
            qty=base_asset_qty_final,
        )
        Mensaje_market = f"Orden Market Short en {symbol} abierta con éxito: {response_market_order}"
        enviar_mensaje_telegram(chat_id=chat_id, mensaje=Mensaje_market)
        print(Mensaje_market)

        time.sleep(5)
        if response_market_order['retCode'] != 0:
            print("Error al abrir la posición: La orden de mercado no se completó correctamente.")
            return

        positions_list = get_current_position(symbol)
        current_price = Decimal(positions_list[0]['avgPrice'])

        price_sl = adjust_price(symbol, current_price * Decimal(1 + distancia_porcentaje_sl))
        stop_loss_order = session.set_trading_stop(
            category="linear",
            symbol=symbol,
            stopLoss=price_sl,
            slTriggerB="LastPrice",
            tpslMode="Full",
            slOrderType="Market",
        )
        mensaje_sl = f"Stop Loss para {symbol} colocado con éxito: {stop_loss_order}"
        enviar_mensaje_telegram(chat_id=chat_id, mensaje=mensaje_sl)
        print(mensaje_sl)
    except Exception as e:
        print(f"Error al abrir la posición: {e}")

def qty_step(symbol, amount_usdt):
    try:
        tickers = session.get_tickers(symbol=symbol, category="linear")
        for ticker_data in tickers["result"]["list"]:
            last_price = float(ticker_data["lastPrice"])

        last_price_decimal = Decimal(last_price)

        step_info = session.get_instruments_info(category="linear", symbol=symbol)
        qty_step = Decimal(step_info['result']['list'][0]['lotSizeFilter']['qtyStep'])

        base_asset_qty = amount_usdt / last_price_decimal

        qty_step_str = str(qty_step)
        if '.' in qty_step_str:
            decimals = len(qty_step_str.split('.')[1])
            base_asset_qty_final = round(base_asset_qty, decimals)
        else:
            base_asset_qty_final = int(base_asset_qty)

        return base_asset_qty_final
    except Exception as e:
        print(f"Error al calcular la cantidad del activo base: {e}")
        return None

def adjust_price(symbol, price):
    try:
        instrument_info = session.get_instruments_info(category="linear", symbol=symbol)
        tick_size = float(instrument_info['result']['list'][0]['priceFilter']['tickSize'])
        price_scale = int(instrument_info['result']['list'][0]['priceScale'])

        tick_dec = Decimal(f"{tick_size}")
        precision = Decimal(f"{10**price_scale}")
        price_decimal = Decimal(f"{price}")
        adjusted_price = (price_decimal * precision) / precision
        adjusted_price = (adjusted_price / tick_dec).quantize(Decimal('1'), rounding=ROUND_FLOOR) * tick_dec

        return float(adjusted_price)
    except Exception as e:
        print(f"Error al ajustar el precio: {e}")
        return None

def read_symbols_targets(file_path):
    symbols_targets = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:  # Asegurar que hay símbolo, precio long y precio short
                    symbol = parts[0]
                    target_price_lg = Decimal(parts[1])
                    target_price_st = Decimal(parts[2])
                    symbols_targets[symbol] = (target_price_lg, target_price_st)
    except Exception as e:
        print(f"Error al leer el archivo de símbolos y targets: {e}")
    return symbols_targets

def tomar_decision(file_path):
    monitoreados = set()  # Para rastrear qué monedas ya se han monitoreado y procesado
    while True:
        # Leer constantemente el archivo y actualizar los targets
        symbols_targets = read_symbols_targets(file_path)

        for symbol, (target_price_lg, target_price_st) in symbols_targets.items():
            if symbol not in monitoreados:  # Si la moneda no ha sido monitoreada aún
                try:
                    # Obtener el precio actual de la moneda
                    tickers = session.get_tickers(symbol=symbol, category="linear")
                    last_price = Decimal(tickers["result"]["list"][0]["lastPrice"])
                    
                    # Calcular las distancias porcentuales para long y short
                    distancia_long = ((target_price_lg - last_price) / last_price) * 100
                    distancia_short = ((last_price - target_price_st) / last_price) * 100

                    # Verificar condiciones para abrir posición larga o corta
                    if last_price <= target_price_lg:  # Condición para posición larga
                        base_asset_qty_final = qty_step(symbol, amount_usdt)
                        abrir_posicion_largo(symbol, base_asset_qty_final, distancia_porcentaje_sl)
                        monitoreados.add(symbol)  # Marcar la moneda como procesada
                        mensaje_monitor = f"Precio llegando a punto Target Long {symbol} a {last_price}. Dejando de monitorear."
                        enviar_mensaje_telegram(chat_id=chat_id, mensaje=mensaje_monitor)
                        print(mensaje_monitor)

                    elif last_price >= target_price_st:  # Condición para posición corta
                        base_asset_qty_final = qty_step(symbol, amount_usdt)
                        abrir_posicion_corto(symbol, base_asset_qty_final, distancia_porcentaje_sl)
                        monitoreados.add(symbol)  # Marcar la moneda como procesada
                        mensaje_monitor = f"Precio llegando a punto Target Short {symbol} a {last_price}. Dejando de monitorear."
                        enviar_mensaje_telegram(chat_id=chat_id, mensaje=mensaje_monitor)
                        print(mensaje_monitor)

                    else:
                        # Log de precios actuales, targets y porcentajes
                        print(f"{symbol} - Precio actual: {last_price}, "
                              f"Long Target: {target_price_lg} ({distancia_long:.2f}%), "
                              f"Short Target: {target_price_st} ({distancia_short:.2f}%)")
                        print("")
                
                except Exception as e:
                    print(f"Error al tomar decisión para {symbol}: {e}")
        
        # Retornar a la lectura del archivo para verificar si hubo cambios
        time.sleep(5)  # Espera de 5 segundos antes de volver a leer el archivo


def monitorear_posiciones(distancia_porcentaje_favor):
    while True:
        try:
            # Obtener todas las posiciones activas para USDT
            posiciones = session.get_positions(category="linear", settleCoin="USDT")
            for posicion in posiciones["result"]["list"]:
                size = Decimal(posicion["size"])  # Tamaño de la posición
                if size == 0:
                    continue  # Si no hay tamaño, no hay posición activa

                symbol = posicion["symbol"]
                side = posicion["side"]  # "Buy" o "Sell"
                entry_price = Decimal(posicion["avgPrice"])

                # Obtener el precio actual desde los tickers
                tickers = session.get_tickers(symbol=symbol, category="linear")
                last_price = None
                for ticker_data in tickers["result"]["list"]:
                    if ticker_data["symbol"] == symbol:
                        last_price = Decimal(ticker_data["lastPrice"])
                        break

                if last_price is None:
                    print(f"No se pudo obtener el precio actual para {symbol}.")
                    continue

                # Calcular el porcentaje de avance
                avance_porcentaje = (
                    (last_price - entry_price) / entry_price * 100
                    if side == "Buy"
                    else (entry_price - last_price) / entry_price * 100
                )

                # Si el avance a favor cumple la condición y no se ha colocado stop loss aún
                if avance_porcentaje >= distancia_porcentaje_favor and symbol not in posiciones_con_stop:
                    print(
                        f"El precio de {symbol} ha avanzado un {avance_porcentaje:.2f}% a favor de la posición. Ajustando stop loss..."
                    )

                    # Cancelar solo las órdenes de Stop Loss asociadas a la posición
                    # Se asume que el stop loss tiene una orden activa
                    try:
                        orders = session.get_open_orders(symbol=symbol, category="linear")
                        for order in orders["result"]["list"]:
                            if order["type"] == "STOP_MARKET":  # Solo cancelar órdenes de Stop Loss
                                session.cancel_order(symbol=symbol, orderId=order["orderId"], category="linear")
                                print(f"Stop loss cancelado para {symbol}.")
                    except Exception as e:
                        print(f"Error al cancelar órdenes de Stop Loss para {symbol}: {e}")

                    # Colocar el stop loss en ganancia (ajustado)
                    stop_ganancias(symbol)
                    print(f"Stop loss en ganancia colocado para {symbol}.")

                    # Marcar que ya se ha colocado el stop loss para esta posición
                    posiciones_con_stop[symbol] = True
                    
        except Exception as e:
            print(f"Error al monitorear posiciones: {e}")

        time.sleep(5)  # Revisión cada 5 segundos
if __name__ == "__main__":
    file_path = 'symbols_targets.txt'
    distancia_porcentaje_favor = distancia_porcentaje_sl * 2 * 100

    # Hilo para la función 'tomar_decision'
    tomar_decision_thread = threading.Thread(target=tomar_decision, args=(file_path,))
    tomar_decision_thread.start()

    # Hilo para la función 'monitorear_posiciones' con el argumento necesario
    monitor_position_thread = threading.Thread(target=monitorear_posiciones, args=(distancia_porcentaje_favor,))
    monitor_position_thread.start()
