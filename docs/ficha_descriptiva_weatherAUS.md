# Ficha descriptiva del conjunto de datos: *Rain in Australia* (`weatherAUS.csv`)

## 1. Identificación general y problema abordado

| Campo | Detalle |
|---|---|
| **Nombre del conjunto de datos** | *Rain in Australia* (`weatherAUS.csv`) |
| **Fuente y custodia** | Bureau of Meteorology (Commonwealth of Australia); compilado en el proyecto *Rattle* (Graham Williams) y publicado en Kaggle |
| **Dimensiones** | **145.460 observaciones** (filas) y **23 variables** (columnas) |
| **Cobertura espacial y temporal** | **49 estaciones meteorológicas** de Australia, con registros diarios del **1 de noviembre de 2007 al 25 de junio de 2017** |
| **Integridad estructural** | **0 filas duplicadas** exactas y **0 claves `Date + Location` repetidas** |
| **Tratamiento de faltantes** | Sin generación de faltantes artificiales (la base original ya presenta `NA` en variables numéricas y categóricas; ver [`docs/decisiones.md`](decisiones.md)) |

### Problema estadístico

El problema central consiste en **analizar y modelar la ocurrencia de lluvia al día siguiente** (`RainTomorrow`, clasificación binaria `Yes`/`No`) a partir de observaciones meteorológicas diarias registradas a las 9:00 y 15:00 horas, junto con variables de ubicación y fecha.

- **Distribución de la variable objetivo (`RainTomorrow`):** Sobre **142.193** registros válidos (existen **3.267** faltantes, `2,25 %`), **110.316** corresponden a `No` (**77,58 %**) y **31.877** a `Yes` (**22,42 %**), evidenciando un desbalance moderado de clases.

---

## 2. Variables involucradas y clasificación estadística

Las 23 columnas de `data/raw/weatherAUS.csv` se clasifican según su naturaleza estadística, escala de medición, dominio observado y proporción de datos faltantes:

| Variable | Tipo estadístico | Escala de medición | Unidad / Dominio observado | Faltantes (`NA`) | Rol analítico |
|---|---|---|---|---:|---|
| `Date` | Temporal (fecha) | Intervalo calendario | `2007-11-01` a `2017-06-25` | 0 (0,00 %) | Índice temporal / estacionalidad |
| `Location` | Cualitativa nominal | Nominal | 49 estaciones meteorológicas | 0 (0,00 %) | Factor espacial / agrupación |
| `WindGustDir` | Cualitativa nominal (direccional) | Nominal / Circular | 16 puntos cardinales | 10.326 (7,10 %) | Explicativa direccional |
| `WindDir9am` | Cualitativa nominal (direccional) | Nominal / Circular | 16 puntos cardinales | 10.566 (7,26 %) | Explicativa direccional (9:00) |
| `WindDir3pm` | Cualitativa nominal (direccional) | Nominal / Circular | 16 puntos cardinales | 4.228 (2,91 %) | Explicativa direccional (15:00) |
| `RainToday` | Cualitativa dicotómica | Nominal binaria | `No` / `Yes` | 3.261 (2,24 %) | Explicativa binaria (persistencia) |
| `RainTomorrow` | Cualitativa dicotómica | Nominal binaria | `No` / `Yes` | 3.267 (2,25 %) | **Variable objetivo** |
| `Cloud9am` | Cuantitativa discreta | Discreta (ordinal) | `0` a `9` oktas | 55.888 (38,42 %) | Explicativa de nubosidad (9:00) |
| `Cloud3pm` | Cuantitativa discreta | Discreta (ordinal) | `0` a `9` oktas | 59.358 (40,81 %) | Explicativa de nubosidad (15:00) |
| `MinTemp` | Cuantitativa continua | Intervalo | `-8,5` a `33,9` °C | 1.485 (1,02 %) | Explicativa térmica mínima |
| `MaxTemp` | Cuantitativa continua | Intervalo | `-4,8` a `48,1` °C | 1.261 (0,87 %) | Explicativa térmica máxima |
| `Temp9am` | Cuantitativa continua | Intervalo | `-7,2` a `40,2` °C | 1.767 (1,21 %) | Explicativa térmica (9:00) |
| `Temp3pm` | Cuantitativa continua | Intervalo | `-5,4` a `46,7` °C | 3.609 (2,48 %) | Explicativa térmica (15:00) |
| `Pressure9am` | Cuantitativa continua | Intervalo | `980,5` a `1041,0` hPa | 15.065 (10,36 %) | Explicativa barométrica (9:00) |
| `Pressure3pm` | Cuantitativa continua | Intervalo | `977,1` a `1039,6` hPa | 15.028 (10,33 %) | Explicativa barométrica (15:00) |
| `Rainfall` | Cuantitativa continua | Razón (no negativa) | `0,0` a `371,0` mm | 3.261 (2,24 %) | Explicativa hidrológica |
| `Evaporation` | Cuantitativa continua | Razón (no negativa) | `0,0` a `145,0` mm | 62.790 (43,17 %) | Explicativa de evaporación |
| `Sunshine` | Cuantitativa continua | Razón (no negativa) | `0,0` a `14,5` horas | 69.835 (48,01 %) | Explicativa de insolación |
| `Humidity9am` | Cuantitativa continua | Razón (acotada) | `0` a `100` % | 2.654 (1,82 %) | Explicativa higrométrica (9:00) |
| `Humidity3pm` | Cuantitativa continua | Razón (acotada) | `0` a `100` % | 4.507 (3,10 %) | Explicativa higrométrica (15:00) |
| `WindGustSpeed` | Cuantitativa continua* | Razón (no negativa) | `6` a `135` km/h | 10.263 (7,06 %) | Explicativa de ráfaga máxima |
| `WindSpeed9am` | Cuantitativa continua* | Razón (no negativa) | `0` a `130` km/h | 1.767 (1,21 %) | Explicativa de viento (9:00) |
| `WindSpeed3pm` | Cuantitativa continua* | Razón (no negativa) | `0` a `87` km/h | 3.062 (2,11 %) | Explicativa de viento (15:00) |

