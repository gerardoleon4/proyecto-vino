# Clasificador de calidad del vino

Proyecto de Machine Learning que clasifica un vino como de **alta** o **baja** calidad a partir de 11 medidas fisicoquímicas. Usa el dataset [Wine Quality de UCI](https://archive.ics.uci.edu/dataset/186/wine+quality): 6,497 vinos portugueses *vinho verde* (1,599 tintos y 4,898 blancos) calificados del 0 al 10.

**Alta calidad = calificación de 7 o más** (1,277 vinos); el resto es baja calidad (5,220).

## Flujo

1. **Volcado a MySQL.** `sql/vino_dump.sql` crea la base `vino_db` y la tabla `vino` con los 6,497 vinos.
2. **Conexión.** `scripts/conexion.py` se conecta a `vino_db` con SQLAlchemy usando el archivo `.env`.
3. **Análisis.** `scripts/analizador.py` verifica que el volcado se cargó mostrando las primeras 5 filas.
4. **Entrenamiento.** `scripts/entrenador.py` divide 80/20, entrena un **Random Forest** (200 árboles, `class_weight='balanced'` porque hay pocos vinos de alta calidad), mide la efectividad (~88 %) y guarda el modelo final, entrenado con todos los vinos, en `modelo/vino.joblib`.
5. **Aplicación web.** `web/app.py` (Flask) recibe las 11 medidas en un formulario y muestra si el vino es de alta o baja calidad y qué tan seguro está el modelo.

## Cómo correrlo

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env              # y poner la contraseña

mysql -u vino_user -p < sql/vino_dump.sql   # carga el volcado

.venv/bin/python scripts/analizador.py   # primeras 5 filas
.venv/bin/python scripts/entrenador.py   # genera modelo/vino.joblib
.venv/bin/python web/app.py              # http://127.0.0.1:5000
```

## Estructura

```
proyecto-vino/
├── datos/            CSV originales de UCI
├── sql/              vino_dump.sql (volcado)
├── scripts/          conexion, analizador, entrenador
├── modelo/           vino.joblib
└── web/              app.py y templates/index.html
```
