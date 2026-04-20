import json
import os

file_path = r"C:\Users\jairo\OneDrive - Pontificia Universidad Javeriana\Desktop\RAPPI_MAKERS\PROYECTO\BLOQUE_1\NOTEBOOKS\CRISP-DM.ipynb"

if not os.path.exists(file_path):
    print("Error: file not found.")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

def add_markdown(text):
    nb['cells'].append({"cell_type": "markdown", "metadata": {}, "source": [line + "\n" if i < len(text.split("\n"))-1 else line for i, line in enumerate(text.split("\n"))]})

def add_code(text):
    nb['cells'].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + "\n" if i < len(text.split("\n"))-1 else line for i, line in enumerate(text.split("\n"))]})

add_markdown("""# 4. Modeling (K-Means Clustering)
Siguiendo la metodología analítica, comenzaremos implementando los algoritmos de **Machine Learning No Supervisado**.
Cargaremos nuestro dataset especializado `AVAILABILITY-clustering.csv` para agrupar los días históricos bajo perfiles de comportamiento similares, descubriendo así los "Tipos de días" operacionales para Rappi.""")

add_code("""from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# Leemos el archivo donde el índex es la fecha (primera columna) y las demás son las horas(0-23)
df_clustering = pd.read_csv('../../../DATOS/DATOS_PROCESADOS/AVAILABILITY-clustering.csv', index_col=0)
print(f"Dimensiones del dataset de clustering: {df_clustering.shape}")

# K-Means es un algoritmo basado en distancias euclidianas. Estandarizamos las magnitudes horarias:
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clustering)
print("Data métrica (escalada) preparada para ingresar a los modelos.")""")

add_markdown("""## 4.1 Selección del Número Óptimo de Clusters (Elbow Method)
Iteraremos entrenamientos variando el número total de Clusters `k` para graficar la inercia interna del modelo y buscar un 'quiebre de codo' matemático.""")

add_code("""wcss = []
k_range = range(1, 10)

for k in k_range:
    kmeans_temp = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
    kmeans_temp.fit(X_scaled)
    wcss.append(kmeans_temp.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(k_range, wcss, marker='o', linestyle='-', color='indigo')
plt.title('Método del Codo para Identificar Agrupaciones')
plt.xlabel('Número Estipulado de Clusters (k)')
plt.ylabel('Inercia (WCSS)')
plt.xticks(k_range)
plt.grid(True)
plt.show()""")

add_markdown("""## 4.2 Entrenamiento del Modelo y Visualización de las 24 Dimensiones
En general, los quiebres en series horarias operacionales suelen situarse tras `k=3` o `4`. Asumiremos `k=3` para este análisis preliminar (puedes ajustar esta variable tras ver el codo si prefieres).""")

add_code("""k_optimo = 3
kmeans = KMeans(n_clusters=k_optimo, init='k-means++', random_state=42, n_init=10)
df_clustering['cluster'] = kmeans.fit_predict(X_scaled)

# Extraer los Centroides del modelo y revertir la escala a 'tiendas visibles' originales
centroides_scaled = kmeans.cluster_centers_
centroides_origin = scaler.inverse_transform(centroides_scaled)

plt.figure(figsize=(14, 6))
horas = range(0, 24)

# Graficar el comportamiento estandar de la curva para cada grupo descubierto
for i in range(k_optimo):
    plt.plot(horas, centroides_origin[i], marker='o', linewidth=2.5, label=f'Cluster {i} (Perfil Operacional {i})')

plt.title('Centroides Horarios 24D: Perfiles de Disponibilidad de Tiendas', fontsize=14)
plt.xlabel('Hora de Operación (0 - 23H)', fontsize=12)
plt.ylabel('Centroide Promedio de Tiendas Visibles', fontsize=12)
plt.xticks(horas)
plt.legend()
plt.grid(True)
plt.show()

# Analizar la densidad: ¿cuántos días pertenecen a cada tipo de cluster?
print("Días de historia agrupados por clúster:")
print(df_clustering['cluster'].value_counts())""")

add_markdown("""## 4.3 Visualización Espacial y Reducción de Dimensionalidad (PCA)
Para poder ver "clusters" en un plano XY normal, aplastaremos matemáticamente estas 24 horas a solo dos Componentes Principales.""")

add_code("""pca = PCA(n_components=2)
principals = pca.fit_transform(X_scaled)

df_pca = pd.DataFrame(data=principals, columns=['PC1', 'PC2'])
df_pca['cluster'] = df_clustering['cluster'].values # Importamos las etiquetas generadas por K-Means

plt.figure(figsize=(10, 6))
sns.scatterplot(x='PC1', y='PC2', hue='cluster', data=df_pca, palette='viridis', s=120, alpha=0.8)
plt.title(f'Gráfico Scatter 2D de Agrupación Temporal (K={k_optimo})')
plt.xlabel(f'Componente Principal 1 ({pca.explained_variance_ratio_[0]:.2%} de la varianza capturada)')
plt.ylabel(f'Componente Principal 2 ({pca.explained_variance_ratio_[1]:.2%} de la varianza capturada)')
plt.legend(title='Cluster de Comportamiento')
plt.show()""")

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook updated successfully with K-Means section.")
