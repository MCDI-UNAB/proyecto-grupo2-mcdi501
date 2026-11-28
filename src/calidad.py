"""Carga y calidad de los datos de Rain in Australia (tarea 1.1).

Uso desde un notebook:

    from src.calidad import cargar_datos
    datos = cargar_datos()

La carga verifica el SHA-256 del archivo fuente (raw) y solo convierte tipos:
no elimina filas, no imputa y no modifica valores.
"""
import hashlib
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RUTA_RAW = RAIZ / "data" / "raw" / "weatherAUS.csv"
SHA256_RAW = "573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014"
DIMENSIONES = (145_460, 23)

RUMBOS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
          "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
DIRECCIONES = ["WindGustDir", "WindDir9am", "WindDir3pm"]
LLUVIA = ["RainToday", "RainTomorrow"]

# Variable: (tipo estadístico, escala, unidad)
CLASIFICACION = {
    "Date": ("Fecha", "Intervalo", "día"),
    "Location": ("Cualitativa nominal", "Nominal", "ubicación"),
    "MinTemp": ("Cuantitativa continua", "Intervalo", "°C"),
    "MaxTemp": ("Cuantitativa continua", "Intervalo", "°C"),
    "Rainfall": ("Cuantitativa continua", "Razón", "mm"),
    "Evaporation": ("Cuantitativa continua", "Razón", "mm"),
    "Sunshine": ("Cuantitativa continua", "Razón", "horas"),
    "WindGustDir": ("Cualitativa nominal", "Nominal circular", "16 rumbos"),
    "WindGustSpeed": ("Cuantitativa continua", "Razón", "km/h"),
    "WindDir9am": ("Cualitativa nominal", "Nominal circular", "16 rumbos"),
    "WindDir3pm": ("Cualitativa nominal", "Nominal circular", "16 rumbos"),
    "WindSpeed9am": ("Cuantitativa continua", "Razón", "km/h"),
    "WindSpeed3pm": ("Cuantitativa continua", "Razón", "km/h"),
    "Humidity9am": ("Cuantitativa continua", "Razón", "%"),
    "Humidity3pm": ("Cuantitativa continua", "Razón", "%"),
    "Pressure9am": ("Cuantitativa continua", "Razón", "hPa"),
    "Pressure3pm": ("Cuantitativa continua", "Razón", "hPa"),
    "Cloud9am": ("Cuantitativa discreta", "Ordinal", "oktas"),
    "Cloud3pm": ("Cuantitativa discreta", "Ordinal", "oktas"),
    "Temp9am": ("Cuantitativa continua", "Intervalo", "°C"),
    "Temp3pm": ("Cuantitativa continua", "Intervalo", "°C"),
    "RainToday": ("Cualitativa binaria", "Nominal", "No / Yes"),
    "RainTomorrow": ("Cualitativa binaria (objetivo)", "Nominal", "No / Yes"),
}


def sha256_archivo(ruta):
    """SHA-256 de un archivo, leído por bloques."""
    resumen = hashlib.sha256()
    with open(ruta, "rb") as archivo:
        for bloque in iter(lambda: archivo.read(1 << 20), b""):
            resumen.update(bloque)
    return resumen.hexdigest()


def cargar_datos(ruta=RUTA_RAW):
    """Verifica el raw y lo carga con la fecha y las categóricas tipadas."""
    ruta = Path(ruta)
    if not ruta.is_file():
        raise FileNotFoundError(f"Falta {ruta}. Ver data/raw/README.md.")
    if sha256_archivo(ruta) != SHA256_RAW:
        raise ValueError(f"El SHA-256 de {ruta.name} no coincide. Ver data/raw/README.md.")
    datos = pd.read_csv(ruta, parse_dates=["Date"])
    if datos.shape != DIMENSIONES:
        raise ValueError(f"Dimensiones inesperadas: {datos.shape}")
    datos["Location"] = datos["Location"].astype("category")
    for columna in DIRECCIONES:
        datos[columna] = datos[columna].astype(pd.CategoricalDtype(RUMBOS))
    for columna in LLUVIA:
        datos[columna] = datos[columna].astype(pd.CategoricalDtype(["No", "Yes"]))
    return datos


def clasificacion_variables():
    """Tipo, escala y unidad de las 23 variables."""
    tabla = pd.DataFrame.from_dict(
        CLASIFICACION, orient="index", columns=["Tipo", "Escala", "Unidad"])
    tabla.index.name = "Variable"
    return tabla


def faltantes_por_ubicacion(datos):
    """Porcentaje de faltantes de cada variable en cada ubicación."""
    variables = datos.drop(columns=["Date", "Location"])
    return variables.isna().groupby(datos["Location"], observed=True).mean().mul(100)


def ubicaciones_sin_registro(datos, variables):
    """Cuántas ubicaciones nunca registran la variable y qué parte de sus faltantes explican."""
    por_ubicacion = faltantes_por_ubicacion(datos)
    filas = []
    for variable in variables:
        sin_dato = por_ubicacion.index[por_ubicacion[variable] == 100]
        total = datos[variable].isna().sum()
        explicados = datos.loc[datos["Location"].isin(sin_dato), variable].isna().sum()
        filas.append({"Variable": variable, "Ubicaciones sin ningún registro": len(sin_dato),
                      "Faltantes": total, "% de los faltantes que explican": 100 * explicados / total})
    return pd.DataFrame(filas).set_index("Variable")