> \* `WindGustSpeed`, `WindSpeed9am` y `WindSpeed3pm` se almacenan como enteros en el CSV, pero representan magnitudes físicas continuas. En `Cloud9am` y `Cloud3pm`, la escala en oktas va de `0` a `8`, reservándose `9` para cielo oscurecido/no observable.

---

## 3. Relaciones preliminares identificadas

A partir de la exploración empírica documentada en [`notebooks/formativa_1.ipynb`](../notebooks/formativa_1.ipynb) y [`notebooks/estadistica_descriptiva_y_graficos.ipynb`](../notebooks/estadistica_descriptiva_y_graficos.ipynb), se observan los siguientes patrones:

1. **Multicolinealidad entre pares intra-día y térmicos:**
   - `MaxTemp` y `Temp3pm` muestran una correlación lineal muy elevada ($r = 0{,}985$, $n = 141.589$), al igual que `Pressure9am` y `Pressure3pm` ($r = 0{,}961$, $n = 130.171$) y `MinTemp` con `Temp9am` ($r = 0{,}902$, $n = 143.382$).
   - `WindGustSpeed` y `WindSpeed3pm` ($r = 0{,}686$), así como `Humidity9am` y `Humidity3pm` ($r = 0{,}667$), presentan asociaciones positivas moderadas-altas.
2. **Relaciones físicas inversas:**
   - Mayor nubosidad vespertina (`Cloud3pm`) se asocia con menos horas de sol (`Sunshine`: $r = -0{,}704$, $n = 65.253$).
   - Mayor humedad a las 15:00 (`Humidity3pm`) se asocia negativamente con `Sunshine` ($r = -0{,}629$, $n = 74.497$) y con `Temp3pm` ($r = -0{,}558$, $n = 140.953$).
3. **Diferencias frente a la variable objetivo (`RainTomorrow`):**
   - Los días previos a lluvia (`RainTomorrow = Yes`) registran en promedio mayor humedad vespertina (`Humidity3pm`: **68,80 %** vs. **46,51 %**), mayor nubosidad (`Cloud3pm`: **6,36** vs. **3,92** oktas), menos insolación (`Sunshine`: **4,47** vs. **8,55** h), menor presión (`Pressure3pm`: **1012,30** vs. **1016,11** hPa), menor temperatura (`Temp3pm`: **19,20** vs. **22,40** °C) y mayor precipitación previa (`Rainfall`: **6,14** vs. **1,27** mm).
   - `Rainfall` presenta fuerte asimetría positiva y acumulación en cero (mediana = `0 mm`, media = `2,36 mm`, máximo = `371 mm`).
4. **Persistencia temporal (`RainToday` → `RainTomorrow`):**
   - Cuando `RainToday = No`, la proporción observada de `RainTomorrow = Yes` es de **15,19 %** (16.604 de 109.332 casos válidos); cuando `RainToday = Yes`, asciende a **46,41 %** (14.597 de 31.455 casos válidos).
5. **Heterogeneidad espacial y estacionalidad:**
   - Las tasas de lluvia, rangos térmicos y presencia de `NA` (especialmente en `Sunshine`, `Evaporation`, `Cloud9am` y `Cloud3pm`, con 38 %–48 % de ausencia) varían según la estación (`Location`) y la época del año (`Date`), por lo que ambos factores deben considerarse en pruebas estadísticas y modelos posteriores.
