import json
import os

file_path = r"C:/Users/jairo/OneDrive - Pontificia Universidad Javeriana/Desktop/RAPPI_MAKERS/PROYECTO/BLOQUE_1/NOTEBOOKS/CRISP-DM.ipynb"

if not os.path.exists(file_path):
    print("Error: file not found.")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source_str = "".join(cell.get('source', []))
        # Buscar la celda especifica de evaluacion de métricas
        if "mae = mean_absolute_error(y_test, predicciones)" in source_str and "RATING DEL MODELO" in source_str:
            cell['source'] = [
                "# Calcular predicción en Train para contrastar y medir el Overfitting\n",
                "pred_train = rf_model.predict(X_train)\n",
                "\n",
                "mae_train = mean_absolute_error(y_train, pred_train)\n",
                "rmse_train = np.sqrt(mean_squared_error(y_train, pred_train))\n",
                "\n",
                "# Mantener los cálculos de Test\n",
                "mae_test = mean_absolute_error(y_test, predicciones)\n",
                "rmse_test = np.sqrt(mean_squared_error(y_test, predicciones))\n",
                "r2_test = r2_score(y_test, predicciones)\n",
                "\n",
                "print(f\"========== RATING DEL MODELO (ANÁLISIS DE OVERFITTING) ==========\")\n",
                "print(f\"--- TRAIN METRICS ---\")\n",
                "print(f\"MAE: {mae_train:.1f} tiendas\")\n",
                "print(f\"RMSE: {rmse_train:.1f} tiendas\")\n",
                "print(f\"\\n--- TEST METRICS ---\")\n",
                "print(f\"MAE: {mae_test:.1f} tiendas (Margen de error promedio real esperado hacia el futuro)\")\n",
                "print(f\"RMSE: {rmse_test:.1f} tiendas\")\n",
                "print(f\"R2-Score: {r2_test:.2%} (Explica estupendamente la varianza estacionaria)\")\n",
                "\n",
                "# Guardar métricas como una tabla estándar para que el Dashboard Web las pueda renderizar\n",
                "metricas_df = pd.DataFrame({\n",
                "    'Metrica': ['MAE_TRAIN', 'RMSE_TRAIN', 'MAE_TEST', 'RMSE_TEST', 'R2_TEST'],\n",
                "    'Valor': [mae_train, rmse_train, mae_test, rmse_test, r2_test]\n",
                "})\n",
                "metricas_df.to_csv(os.path.join(final_output_path, 'DASHBOARD_FORECAST_MetricsSummary.csv'), index=False)\n",
                "print(\"\\n✅ Métricas de rendimiento exportadas a DASHBOARD_FORECAST_MetricsSummary.csv en DATOS_FINAL_MODELOS\")\n"
            ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook updated with Train/Test metrics and CSV export.")