def huecos_calendario(datos):
    """Días sin fila entre la primera y la última fecha de cada ubicación."""
    resumen = datos.groupby("Location", observed=True)["Date"].agg(["min", "max", "count"])
    resumen["Días del periodo"] = (resumen["max"] - resumen["min"]).dt.days + 1
    resumen["Días sin fila"] = resumen["Días del periodo"] - resumen["count"]
    resumen = resumen.rename(columns={"min": "Primera fecha", "max": "Última fecha", "count": "Filas"})
    return resumen.sort_values("Días sin fila", ascending=False)


def marcar_inconsistencias(datos):
    """Una columna booleana por regla; True indica una fila para revisar."""
    d = datos
    return pd.DataFrame({
        "min_mayor_que_max": d["MinTemp"] > d["MaxTemp"],
        "temp9am_fuera_de_rango": (d["Temp9am"] < d["MinTemp"]) | (d["Temp9am"] > d["MaxTemp"]),
        "temp3pm_fuera_de_rango": (d["Temp3pm"] < d["MinTemp"]) | (d["Temp3pm"] > d["MaxTemp"]),
        "rafaga_menor_que_velocidad": (d["WindGustSpeed"] < d["WindSpeed9am"])
                                      | (d["WindGustSpeed"] < d["WindSpeed3pm"]),
        "nubosidad_9": (d["Cloud9am"] == 9) | (d["Cloud3pm"] == 9),
    }, index=d.index)


def reglas_de_consistencia(datos):
    """Filas evaluadas y filas que incumplen cada regla de dominio o de coherencia."""
    d = datos
    siguiente = d.sort_values(["Location", "Date"])
    despues = siguiente.groupby("Location", observed=True)[["Date", "RainToday"]].shift(-1)
    pares = ((despues["Date"] - siguiente["Date"]).dt.days.eq(1)
             & siguiente["RainTomorrow"].notna() & despues["RainToday"].notna())
    distintos = siguiente.loc[pares, "RainTomorrow"].astype(str) != despues.loc[pares, "RainToday"].astype(str)

    filas = []

    def regla(nombre, evaluadas, incumplen):
        filas.append({"Regla": nombre, "Filas evaluadas": int(evaluadas.sum()),
                      "Filas que la incumplen": int((evaluadas & incumplen).sum())})

    def presentes(*columnas):
        return d[list(columnas)].notna().all(axis=1)

    for columna in ["Humidity9am", "Humidity3pm"]:
        regla(f"{columna} entre 0 y 100", presentes(columna), ~d[columna].between(0, 100))
    for columna in ["Rainfall", "Evaporation", "Sunshine", "WindGustSpeed", "WindSpeed9am", "WindSpeed3pm"]:
        regla(f"{columna} no negativa", presentes(columna), d[columna] < 0)
    marcas = marcar_inconsistencias(d)
    regla("MinTemp no supera a MaxTemp", presentes("MinTemp", "MaxTemp"), marcas["min_mayor_que_max"])
    for hora in ["9am", "3pm"]:
        regla(f"Temp{hora} dentro de [MinTemp, MaxTemp]",
              presentes(f"Temp{hora}") & d[["MinTemp", "MaxTemp"]].notna().any(axis=1),
              marcas[f"temp{hora}_fuera_de_rango"])
    regla("Ráfaga no menor que las velocidades de 9:00 y 15:00",
          presentes("WindGustSpeed") & d[["WindSpeed9am", "WindSpeed3pm"]].notna().any(axis=1),
          marcas["rafaga_menor_que_velocidad"])
    regla("Nubosidad entre 0 y 8 oktas", d[["Cloud9am", "Cloud3pm"]].notna().any(axis=1), marcas["nubosidad_9"])
    regla("RainToday = Yes solo si Rainfall > 1 mm", presentes("Rainfall", "RainToday"),
          (d["Rainfall"] > 1) != (d["RainToday"] == "Yes"))
    filas.append({"Regla": "RainTomorrow igual a RainToday del día siguiente",
                  "Filas evaluadas": int(pares.sum()), "Filas que la incumplen": int(distintos.sum())})
    return pd.DataFrame(filas).set_index("Regla")


def valores_extremos(datos):
    """Valores fuera de 1,5 veces el rango intercuartílico (regla de Tukey)."""
    numericas = datos.select_dtypes("number")
    q1, q3 = numericas.quantile(0.25), numericas.quantile(0.75)
    inferior, superior = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    fuera = numericas.lt(inferior) | numericas.gt(superior)
    tabla = pd.DataFrame({
        "Mínimo": numericas.min(), "Límite inferior": inferior,
        "Límite superior": superior, "Máximo": numericas.max(),
        "Valores fuera de límites": fuera.sum(),
        "% de los válidos": 100 * fuera.sum() / numericas.count(),
    })
    tabla.index.name = "Variable"
    return tabla


def reporte_calidad(datos):
    """Una fila por variable: tipo, escala, completitud, cardinalidad y rango."""
    reporte = clasificacion_variables().loc[datos.columns]
    reporte["Válidos"] = datos.count()
    reporte["Faltantes"] = datos.isna().sum()
    reporte["% faltantes"] = 100 * datos.isna().mean()
    reporte["Valores distintos"] = datos.nunique()
    ordenables = ["Date", *datos.select_dtypes("number").columns]
    reporte["Mínimo"] = pd.Series({c: datos[c].min() for c in ordenables}, dtype=object)
    reporte["Máximo"] = pd.Series({c: datos[c].max() for c in ordenables}, dtype=object)
    reporte.loc["Date", ["Mínimo", "Máximo"]] = [f"{datos['Date'].min():%Y-%m-%d}", f"{datos['Date'].max():%Y-%m-%d}"]
    extremos = valores_extremos(datos)
    reporte["Fuera de 1,5·RIC"] = extremos["Valores fuera de límites"].reindex(reporte.index).astype("Int64")
    reporte.index.name = "Variable"
    return reporte
