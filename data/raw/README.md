# Archivo fuente (raw)

**Rain in Australia**, base 1 del apunte del curso «Bases de datos disponibles para el proyecto». Cerca de 10 años de observaciones meteorológicas diarias de estaciones de Australia. Variable a predecir: si lloverá al día siguiente.

El archivo **no se versiona**. Cada integrante lo descarga y lo deja en esta carpeta como `data/raw/weatherAUS.csv`.

| Dato | Valor |
|---|---|
| Fuente | <https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package/data> |
| Archivo | `weatherAUS.csv` (separador `,`, UTF-8, saltos de línea LF; 14.094.055 bytes) |
| Filas y columnas | 145.460 filas y 23 columnas; 49 estaciones, del 1 nov 2007 al 25 jun 2017 |
| Versión | la de Kaggle actualizada el 11 dic 2020, descargada el 26 nov 2026 |
| SHA-256 | `573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014` |

## Opciones de descarga

Los comandos se ejecutan desde la raíz del repositorio.

### Opción A: terminal en macOS, Linux o Git Bash (sin cuenta)

```bash
curl -L -o data/raw/weather-dataset-rattle-package.zip \
  https://www.kaggle.com/api/v1/datasets/download/jsphyg/weather-dataset-rattle-package
unzip data/raw/weather-dataset-rattle-package.zip weatherAUS.csv -d data/raw/
```

### Opción B: PowerShell en Windows (sin cuenta)

```powershell
curl.exe -L -o data\raw\weather-dataset-rattle-package.zip https://www.kaggle.com/api/v1/datasets/download/jsphyg/weather-dataset-rattle-package
Expand-Archive data\raw\weather-dataset-rattle-package.zip -DestinationPath data\raw
```

### Opción C: navegador (con cuenta de Kaggle)

1. Abrir la [página del dataset](https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package/data) y usar **Download**.
2. Descomprimir el archivo y dejar `weatherAUS.csv` directamente en `data/raw/`, sin subcarpetas.

## Verificación

```bash
shasum -a 256 data/raw/weatherAUS.csv        # macOS
sha256sum data/raw/weatherAUS.csv            # Linux o Git Bash
```

```powershell
Get-FileHash data\raw\weatherAUS.csv -Algorithm SHA256
```

El resultado debe ser el SHA-256 de la tabla (PowerShell lo muestra en mayúsculas). Si es distinto, el archivo cambió: borrarlo y descargarlo de nuevo. No guardarlo con Excel. Las versiones limpias van en `data/processed/`.

La base trae faltantes en varias variables numéricas, por lo que no se generan faltantes artificiales.

## Origen y condiciones de uso

- Fuente y custodio de los datos: Bureau of Meteorology, © Commonwealth of Australia (<http://www.bom.gov.au/climate/data>).
- Compilación: Graham Williams, proyecto Rattle. Publicación en Kaggle: Joe Young.
- La descripción en Kaggle indica «Copyright Commonwealth of Australia 2010, Bureau of Meteorology» y no declara una licencia de redistribución.
- La [página de copyright del Bureau](https://www.bom.gov.au/copyright) señala que, si no se declaran otras condiciones, el contenido puede descargarse y usarse, pero no entregarse a terceros ni usarse comercialmente.
