import json
import os

file_path = r"C:\Users\jairo\OneDrive - Pontificia Universidad Javeriana\Desktop\RAPPI_MAKERS\PROYECTO\BLOQUE_1\NOTEBOOKS\CRISP-DM.ipynb"

if not os.path.exists(file_path):
    print("Error: file not found.")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        src = "".join(cell.get('source', []))
        if 'k_optimo = 3' in src and 'kmeans = KMeans' in src:
            cell['source'] = [
                "k_optimo = 2  # Actualizado a 2 tras observar el Método del Codo\n",
                "kmeans = KMeans(n_clusters=k_optimo, init='k-means++', random_state=42, n_init=10)\n",
                "df_clustering['cluster'] = kmeans.fit_predict(X_scaled)\n",
                "\n",
                "# Extraer los Centroides del modelo y revertir la escala a 'tiendas visibles' originales\n",
                "centroides_scaled = kmeans.cluster_centers_\n",
                "centroides_origin = scaler.inverse_transform(centroides_scaled)\n",
                "\n",
                "plt.figure(figsize=(14, 6))\n",
                "\n",
                "# Extraemos dinámicamente las horas presentes en los datos (las 19 dimensiones reales)\n",
                "horas_cols = [c for c in df_clustering.columns if str(c) != 'cluster']\n",
                "horas_num = [int(float(h)) for h in horas_cols]\n",
                "\n",
                "# Graficar el comportamiento estandar de la curva para cada grupo descubierto\n",
                "for i in range(k_optimo):\n",
                "    plt.plot(horas_num, centroides_origin[i], marker='o', linewidth=2.5, label=f'Cluster {i} (Perfil {i})')\n",
                "\n",
                "plt.title(f'Centroides Horarios ({len(horas_num)}D): Perfiles de Disponibilidad de Tiendas', fontsize=14)\n",
                "plt.xlabel('Hora de Operación Reales Registradas', fontsize=12)\n",
                "plt.ylabel('Centroide Promedio de Tiendas Visibles', fontsize=12)\n",
                "plt.xticks(horas_num)\n",
                "plt.legend()\n",
                "plt.grid(True)\n",
                "plt.show()\n",
                "\n",
                "# Analizar la densidad: ¿cuántos días pertenecen a cada tipo de cluster?\n",
                "print(\"Días de historia agrupados por clúster:\")\n",
                "print(df_clustering['cluster'].value_counts())\n"
            ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook code logic directly fixed successfully.")
