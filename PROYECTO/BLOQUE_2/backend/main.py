from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI(title="Rappi Makers Dashboard API", description="API para servir insights de Machine Learning a la Web")

# Permitir a la web de Next.js conectarse a nuestro backend local sin bloqueos de seguridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Encontramos la bóveda de datos que la Fase 1 creó
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../DATOS/DATOS_FINAL_MODELOS"))

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend de Inteligencia Operativa de Rappi en vivo."}

# ======== ENDPOINTS DE CLUSTERING (Perfilamiento) ========

@app.get("/api/clustering/profiles")
def get_clustering_profiles():
    """Devuelve las curvas horarias promedio para los clusters de K-Means."""
    path = os.path.join(DATA_DIR, "DASHBOARD_KMEANS_Results.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

@app.get("/api/clustering/pca")
def get_pca_scatter():
    """Devuelve las posiciones en el mapa 2D de cada día analizado."""
    path = os.path.join(DATA_DIR, "DASHBOARD_PCA_Clusters.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

# ======== ENDPOINTS DE FORECASTING (Series de Tiempo) ========

@app.get("/api/forecast/test")
def get_forecast_test():
    """Devuelve el contraste histórico entre lo que se predijo y lo que realmente pasó."""
    path = os.path.join(DATA_DIR, "DASHBOARD_FORECAST_TestMetrics.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

@app.get("/api/forecast/future")
def get_forecast_future():
    """Devuelve la predicción a futuro puro de las próximas 24 horas invisibles."""
    path = os.path.join(DATA_DIR, "DASHBOARD_FORECAST_Future24H.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

@app.get("/api/forecast/metrics")
def get_forecast_metrics():
    """Devuelve los puntajes de rendimiento matemático y porcentual del Algoritmo (MAE, RMSE, MAPE)."""
    path = os.path.join(DATA_DIR, "DASHBOARD_FORECAST_MetricsSummary.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

# ======== ENDPOINTS DE EXPLICABILIDAD ========

@app.get("/api/features/importance")
def get_feature_importance():
    """Devuelve el ranking de factores clave que dominan el comportamiento del sistema."""
    path = os.path.join(DATA_DIR, "DASHBOARD_FEATURE_IMPORTANCE.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

if __name__ == "__main__":
    import uvicorn
    # Inicia eñ servidor en el puerto 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
