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

add_markdown("""## 3.4 Feature Engineering (Datasets Listos para Modeling)
Las ideas presentadas a nivel de negocio para el modelo (K-Means por días, series de tiempo ARMA/Prophet) son muy acertadas. Para lograrlo directamente en la fase de **Modeling**, dejaremos ya pre-construidos y procesados tres (3) configuraciones del dataset:

1. **Dataset con Features Temporales Geocéntricos**: Extracción de franjas horarias y días clave.
2. **Dataset Resampleado (Serie temporal)**: Consolidación por horas y suavizado para algoritmos Autoregresivos.
3. **Dataset de Perfiles Diarios (Clustering)**: Forma pivotada de horas horizontales por día (24 columnas) listo para ser ingerido por K-Means.""")

add_code("""import warnings
warnings.filterwarnings('ignore')

# 1. Feature Engineering: Variables temporales
df_features = df_consolidado.copy()

# Extracción de características
df_features['hour'] = df_features['timestamp'].dt.hour
df_features['day_of_week'] = df_features['timestamp'].dt.dayofweek
df_features['is_weekend'] = df_features['day_of_week'].isin([5, 6]).astype(int)
df_features['date'] = df_features['timestamp'].dt.date

# Crear Franjas Horarias
bins = [0, 6, 12, 18, 24]
labels = ['Madrugada', 'Mañana', 'Tarde', 'Noche']
# Usamos right=False para que 06:00 pertenezca a 'Mañana' y no 'Madrugada'
df_features['time_band'] = pd.cut(df_features['hour'], bins=bins, labels=labels, right=False)

df_features.head()""")

add_markdown("""### Generación de Datasets Estructurales para Modelos""")

add_code("""# A) Dataset de Serie de Tiempo (Remuestreo)
# Para modelado autorregresivo nos sirve que las observaciones sean equidistantes en el tiempo.
# Agruparemos (resample) por 1 HORA y promediaremos la cantidad para suavizar el ruido de la medición corta.

df_hourly = df_features.set_index('timestamp').resample('1h')['visible_stores'].mean().reset_index()

# Si algún tramo en la noche no tuvo data y quedo NaN, lo rellenamos interpolando linealmente.
# Usamos bfill() o ffill() o interpolate() para mayor precisión.
df_hourly['visible_stores'] = df_hourly['visible_stores'].interpolate(method='linear')
df_hourly.dropna(inplace=True)
df_hourly['visible_stores'] = df_hourly['visible_stores'].round(0).astype("Int64")

print(f"Dataset Autorregresivo (Horario): {df_hourly.shape}")
df_hourly.head()""")

add_code("""# B) Dataset de Perfiles Diarios para Clustering (K-Means)
# Transformamos a un data-frame donde las columnas son '0'...'23' (las horas de un dia). 
# Cada Fila es una fecha y muestra el comportamiento de tiendas en todo el transcurso del día.

df_clustering = df_features.pivot_table(
    index='date', 
    columns='hour', 
    values='visible_stores', 
    aggfunc='mean'
)

# Rellenar posibles gaps de horas faltantes interpolando vecinos del mismo día, o usando el día anterior.
df_clustering = df_clustering.ffill(axis=1).bfill(axis=1)
df_clustering = df_clustering.round(0).astype("Int64")

print(f"Dataset Perfil de Días (Clustering): {df_clustering.shape}")
df_clustering.head()""")

add_code("""# C) Exportar configuraciones experimentales a PROCESADOS
path_base = r'../../../DATOS/DATOS_PROCESADOS/'
os.makedirs(path_base, exist_ok=True)

# 1. Base enriquecida 
df_features.to_csv(os.path.join(path_base, 'AVAILABILITY-features.csv'), index=False)
# 2. Serie temporal
df_hourly.to_csv(os.path.join(path_base, 'AVAILABILITY-hourly.csv'), index=False)
# 3. Datos vectorizados para clusters
df_clustering.to_csv(os.path.join(path_base, 'AVAILABILITY-clustering.csv'))

print("✅ Todos los Datasets estructurales para la fase 'Modeling' han sido exportados correctamente.")""")

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook updated successfully with Feature Engineering.")
