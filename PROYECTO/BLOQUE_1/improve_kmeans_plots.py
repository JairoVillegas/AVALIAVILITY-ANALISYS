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
        
        # Modify the centroids plot
        if "Centroides Horarios" in src and "kmeans.cluster_centers_" in src:
            cell['source'] = [
                "k_optimo = 2\n",
                "kmeans = KMeans(n_clusters=k_optimo, init='k-means++', random_state=42, n_init=10)\n",
                "clusters_pred = kmeans.fit_predict(X_scaled)\n",
                "df_clustering['cluster'] = clusters_pred\n",
                "\n",
                "centroides_scaled = kmeans.cluster_centers_\n",
                "centroides_origin = scaler.inverse_transform(centroides_scaled)\n",
                "\n",
                "plt.figure(figsize=(14, 7))\n",
                "horas_cols = [c for c in df_clustering.columns if str(c) != 'cluster']\n",
                "horas_num = [int(float(h)) for h in horas_cols]\n",
                "\n",
                "for i in range(k_optimo):\n",
                "    # Tratar de darle un nombre humano al clúster según su altura promedio\n",
                "    promedio = centroides_origin[i].mean()\n",
                "    etiqueta = 'Perfil de ALTA Disponibilidad' if promedio > centroides_origin.mean() else 'Perfil de BAJA Disponibilidad'\n",
                "    plt.plot(horas_num, centroides_origin[i], marker='o', linewidth=3.5, label=f'{etiqueta} (Cluster {i})')\n",
                "\n",
                "plt.title('¿Cómo es un día típico según el modelo matemático?', fontsize=16, fontweight='bold')\n",
                "plt.xlabel('Hora del Día', fontsize=12)\n",
                "plt.ylabel('Cantidad Media de Tiendas Abiertas', fontsize=12)\n",
                "plt.xticks(horas_num)\n",
                "plt.legend()\n",
                "plt.grid(True, alpha=0.4)\n",
                "\n",
                "plt.annotate('NOTA: Esta gráfica define las curvas \"molde\". Cada curva dibuja el comportamiento promedio\\nde todos los días que cayeron en ese grupo, resumiendo así el histórico.',\n",
                "            xy=(0.5, -0.15), xycoords='axes fraction', ha='center', fontsize=11, color='dimgray')\n",
                "plt.tight_layout()\n",
                "plt.show()\n"
            ]

        # Modify the Scatter plot
        if "pca = PCA(" in src and "sns.scatterplot" in src:
            cell['source'] = [
                "pca = PCA(n_components=2)\n",
                "principals = pca.fit_transform(X_scaled)\n",
                "\n",
                "df_pca = pd.DataFrame(data=principals, columns=['PC1', 'PC2'])\n",
                "df_pca['cluster'] = df_clustering['cluster'].values\n",
                "df_pca['date'] = df_clustering.index.values # Extraemos explícitamente las FECHAS para etiquetar puntos\n",
                "\n",
                "plt.figure(figsize=(12, 8))\n",
                "ax = sns.scatterplot(x='PC1', y='PC2', hue='cluster', data=df_pca, palette='Set2', s=250, alpha=0.9)\n",
                "\n",
                "# Imprimir la FECHA sobre cada punto exacto para contexto de negocio\n",
                "for i in range(df_pca.shape[0]):\n",
                "    ax.text(df_pca['PC1'][i]+0.2, df_pca['PC2'][i]-0.1, df_pca['date'][i], \n",
                "            horizontalalignment='left', size='medium', color='black', weight='semibold')\n",
                "\n",
                "plt.title('Mapa de Clustering Diario (Similitud del Comportamiento Operacional)', fontsize=16, fontweight='bold')\n",
                "plt.xlabel('Eje Matemático 1 (No Interpretable)', fontsize=11)\n",
                "plt.ylabel('Eje Matemático 2 (No Interpretable)', fontsize=11)\n",
                "plt.legend(title='Grupo de Rendimiento')\n",
                "\n",
                "plt.annotate('NOTA: CADA PUNTO ES UN DÍA HISTÓRICO EXISTENTE. \\nLos ejes 1 y 2 son abstracciones matemáticas (PCA); no tienen nombre comercial.\\nSi dos puntos están juntos, significa que esos dos días tuvieron un comportamiento IDÉNTICO.',\n",
                "            xy=(0.5, -0.15), xycoords='axes fraction', ha='center', fontsize=11, color='dimgray')\n",
                "plt.tight_layout()\n",
                "plt.show()\n"
            ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook K-means interpreted cells fixed successfully.")
