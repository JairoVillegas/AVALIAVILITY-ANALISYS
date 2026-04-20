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
        # Corregir el 'Int64' a int en todas las celdas que lo tengan
        if "astype('Int64')" in source_str:
            new_source = []
            for line in cell['source']:
                new_source.append(line.replace("astype('Int64')", "astype(int)"))
            cell['source'] = new_source

def add_markdown(text):
    nb['cells'].append({"cell_type": "markdown", "metadata": {}, "source": [line + "\n" if i < len(text.split("\n"))-1 else line for i, line in enumerate(text.split("\n"))]})

def add_code(text):
    nb['cells'].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + "\n" if i < len(text.split("\n"))-1 else line for i, line in enumerate(text.split("\n"))]})

add_markdown("""## 5.4 Feature Importance (Explicabilidad del Comportamiento Operacional)
Para cumplir con la meta analítica estructurada en la sección de Preparation, utilizaremos nuestro archivo `AVAILABILITY-features.csv`.
Entrenaremos un modelo global sobre TODOS nuestros factores ambientales (la hora, el día de la semana, fin de semana) para que el Machine Learning nos diga **MATEMÁTICAMENTE QUÉ VARIABLE PESA MÁS** a la hora de determinar si habrán muchas o pocas tiendas abiertas. Esto brinda muchísimo valor al cliente.""")

add_code("""import seaborn as sns
import matplotlib.pyplot as plt

# Cargar Dataset Extendido estructurado para Tabular ML
df_factors = pd.read_csv('../../../DATOS/DATOS_PROCESADOS/AVAILABILITY-features.csv')

# Machine Learning necesita números, las categorías de texto como 'time_band' (Madrugada, Tarde, etc) se transforman a One-Hot Encoding
df_model_feat = pd.get_dummies(df_factors, columns=['time_band'], drop_first=False)

# Separar variables predictoras (X) y el objetivo que se quiere descifrar (Y)
# Quitamos columnas que son strings (fechas) y la variable a predecir
X_feat = df_model_feat.drop(columns=['timestamp', 'date', 'visible_stores'])
y_feat = df_model_feat['visible_stores']

# Entrenar un modelo de Árboles (es el algoritmo PERFECTO para calcular Importancia sin escalar variables)
rf_explainer = RandomForestRegressor(n_estimators=100, random_state=42)
rf_explainer.fit(X_feat, y_feat)

# Extraer y graficar el 'Feature Importance' matemático
importances = rf_explainer.feature_importances_
feature_names = X_feat.columns

# Lo pasamos a Serie de Pandas para fácil plotting
feat_importances = pd.Series(importances, index=feature_names)
feat_importances = feat_importances.sort_values(ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x=feat_importances.values, y=feat_importances.index, palette='magma')

plt.title('¿Qué factor dicta si habrá alta o baja disponibilidad? (Feature Importance)', fontsize=15, fontweight='bold')
plt.xlabel('Grado de Importancia Matemática en el Sistema (0 a 1)', fontsize=12)
plt.ylabel('Variables Temporales Evaluadas', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Exportamos las variables más valiosas para consumo del LLM en la fase 3 o el Dashboard
final_output_path = r'../../../DATOS/DATOS_FINAL_MODELOS/'
os.makedirs(final_output_path, exist_ok=True)
feat_importances.to_frame('Importance').to_csv(os.path.join(final_output_path, 'DASHBOARD_FEATURE_IMPORTANCE.csv'))
print(f"✅ Rank de Importancia exportado exitosamente a la bóveda estratégica.")""")

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Notebook code fixed and Feature Importance appended.")
