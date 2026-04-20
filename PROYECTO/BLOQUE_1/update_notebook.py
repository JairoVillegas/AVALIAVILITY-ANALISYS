import json
import os

file_path = r"C:\Users\jairo\OneDrive - Pontificia Universidad Javeriana\Desktop\RAPPI_MAKERS\PROYECTO\BLOQUE_1\NOTEBOOKS\CRISP-DM.ipynb"

if not os.path.exists(file_path):
    print("Error: file not found.")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Reemplazamos la última celda si tenía el texto 'imp'
last_cell = nb['cells'][-1]
if ''.join(last_cell['source']).strip() == 'imp':
    last_cell['cell_type'] = 'code'
    last_cell['source'] = [
        "import pandas as pd\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "# Configuración visual\n",
        "sns.set_theme(style='whitegrid', palette='muted')\n",
        "plt.rcParams['figure.figsize'] = (12, 6)"
    ]
    if 'execution_count' not in last_cell:
        last_cell['execution_count'] = None
    if 'outputs' not in last_cell:
        last_cell['outputs'] = []

def add_markdown(text):
    nb['cells'].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" if i < len(text.split("\n"))-1 else line for i, line in enumerate(text.split("\n"))]
    })

def add_code(text):
    nb['cells'].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" if i < len(text.split("\n"))-1 else line for i, line in enumerate(text.split("\n"))]
    })

add_markdown("""## 2.1 Carga de datos
Cargaremos el archivo histórico de disponibilidad. El archivo CSV proporcionado tiene una estructura "ancha" (wide format) donde cada columna representa un timestamp de muestreo y la fila contiene los valores, esto suele ser un export directo de herramientas de monitoreo.""")

add_code("""file_path = r'../../../DATOS/DATOS_CRUDOS/AVAILABILITY-data.csv'
df_raw = pd.read_csv(file_path)

print(f'Dimensiones del dataset original: {df_raw.shape}')
# Mostramos la cabecera y 10 primeras columnas de tiempo
df_raw.iloc[:, :10].head()""")

add_markdown("""## 2.2 Transformación Inicial (Melt)
Para realizar un análisis temporal y estadístico adecuado, requerimos que los datos tengan una estructura larga (long format) donde cada registro sea la combinación `(timestamp, visible_stores)`.""")

add_code("""id_cols = ['Plot name', 'metric (sf_metric)', 'Value Prefix', 'Value Suffix']

# Hacemos un melt para bajar los timestamps a filas
df_long = pd.melt(df_raw, id_vars=id_cols, var_name='timestamp_raw', value_name='visible_stores')

# Limpiamos el texto del timestamp usando una expresión regular para remover "(hora estándar de Colombia)" y dejar el timezone "+-0500"
df_long['timestamp_raw'] = df_long['timestamp_raw'].str.extract(r'(.* GMT[+-]\\d{4})')[0]

# Parseamos a Datetime indicando el format string exacto
df_long['timestamp'] = pd.to_datetime(df_long['timestamp_raw'], format='%a %b %d %Y %H:%M:%S GMT%z')

# Nos quedamos con las columnas útiles
df_clean = df_long[['timestamp', 'visible_stores']].copy()

# Ordenamos obligatoriamente por fecha para el EDA
df_clean.sort_values('timestamp', inplace=True)
df_clean.reset_index(drop=True, inplace=True)

df_clean.head()""")

add_markdown("""## 2.3 Exploración Básica (EDA)
Una vez transformada la data, validaremos nulos, la completitud de la medición y estadísticas básicas.""")

add_code("""df_clean.info()""")

add_code("""# Revisar las analíticas descriptivas
df_clean.describe()""")

add_code("""# Verificamos si hay nulos creados durante el pivoting o por falta de datos
print("Valores nulos en el dataset:")
print(df_clean.isnull().sum())""")

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook updated successfully.")
