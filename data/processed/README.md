# Datos procesados

Resúmenes generados por el código que reutilizan las siguientes sumativas: calidad y faltantes, parámetros e intervalos y valores p.

Aquí solo se versionan resúmenes agregados. La base fila a fila no se guarda, porque las condiciones de los datos no permiten redistribuirla (ver `data/raw/README.md`): se obtiene con `cargar_datos()` de `src/calidad.py`.

Cada archivo se anota aquí con el notebook que lo genera.

| Archivo | Contenido | Notebook |
|---|---|---|
| `calidad_variables.csv` | Tipo, escala, completitud, rango y valores extremos de cada variable | `s1_carga_y_calidad.ipynb` |
| `calidad_faltantes_por_ubicacion.csv` | Porcentaje de faltantes por variable y ubicación | `s1_carga_y_calidad.ipynb` |
| `calidad_reglas_consistencia.csv` | Filas evaluadas y filas que incumplen cada regla | `s1_carga_y_calidad.ipynb` |
