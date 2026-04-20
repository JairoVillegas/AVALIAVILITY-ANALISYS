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
        
        # 1. Buscar la celda donde instanciamos el Random Forest y añadirle hiperparámetros para Regularizar (Podar) el overfitting
        if "rf_model = RandomForestRegressor" in source_str:
            new_source = []
            for line in cell['source']:
                if "rf_model = RandomForestRegressor(" in line:
                    # En lugar de usar árboles de profundidad infinita (que memorizan todo el train y se overfitean),
                    # Limitamos la profundidad máxima a 6 ramas, y forzamos un mínimo de 3 muestras por hoja.
                    new_source.append("rf_model = RandomForestRegressor(n_estimators=150, max_depth=6, min_samples_leaf=4, random_state=42)\n")
                else:
                    new_source.append(line)
            cell['source'] = new_source

        # 2. Reemplazar la celda de Evaluación para añadir MAPE y mostrar Test vs Train balanceado
        if "mae_train = mean_absolute_error(y_train, pred_train)" in source_str or ("RATING DEL MODELO" in source_str and "np.sqrt(mean_squared_error" in source_str):
            cell['source'] = [
                "from sklearn.metrics import mean_absolute_percentage_error\n",
                "\n",
                "# Calcular predicciones y Métricas en Entorno de Train (Conocido)\n",
                "pred_train = rf_model.predict(X_train)\n",
                "mae_train = mean_absolute_error(y_train, pred_train)\n",
                "rmse_train = np.sqrt(mean_squared_error(y_train, pred_train))\n",
                "mape_train = mean_absolute_percentage_error(y_train, pred_train)\n",
                "\n",
                "# Calcular predicciones y Métricas en Entorno de Test (Inédito)\n",
                "mae_test = mean_absolute_error(y_test, predicciones)\n",
                "rmse_test = np.sqrt(mean_squared_error(y_test, predicciones))\n",
                "r2_test = r2_score(y_test, predicciones)\n",
                "mape_test = mean_absolute_percentage_error(y_test, predicciones)\n",
                "\n",
                "print(f\"========== RATING DEL MODELO (CONTROL DE OVERFITTING) ==========\")\n",
                "print(f\"--- TRAIN METRICS ---\")\n",
                "print(f\"MAE: {mae_train:.1f} tiendas\")\n",
                "print(f\"RMSE: {rmse_train:.1f} tiendas\")\n",
                "print(f\"MAPE (Error Porcentual): {mape_train:.2%}\")\n",
                "print(f\"\\n--- TEST METRICS ---\")\n",
                "print(f\"MAE: {mae_test:.1f} tiendas\")\n",
                "print(f\"RMSE: {rmse_test:.1f} tiendas\")\n",
                "print(f\"MAPE (Error Porcentual): {mape_test:.2%} (Margen absoluto por cada 100 tiendas!)\")\n",
                "print(f\"R2-Score: {r2_test:.2%}\")\n",
                "\n",
                "# Guardar métricas incluyendo MAPE para la Web\n",
                "metricas_df = pd.DataFrame({\n",
                "    'Metrica': ['MAE_TRAIN', 'RMSE_TRAIN', 'MAPE_TRAIN', 'MAE_TEST', 'RMSE_TEST', 'MAPE_TEST', 'R2_TEST'],\n",
                "    'Valor': [mae_train, rmse_train, mape_train, mae_test, rmse_test, mape_test, r2_test]\n",
                "})\n",
                "os.makedirs(final_output_path, exist_ok=True)\n",
                "metricas_df.to_csv(os.path.join(final_output_path, 'DASHBOARD_FORECAST_MetricsSummary.csv'), index=False)\n",
                "print(\"\\n✅ Evaluación MAPE incorporada. Métricas exportadas a la bóveda estratégica.\")\n"
            ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook logic strictly regularized against Overfitting.")
