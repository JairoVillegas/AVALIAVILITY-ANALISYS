import json
import os

file_path = r"C:\Users\jairo\OneDrive - Pontificia Universidad Javeriana\Desktop\RAPPI_MAKERS\PROYECTO\BLOQUE_1\NOTEBOOKS\CRISP-DM.ipynb"

if not os.path.exists(file_path):
    print("Error: file not found.")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

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

add_markdown("""# 3. Data Preparation
## 3.1 Consolidación de todos los archivos CSV históricos
Dado que tenemos una gran cantidad de archivos CSV segmentados, la siguiente función se encarga de iterar sobre el directorio entero, aplicar el pipeling de transformación (Wide-to-Long) en cada unidad, y luego unir el universo completo en un solo DataFrame de pandas.""")

add_code("""import glob
import os

raw_data_dir = r'../../../DATOS/DATOS_CRUDOS/'
# Hacemos la busqueda de todos los archivos que coincidan
all_files = glob.glob(os.path.join(raw_data_dir, "AVAILABILITY-data*.csv"))

print(f"Encontrados {len(all_files)} archivos para consolidar.")

dfs_list = []
id_cols = ['Plot name', 'metric (sf_metric)', 'Value Prefix', 'Value Suffix']

for file in all_files:
    try:
        # 1. Lectura del CSV temporal
        df_temp = pd.read_csv(file)
        
        # 2. Hacer el pivot (Wide a Long)
        df_melted = pd.melt(df_temp, id_vars=id_cols, var_name='timestamp_raw', value_name='visible_stores')
        
        # 3. Extracción de zona horaria y casting a Datetime
        df_melted['timestamp_raw'] = df_melted['timestamp_raw'].str.extract(r'(.* GMT[+-]\\d{4})')[0]
        # Coerce es útil por si algún registro de un CSV corrupto no puede convertirse
        df_melted['timestamp'] = pd.to_datetime(df_melted['timestamp_raw'], format='%a %b %d %Y %H:%M:%S GMT%z', errors='coerce')
        
        # 4. Quedarnos únicamente con timestamp y métrica, y descartar NAs si los hay
        df_melted = df_melted[['timestamp', 'visible_stores']].dropna()
        
        # 5. Volcar a la matriz principal
        dfs_list.append(df_melted)
        
    except Exception as e:
        print(f"Error procesando el archivo {os.path.basename(file)}: {e}")

# 6. Concatenar los 200+ archivos
print("Concatenando todos los registros... esto puede tomar un poco.")
df_consolidado = pd.concat(dfs_list, ignore_index=True)

# 7. Eliminar si hay tiempos duplicados entre archivos (snapshots traslapados)
df_consolidado.drop_duplicates(subset=['timestamp'], inplace=True)

# 8. Ordenar cronológicamente para que la serie de tiempo tenga coherencia y reset del index
df_consolidado.sort_values('timestamp', inplace=True)
df_consolidado.reset_index(drop=True, inplace=True)

print(f"Dimensión final del Dataset Consolidado: {df_consolidado.shape}")
df_consolidado.head()""")

add_markdown("""## 3.2 Limpieza y tratamiento de ruido
Garantizamos tipologías correctas para las columnas.""")

add_code("""# Convertir a numérico estricto y luego forzar Int64 (ya que son conteos de tiendas)
df_consolidado['visible_stores'] = pd.to_numeric(df_consolidado['visible_stores'], errors='coerce')
df_consolidado = df_consolidado.dropna()

# Cast int
df_consolidado['visible_stores'] = df_consolidado['visible_stores'].astype(int)

df_consolidado.info()""")

add_markdown("""## 3.3 Guardar el Output Final Procesado
Enviamos esta base de datos consolidada a `DATOS_PROCESADOS`. 
Este archivo consolida **todo el esfuerzo de preparación de la data** y es el Dataset Entregable de la Fase 1 que luego ingestaremos en la Web (Fase 2) y usaremos de contexto para la IA (Fase 3).""")

add_code("""processed_dir = r'../../../DATOS/DATOS_PROCESADOS/'
os.makedirs(processed_dir, exist_ok=True)

output_path = os.path.join(processed_dir, 'AVAILABILITY-procesado.csv')
df_consolidado.to_csv(output_path, index=False)

print(f"¡Dataset estructurado, procesado y consolidado guardado exitosamente!\\nRuta: {output_path}")""")

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook updated successfully with Data Preparation.")
