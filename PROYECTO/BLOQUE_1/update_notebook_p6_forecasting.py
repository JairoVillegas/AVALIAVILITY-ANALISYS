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

add_markdown("""## 4.4 Guardar Outputs Analíticos (K-Means)
Tal como lo requiere la arquitectura del proyecto, crearemos una ruta sagrada para el BLOQUE 2 y BLOQUE 3. Todos los hallazgos valiosos del Machine Learning se exportarán a la carpeta **`DATOS_FINAL_MODELOS`**. De ahí los leerá el Dashboard Web de nuestro cliente.""")

add_code("""final_output_path = r'../../../DATOS/DATOS_FINAL_MODELOS/'
os.makedirs(final_output_path, exist_ok=True)

# Guardar Resultados PCA (Puntos 2D y sus fechas) para el Scatterplot del Web Dashboard
df_pca.to_csv(os.path.join(final_output_path, 'DASHBOARD_PCA_Clusters.csv'), index=False)

# Guardar Resultados de las curvas horarias Centroides
df_clustering.to_csv(os.path.join(final_output_path, 'DASHBOARD_KMEANS_Results.csv'))

print(f"¡Modelos de Clustering empaquetados y guardados en -> {final_output_path}")""")

add_markdown("""# 5. Modeling y Evaluación (Forecasting Supervisado)
A continuación implementaremos la segunda estrategia y la última fase de CRISP-DM. Tomaremos el dataset `AVAILABILITY-hourly.csv` para entrenar a un modelo capaz de predecir cuántas tiendas estarán disponibles temporalmente hacia el futuro.
Utilizaremos `Random Forest Regressor` inyectándole conocimiento como los Lags (Rezagos) de tiempo pasados, un truco súper eficaz de Data Science.""")

add_code("""from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Leemos de nuevo la serie
df_hourly = pd.read_csv('../../../DATOS/DATOS_PROCESADOS/AVAILABILITY-hourly.csv')
df_hourly['timestamp'] = pd.to_datetime(df_hourly['timestamp'])
df_hourly.sort_values('timestamp', inplace=True)
df_hourly.set_index('timestamp', inplace=True)

# FEATURE ENGINEERING PARA SERIES TEMPORALES
# Le pasamos al modelo el estado de hace 1 hora, 2 horas y 24 horas (estacionalidad diaria directa)
df_hourly['lag_1'] = df_hourly['visible_stores'].shift(1)
df_hourly['lag_2'] = df_hourly['visible_stores'].shift(2)
df_hourly['lag_24'] = df_hourly['visible_stores'].shift(24)

# Como el modelo no puede entrenar con celdas "vacías" de las primeras 24 hrs que no tienen "pasado", las podamos
df_model = df_hourly.dropna().copy()
print("Matriz temporal enriquecida con variables desfasadas.")""")

add_markdown("""## 5.1 Entrenamiento y Predicción con Partición de Tiempo
Aislaremos las últimas 25 horas del dataset como zona incógnita (Test) simulando que queremos "predecir" lo que pasará al día siguiente. El modelo se entrenará solo con la primera parte de la historia.""")

add_code("""test_size = 25 

train = df_model.iloc[:-test_size].copy()
test = df_model.iloc[-test_size:].copy()

X_train = train[['lag_1', 'lag_2', 'lag_24']]
y_train = train['visible_stores']

X_test = test[['lag_1', 'lag_2', 'lag_24']]
y_test = test['visible_stores']

# Ensamblamos los Árboles
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Aplicamos la predicción al futuro oscuro
predicciones = rf_model.predict(X_test)
test['predictions'] = predicciones.round(0).astype('Int64')

print("✅ Modelo RF Autorregresivo Evaluado y Predicciones Creadas.")""")

add_markdown("""## 5.2 Evaluación Matemáticas Estándar de Regresión""")

add_code("""mae = mean_absolute_error(y_test, predicciones)
rmse = np.sqrt(mean_squared_error(y_test, predicciones))
r2 = r2_score(y_test, predicciones)

print(f"========== RATING DEL MODELO ==========")
print(f"MAE (Error Absoluto Medio): {mae:.1f} tiendas (Es decir, la predicción en promedio se desfasó por {int(mae)} restaurantes en ese periodo)")
print(f"RMSE (Error Cuadrático): {rmse:.1f} tiendas")
print(f"R2-Score: {r2:.2%} (Mide la varianza del comportamiento)")""")

add_markdown("""## 5.3 Contraste Visual de Regresión y Exportación
Guardamos los resultados del Forecast para que la web y el chatbot lo expongan en tablas o interroguen libremente sus aciertos.""")

add_code("""plt.figure(figsize=(14, 6))

# Dibujar historia (Train)
plt.plot(train.index[-50:], train['visible_stores'][-50:], label='Histórico de Referencia', color='lightgrey')
# Dibujar el Futuro (Test) vs lo Predicho
plt.plot(test.index, test['visible_stores'], label='Realidad Oculta', color='navy', marker='o')
plt.plot(test.index, test['predictions'], label='Predicción (Forecast)', color='crimson', linestyle='--', linewidth=3, marker='x')

plt.title('Performance Predictivo: Random Forest c/ Lags sobre las Últimas 25 horas', fontsize=16, fontweight='bold')
plt.xlabel('Corte Temporal Hora a Hora')
plt.ylabel('Volumen de Tiendas Visibles')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Exportamos las predicciones
test.reset_index().to_csv(os.path.join(final_output_path, 'DASHBOARD_FORECAST_Predictions.csv'), index=False)
print("Archivo Predictivo exportado hacia DATOS_FINAL_MODELOS")""")

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook updated successfully with final outputs and forecasting.")
