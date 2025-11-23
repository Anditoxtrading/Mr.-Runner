Mr. Runner es un bot de trading diseñado para maximizar ganancias mediante una estrategia dinámica y eficiente basada en puntos clave del mercado. 

¿Cómo funciona Mr. Runner?
Definición de puntos shock:
Tú defines los puntos shock para long y short basándote en tu análisis del libro de órdenes. Estos puntos marcan los niveles en los que el bot estará atento a posibles movimientos del precio.

Monitoreo del precio:
Una vez configurados los puntos shock, el bot monitorea constantemente el mercado. Si el precio alcanza uno de los puntos definidos, Mr. Runner actúa de inmediato.

Ejecución de operaciones:

Cuando el precio toca un punto shock, el bot abre una operación a market en la dirección correspondiente (long o short).
El bot establece automáticamente un stop loss en un porcentaje predeterminado, que defines al configurar el bot.
Gestión dinámica de ganancias:

Si el precio se mueve a favor de la operación, el bot asegura un beneficio inicial equivalente al 1 a 1 del riesgo asumido.
Una vez asegurado el 1 a 1, Mr. Runner permite que la operación siga activa, dejando correr las ganancias para maximizar el rendimiento.
Beneficios clave:
Protección inteligente: Garantiza que siempre se asegure al menos el beneficio inicial, minimizando riesgos.
Maximización de ganancias: Permite que las operaciones exitosas sigan creciendo sin restricciones innecesarias.
Ejecución precisa: Opera automáticamente en puntos clave definidos por el análisis del libro de órdenes.
Flexibilidad: Te permite personalizar los puntos shock y el porcentaje de stop loss según tu estrategia.


## 📚 Documentación

Para aprender a usar Mr. Runner de forma completa, consulta nuestro **[Tutorial Completo](TUTORIAL.md)** que incluye:

- 📦 Instalación paso a paso
- ⚙️ Configuración detallada
- 🎯 Cómo definir puntos shock
- 🚀 Ejecución y monitoreo
- 💡 Ejemplos prácticos
- 🔧 Solución de problemas
- ✨ Mejores prácticas

## 🚀 Instalación Rápida

```bash
pip install pybit pyTelegramBotAPI
```

## ⚙️ Configuración

1. Copia `config.py.example` a `config.py` y completa tus credenciales
2. Copia `symbols_targets.txt.example` a `symbols_targets.txt` y define tus puntos shock
3. Ejecuta: `python "Mr Runner.py"`

Para más detalles, consulta el [Tutorial Completo](TUTORIAL.md).
