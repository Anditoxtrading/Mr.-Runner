# 📚 Tutorial Completo de Mr. Runner

## 📖 Índice
1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
4. [Configuración Inicial](#configuración-inicial)
5. [Definir Puntos Shock](#definir-puntos-shock)
6. [Parámetros de Trading](#parámetros-de-trading)
7. [Ejecutar el Bot](#ejecutar-el-bot)
8. [Interpretando las Notificaciones](#interpretando-las-notificaciones)
9. [Ejemplos Prácticos](#ejemplos-prácticos)
10. [Gestión de Riesgo](#gestión-de-riesgo)
11. [Solución de Problemas](#solución-de-problemas)
12. [Mejores Prácticas](#mejores-prácticas)

---

## 🎯 Introducción

**Mr. Runner** es un bot de trading automatizado diseñado para operar en el mercado de futuros de criptomonedas utilizando una estrategia basada en puntos clave del mercado (puntos shock).

### ¿Cómo funciona?

1. **Defines puntos shock**: Basándote en tu análisis del libro de órdenes, defines niveles de precio para entradas long (compra) y short (venta)
2. **Monitoreo constante**: El bot monitorea el precio de las criptomonedas 24/7
3. **Ejecución automática**: Cuando el precio toca un punto shock, el bot abre una operación inmediatamente
4. **Gestión de riesgo**: Coloca stop loss automático y ajusta el stop a ganancias cuando el precio se mueve a favor

### Características principales

- ✅ Operaciones automáticas en puntos específicos
- ✅ Stop loss automático configurable
- ✅ Protección de ganancias (mueve el stop loss a breakeven cuando alcanza 1:1)
- ✅ Notificaciones en tiempo real vía Telegram
- ✅ Soporte para múltiples posiciones simultáneas
- ✅ Monitoreo de PNL (ganancias y pérdidas)

---

## 🛠️ Requisitos Previos

### 1. Cuenta de Exchange
- **Bybit** (cuenta registrada y verificada)
- Fondos en USDT para operar
- API Key con permisos de trading

### 2. Bot de Telegram
- Cuenta de Telegram
- Bot de Telegram creado (te explicaremos cómo)

### 3. Software
- **Python 3.7+** instalado en tu computadora
- Editor de texto (VS Code, Sublime, Notepad++, etc.)
- Terminal o línea de comandos

---

## 📦 Instalación

### Paso 1: Clonar o descargar el repositorio

```bash
git clone https://github.com/tuusuario/Mr.-Runner.git
cd Mr.-Runner
```

O descarga el archivo ZIP y extráelo.

### Paso 2: Instalar dependencias

Abre la terminal en la carpeta del proyecto y ejecuta:

```bash
pip install pybit telebot
```

O alternativamente:

```bash
pip install pybit pyTelegramBotAPI
```

### Paso 3: Verificar la instalación

```bash
python --version
pip list | grep pybit
pip list | grep telebot
```

Deberías ver las versiones instaladas de las librerías.

---

## ⚙️ Configuración Inicial

### 1. Obtener API Keys de Bybit

1. Inicia sesión en [Bybit](https://www.bybit.com)
2. Ve a **API** → **Crear nueva clave API**
3. Configura los permisos:
   - ✅ Trading de contratos (Contract Trading)
   - ✅ Leer posiciones
   - ❌ Retiros (por seguridad)
4. **Guarda tu API Key y Secret** en un lugar seguro

⚠️ **IMPORTANTE**: Nunca compartas tus API Keys con nadie.

### 2. Crear Bot de Telegram

1. Abre Telegram y busca **@BotFather**
2. Envía el comando `/newbot`
3. Sigue las instrucciones:
   - Nombre del bot: `Mi Mr Runner Bot` (puedes elegir el que quieras)
   - Username: `mi_mr_runner_bot` (debe terminar en `bot`)
4. **Guarda el token** que te proporciona BotFather

### 3. Obtener tu Chat ID de Telegram

1. Busca **@userinfobot** en Telegram
2. Inicia conversación con el bot
3. Te mostrará tu **Chat ID** (un número como `123456789`)
4. Guarda este número

### 4. Crear archivo de configuración

Crea un archivo llamado `config.py` en la carpeta del proyecto:

```python
# config.py

# API Keys de Bybit
api_key = "TU_API_KEY_AQUI"
api_secret = "TU_API_SECRET_AQUI"

# Telegram
token_telegram = "TU_TOKEN_DE_TELEGRAM_AQUI"
chat_id = "TU_CHAT_ID_AQUI"
```

**Ejemplo real** (con datos ficticios):

```python
# config.py

api_key = "A1B2C3D4E5F6G7H8"
api_secret = "X9Y8Z7W6V5U4T3S2"
token_telegram = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
chat_id = "987654321"
```

---

## 🎯 Definir Puntos Shock

Los puntos shock son los niveles de precio donde quieres que el bot abra operaciones.

### Crear el archivo `symbols_targets.txt`

Crea un archivo llamado `symbols_targets.txt` en la carpeta del proyecto.

### Formato del archivo

Cada línea debe tener este formato:

```
SIMBOLO PRECIO_LONG PRECIO_SHORT
```

- **SIMBOLO**: El par de trading (ej: BTCUSDT, ETHUSDT)
- **PRECIO_LONG**: Precio para abrir posición larga (compra)
- **PRECIO_SHORT**: Precio para abrir posición corta (venta)

### Ejemplo práctico

Supongamos que Bitcoin está en **$95,000** y Ethereum en **$3,500**:

```
BTCUSDT 94000 96000
ETHUSDT 3400 3600
SOLUSDT 180 190
```

**Interpretación:**
- Si BTC baja a $94,000 → abre LONG (compra)
- Si BTC sube a $96,000 → abre SHORT (venta)
- Si ETH baja a $3,400 → abre LONG
- Si ETH sube a $3,600 → abre SHORT
- Si SOL baja a $180 → abre LONG
- Si SOL sube a $190 → abre SHORT

### Reglas importantes

✅ El precio LONG debe ser **menor** que el precio SHORT
✅ Usa precios realistas basados en análisis técnico
✅ Puedes agregar todas las monedas que quieras
✅ Una moneda = una línea
✅ Usa espacios para separar los valores

---

## 🔧 Parámetros de Trading

Abre el archivo `Mr Runner.py` y busca la sección **"DEFINIR PARAMETROS PARA OPERAR"**:

```python
# DEFINIR PARAMETROS PARA OPERAR
amount_usdt = Decimal(50)  # Monto en USDT
distancia_porcentaje_sl = Decimal(2/100)  # Stop loss a un 2%
Numero_de_posiciones = 1  # Numero de posiciones simultaneas
```

### 1. `amount_usdt`
**Cantidad en USDT por operación**

- Por defecto: 50 USDT
- Recomendado para principiantes: 10-50 USDT
- Ajústalo según tu capital disponible

**Ejemplo:**
```python
amount_usdt = Decimal(100)  # Cada operación usará 100 USDT
```

### 2. `distancia_porcentaje_sl`
**Porcentaje de stop loss**

- Por defecto: 2% (0.02)
- Significado: Si el precio se mueve 2% en contra, cierra la operación
- Ajústalo según tu tolerancia al riesgo

**Ejemplos:**
```python
distancia_porcentaje_sl = Decimal(1/100)   # Stop loss al 1%
distancia_porcentaje_sl = Decimal(3/100)   # Stop loss al 3%
distancia_porcentaje_sl = Decimal(0.5/100) # Stop loss al 0.5%
```

### 3. `Numero_de_posiciones`
**Número máximo de posiciones simultáneas**

- Por defecto: 1
- Significado: Cuántas operaciones puede tener abiertas al mismo tiempo

**Ejemplos:**
```python
Numero_de_posiciones = 1  # Solo 1 posición a la vez
Numero_de_posiciones = 3  # Hasta 3 posiciones simultáneas
Numero_de_posiciones = 5  # Hasta 5 posiciones simultáneas
```

⚠️ **Cuidado**: Más posiciones = más riesgo

---

## 🚀 Ejecutar el Bot

### Paso 1: Verificar configuración

Antes de ejecutar, asegúrate de tener:
- ✅ `config.py` configurado con tus API keys
- ✅ `symbols_targets.txt` con tus puntos shock
- ✅ Parámetros de trading ajustados

### Paso 2: Iniciar el bot

Abre la terminal en la carpeta del proyecto y ejecuta:

```bash
python "Mr Runner.py"
```

### Paso 3: Verificar que está funcionando

Deberías ver en la consola algo como:

```
BTCUSDT - Precio actual: 95234.50, Long Target: 94000.00 (-1.30%), Short Target: 96000.00 (0.80%)
ETHUSDT - Precio actual: 3521.34, Long Target: 3400.00 (-3.45%), Short Target: 3600.00 (2.23%)
```

Esto significa que el bot está monitoreando activamente.

### Paso 4: Mantener el bot activo

- **No cierres la terminal** mientras quieras que el bot opere
- Para detener el bot: presiona `Ctrl + C`
- El bot funciona 24/7 mientras esté ejecutándose

### Ejecución en servidor (avanzado)

Para mantener el bot corriendo permanentemente:

```bash
nohup python "Mr Runner.py" > output.log 2>&1 &
```

Para ver los logs:
```bash
tail -f output.log
```

Para detener:
```bash
pkill -f "Mr Runner.py"
```

---

## 📱 Interpretando las Notificaciones

El bot te enviará mensajes a Telegram en diferentes situaciones:

### 1. Precio llegando a Target

```
⚠️ Precio llegando a punto Target Long BTCUSDT a 94000.0. Dejando de monitorear.
```

**Significado**: El precio tocó tu punto shock long y el bot va a abrir la operación.

### 2. Orden Long Abierta

```
🟢 ¡ORDEN LONG ABIERTA!
🔹 Ticker: BTCUSDT
🛡️ Stop Loss colocado con éxito
✅ Estado: Abierta con éxito
```

**Significado**: El bot abrió una posición de compra y colocó el stop loss.

### 3. Orden Short Abierta

```
🔴 ¡ORDEN SHORT ABIERTA!
🔹 Ticker: ETHUSDT
Stop Loss colocando con exito
✅ Estado: Abierta con éxito
```

**Significado**: El bot abrió una posición de venta y colocó el stop loss.

### 4. Stop Loss en Ganancias

```
🛡️ Stop loss en ganancias en BTCUSDT Porcentaje a Favor: 4.15% Ajustando stop loss...
Protección con stop loss en colocado con éxito
```

**Significado**: El precio se movió a tu favor y el bot movió el stop loss a breakeven (punto de entrada) para proteger ganancias.

### 5. Operación Cerrada con Ganancia

```
✅ ¡Operación cerrada en ganancia! 🎉💰
Símbolo: BTCUSDT
Lado: Buy
PNL: +12.45 USDT
```

**Significado**: La operación se cerró con beneficio.

### 6. Operación Cerrada con Pérdida

```
😢 Operación cerrada en pérdida 😢💸
Símbolo: ETHUSDT
Lado: Sell
PNL: -6.80 USDT
```

**Significado**: La operación se cerró en pérdida (alcanzó el stop loss).

### 7. Máximo de Posiciones

```
Se alcanzó el máximo posiciones abiertas. No se abrirá una nueva posición.
```

**Significado**: Ya tienes el número máximo de posiciones abiertas configurado.

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Trading Conservador

**Escenario**: Tienes $500 y quieres operar de forma segura.

**Configuración:**
```python
amount_usdt = Decimal(25)          # 5% de tu capital
distancia_porcentaje_sl = Decimal(1/100)  # Stop loss 1%
Numero_de_posiciones = 2           # Máximo 2 posiciones
```

**symbols_targets.txt:**
```
BTCUSDT 94500 95500
```

**Resultado esperado:**
- Riesgo por operación: 25 USDT × 1% = $0.25
- Máximo riesgo simultáneo: $0.50 (2 posiciones)
- Gestión conservadora del capital

### Ejemplo 2: Trading Agresivo

**Escenario**: Tienes $1,000 y buscas mayores ganancias (mayor riesgo).

**Configuración:**
```python
amount_usdt = Decimal(100)         # 10% de tu capital
distancia_porcentaje_sl = Decimal(3/100)  # Stop loss 3%
Numero_de_posiciones = 5           # Hasta 5 posiciones
```

**symbols_targets.txt:**
```
BTCUSDT 94000 96000
ETHUSDT 3400 3600
BNBUSDT 620 640
SOLUSDT 180 190
ADAUSDT 0.95 1.05
```

**Resultado esperado:**
- Riesgo por operación: 100 USDT × 3% = $3
- Máximo riesgo simultáneo: $15 (5 posiciones)
- Mayor exposición al mercado

### Ejemplo 3: Scalping en Volatilidad

**Escenario**: Quieres aprovechar movimientos rápidos en altcoins.

**Configuración:**
```python
amount_usdt = Decimal(50)
distancia_porcentaje_sl = Decimal(0.5/100)  # Stop muy ajustado
Numero_de_posiciones = 3
```

**symbols_targets.txt:**
```
PEPEUSDT 0.00001850 0.00001900
SHIBUSDT 0.00002100 0.00002150
DOGEUSDT 0.38 0.40
```

**Característica:**
- Stop loss muy ajustado (0.5%)
- Apropiado para monedas muy volátiles
- Requiere puntos shock muy precisos

---

## ⚖️ Gestión de Riesgo

### Cálculo de Riesgo por Operación

**Fórmula:**
```
Riesgo = amount_usdt × distancia_porcentaje_sl
```

**Ejemplo:**
```
amount_usdt = 100 USDT
distancia_porcentaje_sl = 2% (0.02)
Riesgo = 100 × 0.02 = 2 USDT por operación
```

### Reglas de Oro

1. **Nunca arriesgues más del 1-2% de tu capital por operación**
   ```python
   # Si tienes 1000 USDT:
   amount_usdt = Decimal(50)  # 5% del capital
   distancia_porcentaje_sl = Decimal(1/100)  # Riesgo real = 0.5 USDT (0.05%)
   ```

2. **Diversifica con posiciones simultáneas limitadas**
   ```python
   # No más de 3-5 posiciones simultáneas
   Numero_de_posiciones = 3
   ```

3. **Ajusta el stop loss según la volatilidad**
   - Bitcoin/Ethereum: 1-2%
   - Altcoins grandes: 2-3%
   - Altcoins pequeñas: 3-5%

### Sistema 1:1 de Protección

El bot automáticamente:
1. Abre operación con stop loss inicial
2. Cuando la ganancia alcanza el **doble del riesgo** (1:1), mueve el stop a breakeven
3. Deja correr las ganancias sin límite

**Ejemplo:**
```
Entrada: $100
Stop Loss: $98 (riesgo de $2)
Cuando alcanza $104 (ganancia de $4 = 2×$2):
  → Mueve stop loss a $100 (breakeven)
  → Ya no puedes perder en esta operación
```

---

## 🔧 Solución de Problemas

### Error: "No module named 'pybit'"

**Solución:**
```bash
pip install pybit
```

### Error: "No module named 'telebot'"

**Solución:**
```bash
pip install pyTelegramBotAPI
```

### Error: "No se pudo enviar el mensaje a Telegram"

**Causas posibles:**
1. Token de Telegram incorrecto
2. Chat ID incorrecto
3. No has iniciado conversación con tu bot

**Solución:**
1. Verifica `config.py`
2. Busca tu bot en Telegram y envíale `/start`
3. Verifica el chat ID con @userinfobot

### Error: "Invalid API key"

**Solución:**
1. Verifica que copiaste correctamente las API keys de Bybit
2. Asegúrate de que la API key tiene permisos de trading
3. Verifica que no esté en modo testnet si operas en real (y viceversa)

### El bot no abre operaciones

**Verificar:**
1. ¿El precio ha tocado tus puntos shock?
2. ¿El archivo `symbols_targets.txt` está correctamente formateado?
3. ¿Ya tienes el máximo de posiciones abiertas?
4. ¿Tienes fondos suficientes en tu cuenta?

**Debug:**
```bash
# Revisa la consola, debe mostrar:
BTCUSDT - Precio actual: 95234.50, Long Target: 94000.00...
```

### El bot abre operación pero no coloca stop loss

**Posibles causas:**
1. Error de formato en el precio
2. Precio fuera del rango permitido por el exchange

**Solución:**
- Revisa los logs en la consola
- Verifica que el símbolo sea correcto (ej: BTCUSDT, no BTC-USDT)

---

## ✨ Mejores Prácticas

### 1. Análisis antes de definir puntos shock

❌ **Mal:**
```
BTCUSDT 90000 100000  # Rango muy amplio, sin análisis
```

✅ **Bien:**
```
BTCUSDT 94750 95250  # Basado en niveles de soporte/resistencia
```

### 2. Prueba en testnet primero

1. Cambia en el código:
```python
session = HTTP(
    testnet=True,  # ← Cambia a True
    api_key=config.api_key,
    api_secret=config.api_secret,
)
```

2. Crea API keys de testnet en Bybit
3. Prueba con dinero ficticio
4. Cuando te sientas seguro, pasa a real

### 3. Monitoreo activo las primeras horas

- No dejes el bot solo inmediatamente
- Observa cómo reacciona a los movimientos de precio
- Verifica que las notificaciones lleguen correctamente
- Comprueba que los stop loss se colocan bien

### 4. Actualiza los puntos shock regularmente

El mercado cambia constantemente:
- Revisa tus niveles diariamente
- Actualiza `symbols_targets.txt` según análisis nuevo
- El bot lee el archivo cada 2 segundos, los cambios se aplican automáticamente

### 5. Lleva un registro de operaciones

Crea un archivo para registrar:
- Fecha y hora
- Símbolo operado
- Punto de entrada
- Resultado (ganancia/pérdida)
- Observaciones

Esto te ayudará a mejorar tu estrategia.

### 6. No sobreoperes

- Menos es más
- Es mejor tener 2-3 puntos muy bien analizados que 20 aleatorios
- La calidad sobre la cantidad

### 7. Gestión emocional

- No modifiques los parámetros después de una pérdida
- Mantén tu estrategia consistente
- Si tienes varias pérdidas seguidas, detén el bot y revisa tu análisis

---

## 📊 Resumen de Comandos Útiles

### Iniciar el bot
```bash
python "Mr Runner.py"
```

### Iniciar en background (Linux/Mac)
```bash
nohup python "Mr Runner.py" > output.log 2>&1 &
```

### Ver logs en tiempo real
```bash
tail -f output.log
```

### Detener bot en background
```bash
pkill -f "Mr Runner.py"
```

### Verificar procesos
```bash
ps aux | grep "Mr Runner"
```

---

## 🎓 Próximos Pasos

Ahora que conoces Mr. Runner:

1. **Configura tu entorno** siguiendo el paso a paso
2. **Prueba en testnet** con dinero ficticio
3. **Define tus primeros puntos shock** con análisis técnico
4. **Inicia con poco capital** para familiarizarte
5. **Ajusta y optimiza** según resultados

**Recuerda**: El trading automatizado no garantiza ganancias. Usa este bot como herramienta complementaria a tu análisis y gestión de riesgo.

---

## 📞 Soporte

Si tienes dudas o problemas:
1. Revisa la sección de [Solución de Problemas](#solución-de-problemas)
2. Verifica que seguiste todos los pasos correctamente
3. Revisa los logs en la consola para mensajes de error específicos

---

**⚠️ Disclaimer**: Este bot es una herramienta educativa. El trading de criptomonedas conlleva riesgos significativos. Opera solo con capital que puedas permitirte perder. Ningún bot garantiza ganancias.

**¡Feliz trading! 🚀**
