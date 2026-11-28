# Decisiones del grupo

Cada decisión registra el problema, lo que se decidió y por qué.

## 1. Dataset: Rain in Australia

- **Decisión:** base 1 del apunte del curso (clasificación binaria: si lloverá al día siguiente). Se usa en la Formativa 1 y en las sumativas.
- **Archivo fuente (raw):** no se versiona. Las [condiciones del Bureau of Meteorology](https://www.bom.gov.au/copyright), cuando no declaran otras, permiten usar el contenido pero no entregarlo a terceros, y la fuente en Kaggle no declara una licencia que lo permita. Cada integrante lo descarga y verifica su SHA-256.
- **A considerar:** faltantes en varias variables numéricas, posible estacionalidad, diferencias entre ubicaciones y tamaño grande, según el apunte.

## 2. Datos faltantes: no se generan artificiales

La base ya tiene faltantes en variables numéricas, y el apunte indica que en ese caso no se aplica la regla de generación.

## 3. Variables para los intervalos y pruebas de hipótesis

- **Problema:** definir con qué variables y pruebas analizar las condiciones asociadas a la lluvia del día siguiente.
- **Intervalos:** media e intervalo t al 95 % de `MaxTemp`, `Humidity3pm` y `Pressure3pm`.

| Variable | Por qué se elige | Media si no llueve al día siguiente | Media si llueve | Faltantes |
|---|---|---|---|---|
| `MaxTemp` (°C) | Condición térmica del día | 23,84 | 21,12 | 0,87 % |
| `Humidity3pm` (%) | Humedad de la tarde; muestra una diferencia marcada entre grupos | 46,51 | 68,80 | 3,10 % |
| `Pressure3pm` (hPa) | Condición barométrica de la tarde | 1.016,11 | 1.012,30 | 10,33 % |

- **Prueba 1, t de Welch bilateral:** `Humidity3pm` según `RainTomorrow`. H₀: las medias son iguales; H₁: difieren. Compara una variable numérica entre dos grupos sin suponer varianzas iguales. Se informa la d de Cohen y el intervalo al 95 % de la diferencia de medias.
- **Prueba 2, χ² de independencia sin corrección de Yates:** `RainToday` con `RainTomorrow`. H₀: son independientes; H₁: están asociadas. Ambas variables son categóricas. Se informa la V de Cramér.
- **Significancia:** α = 0,05, nivel convencional para un análisis exploratorio; limita a 5 % la probabilidad de rechazar una H₀ verdadera si se cumplen los supuestos. Con más de 138.000 registros por prueba, la conclusión se apoya además en el tamaño del efecto.
- **Supuestos a verificar:** en Welch, que la aproximación normal de las medias sea razonable por el tamaño de los grupos y su asimetría; en χ², frecuencias esperadas de al menos 5. En ambas, independencia entre observaciones.
- **Limitaciones:** los días consecutivos y las ubicaciones cercanas pueden estar correlacionados. Las pruebas se eligieron después de explorar estos mismos datos, por lo que se interpretan como exploratorias.
