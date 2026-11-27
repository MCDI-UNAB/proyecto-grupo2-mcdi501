# proyecto-grupo2-mcdi501

Estadística Computacional para la Toma de Decisiones (MCDI501) · Magíster en Ciencia de Datos e Inteligencia Artificial, UNAB.

**Grupo 2:** Bertgil González Olmos, Daniel Rojas Sánchez, Christian Siebert Aguilera y Oscar Salgado Sanhueza.

## Entregas

| Entrega | Plazo del grupo |
|---|---|
| Formativa 1 (ensayo de la Sumativa 1) | 27 nov 2026 |
| Sumativa 1 | 2 dic 2026 |
| Sumativa 2 | 6 dic 2026 |
| Sumativa 3 | 13 dic 2026 |

## Datos

Dataset: **Rain in Australia** (base 1 del apunte del curso), clasificación binaria sobre si lloverá al día siguiente. El archivo fuente (raw) no se versiona: cada integrante lo descarga en `data/raw/` y comprueba su SHA-256, como explica [`data/raw/README.md`](data/raw/README.md).

## Entorno

Requiere Python 3.12.

```bash
python3.12 -m venv .venv
source .venv/bin/activate            # Windows (Git Bash): source .venv/Scripts/activate
pip install -r requirements.txt
python -m ipykernel install --user --name grupo2-mcdi501 --display-name "Python (grupo2-mcdi501)"
jupyter lab
```

## Estructura

```text
data/raw/         archivo fuente (raw); solo se versiona su README
data/processed/   salidas que reutilizan las siguientes sumativas
notebooks/        notebooks de cada entrega
src/              funciones que usan los notebooks
docs/             decisiones del grupo
informes/         PDF entregados
```

## Forma de trabajo

1. Antes del primer commit, configurar la identidad con el correo `noreply` propio (está en `.mailmap`):
   ```bash
   git config user.name "Nombre Apellido"
   git config user.email "ID+usuario@users.noreply.github.com"
   ```
2. Una rama por tarea (`feat-descriptiva`, `feat-intervalos`) y un pull request a `main`. Los merges los hace Oscar.
3. Commits con prefijo y cambio: `ADD intervalos de confianza`, `UPDATE …`, `FIX …`.
4. Cada persona escribe sus funciones en su archivo de `src/`; cada notebook lo edita una sola persona.
5. Semilla fija: 42.
6. No modificar `data/raw/` ni abrir y guardar sus CSV con Excel; las salidas van en `data/processed/`.
