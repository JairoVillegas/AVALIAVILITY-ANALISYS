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
        source_str = "".join(cell.get('source', []))
        
        # 1. Update the 5.3 Forecasting section to include VERDADERO FUTURO prediction loop
        if "plt.plot(test.index, test['predictions']" in source_str:
            cell['source'] = [
                "# Generar predicciones Puras hacia el FUTURO INVISIBLE (Próximas 24 horas)\n",
                "last_timestamp = df_model.index[-1]\n",
                "future_times = [last_timestamp + pd.Timedelta(hours=i) for i in range(1, 25)]\n",
                "future_pred = []\n",
                "\n",
                "# Recolectamos todo el registro estadístico en memoria para alimentar los Rezagos Lags\n",
                "history_vals = list(df_model['visible_stores'].values)\n",
                "\n",
                "import warnings; warnings.filterwarnings('ignore') # Evitamos la alerta inofensiva de Numpy al inferir sin DataFrame Head\n",
                "\n",
                "for i in range(24):\n",
                "    lag_1 = history_vals[-1]\n",
                "    lag_2 = history_vals[-2]\n",
                "    lag_24 = history_vals[-24]\n",
                "    \n",
                "    pred = rf_model.predict([[lag_1, lag_2, lag_24]])[0]\n",
                "    pred = int(round(pred, 0))\n",
                "    future_pred.append(pred)\n",
                "    \n",
                "    # AUTORREGRESIÓN: Agregamos nuestra propia predicción como si fuera un evento \"pasado\" para generar la hora siguiente.\n",
                "    history_vals.append(pred)\n",
                "\n",
                "df_future = pd.DataFrame({'visible_stores_futuro': future_pred}, index=future_times)\n",
                "\n",
                "plt.figure(figsize=(14, 6))\n",
                "# Ploteamos historia (Train)\n",
                "plt.plot(train.index[-80:], train['visible_stores'][-80:], label='Contexto Histórico (Entrenamiento)', color='lightgrey')\n",
                "# Ploteamos Set de Prueba Test (Para evaluar el Error MAE/RMSE y que no haya Overfitting)\n",
                "plt.plot(test.index, test['visible_stores'], label='Realidad Cruda (Set Test)', color='gray', marker='o')\n",
                "plt.plot(test.index, test['predictions'], label='Predicción Test (Modelo Evaluándose)', color='navy', linestyle='--', linewidth=2.5)\n",
                "\n",
                "# Ploteamos la Proyección Final Pura 24h!\n",
                "plt.plot(df_future.index, df_future['visible_stores_futuro'], label='[NUEVO FUTURO] Forecast 24 Horas Siguientes', color='crimson', linestyle='-', linewidth=3.5, marker='D')\n",
                "\n",
                "plt.title('Forecasting: Testeo Analítico vs Proyección Futurista (Siguientes 24H)', fontsize=15, fontweight='bold')\n",
                "plt.xlabel('Tiempos de Medición')\n",
                "plt.ylabel('Total Tiendas Disponibles')\n",
                "plt.legend()\n",
                "plt.grid(True, alpha=0.3)\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "# Grabamos el Modelo Testeado en CSV separados. El Dashboard de la fase 2 los usará abundantemente!\n",
                "df_export_test = test.reset_index()[['timestamp', 'visible_stores', 'predictions']]\n",
                "df_export_test.to_csv(os.path.join(final_output_path, 'DASHBOARD_FORECAST_TestMetrics.csv'), index=False)\n",
                "\n",
                "df_export_future = df_future.reset_index()\n",
                "df_export_future.rename(columns={'index': 'timestamp'}, inplace=True)\n",
                "df_export_future.to_csv(os.path.join(final_output_path, 'DASHBOARD_FORECAST_Future24H.csv'), index=False)\n",
                "print(\"✅ Predicciones absolutas de futuro exportadas exitosamente a DATOS_FINAL_MODELOS\")\n"
            ]

        # 2. Update Feature Importance plotting block
        if "sns.barplot(x=feat_importances.values, y=feat_importances.index" in source_str:
            cell['source'] = [
                "# Lo pasamos a Serie de Pandas para fácil plotting\n",
                "feat_importances = pd.Series(importances, index=feature_names)\n",
                "feat_importances = feat_importances.sort_values(ascending=False)\n",
                "\n",
                "plt.figure(figsize=(13, 6))\n",
                "ax = sns.barplot(x=feat_importances.values, y=feat_importances.index, palette='viridis')\n",
                "\n",
                "# Para solucionar el problema de compresión de escalas (donde la Hora comprime todo), usamos ESCALA LOGARÍTMICA\n",
                "ax.set_xscale('log')\n",
                "from matplotlib.ticker import ScalarFormatter\n",
                "ax.xaxis.set_major_formatter(ScalarFormatter())\n",
                "\n",
                "# Añadimos Textos Numericos para poder ver los datos concretos ya que la escala es log\n",
                "for p in ax.patches:\n",
                "    ax.annotate(f'{p.get_width():.4f}', (p.get_width() * 1.1, p.get_y() + p.get_height() / 2.),\n",
                "                ha='left', va='center', size=11, color='black', weight='semibold')\n",
                "\n",
                "plt.title('Desglose de Peso Analítico por Atributo (ESCALA LOGARÍTMICA)', fontsize=15, fontweight='bold')\n",
                "plt.xlabel('Relevancia Científica (Logaritmo, cuanto más grande es la cifra más define tu disponibilidad)', fontsize=12)\n",
                "plt.ylabel('Variables del Comportamiento', fontsize=12)\n",
                "plt.xlim(right=ax.get_xlim()[1]*4) # Ampliar visualmente el límite X para que entre el texto\n",
                "plt.grid(axis='x', linestyle='--', alpha=0.4)\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "# Exportamos las variables más valiosas para consumo del LLM en la fase 3 o el Dashboard\n",
                "final_output_path = r'../../../DATOS/DATOS_FINAL_MODELOS/'\n",
                "os.makedirs(final_output_path, exist_ok=True)\n",
                "feat_importances.to_frame('Importance').to_csv(os.path.join(final_output_path, 'DASHBOARD_FEATURE_IMPORTANCE.csv'))\n",
                "print(f\"✅ Rank de Importancia exportado exitosamente a la bóveda estratégica.\")\n"
            ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook future forecasting loop and log-scale plots applied.")
