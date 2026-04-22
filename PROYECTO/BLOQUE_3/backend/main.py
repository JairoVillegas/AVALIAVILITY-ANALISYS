from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os

# --- Cargar variables de entorno desde .env ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(title="Rappi Makers Dashboard API", description="API para servir insights de Machine Learning a la Web")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta a los datos procesados
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../DATOS/DATOS_FINAL_MODELOS"))

# =====================================================================
# CONTEXT CACHING LOCAL: construimos el contexto de datos UNA SOLA VEZ
# al arrancar el servidor, no en cada llamada al chat.
# =====================================================================
_DATA_CONTEXT_CACHE: str = ""
_HISTORICAL_DF: pd.DataFrame = None

def get_historical_context(user_query: str) -> str:
    """
    Busca fechas o momentos específicos en el historial completo (CSV procesado)
    para inyectarlos como contexto fresco si el usuario pregunta por el pasado.
    """
    global _HISTORICAL_DF
    if _HISTORICAL_DF is None:
        return ""
    
    query_lower = user_query.lower()
    # Heurística simple para detectar fechas en febrero 2026
    # Buscamos números del 1 al 11 (rango del CSV)
    found_day = None
    meses_feb = ["febrero", "feb", "/02/", "-02-"]
    
    if any(m in query_lower for m in meses_feb) or "pasado" in query_lower or "historial" in query_lower:
        # Buscamos del 11 al 1 (reversa) para evitar que "10" sea detectado como "1"
        for d in range(11, 0, -1):
            if f" {d}" in f" {query_lower}" or f"{d:02d}" in query_lower:
                found_day = f"2026-02-{d:02d}"
                break
    
    if found_day:
        print(f"🔎 Buscando datos históricos para: {found_day}...")
        # Filtramos el DF por ese día
        day_data = _HISTORICAL_DF[_HISTORICAL_DF['timestamp'].str.contains(found_day)]
        if not day_data.empty:
            # Si preguntan por una hora específica (ej. "a las 12")
            import re
            hour_match = re.search(r'(\d{1,2})\s*(?:am|pm|:00|hrs|horas|h)', query_lower)
            if not hour_match:
                hour_match = re.search(r'las\s+(\d{1,2})', query_lower)
            
            if hour_match:
                target_hour = f" {int(hour_match.group(1)):02d}:"
                hour_data = day_data[day_data['timestamp'].str.contains(target_hour)]
                if not hour_data.empty:
                    # Retornamos una muestra de esa hora
                    res = hour_data.head(5)
                    data_str = "\n".join([f"  - {row['timestamp']}: {int(row['visible_stores']):,} tiendas" for _, row in res.iterrows()])
                    return f"\nDATOS HISTÓRICOS ESPECÍFICOS PARA EL {found_day} (Cerca de la hora solicitada):\n{data_str}"
            
            # Si no hay hora o no se encontró la hora, damos un resumen del día
            pico = day_data.loc[day_data['visible_stores'].idxmax()]
            valle = day_data.loc[day_data['visible_stores'].idxmin()]
            avg = day_data['visible_stores'].mean()
            return (f"\nDATOS HISTÓRICOS PARA EL {found_day}:\n"
                    f"  - Promedio del día: {int(avg):,} tiendas disponibles.\n"
                    f"  - Punto máximo: {int(pico['visible_stores']):,} tiendas a las {pico['timestamp'][11:16]}.\n"
                    f"  - Punto mínimo: {int(valle['visible_stores']):,} tiendas a las {valle['timestamp'][11:16]}.")
    
    return ""

def build_data_context() -> str:
    """
    Lee todos los CSV clave y construye un resumen de negocio.
    Se llama una sola vez al inicio y se cachea en memoria.
    """
    context_parts = []
    nombre_map = {
        'hour': 'Hora del día', 'day_of_week': 'Día de la semana',
        'day': 'Día del mes', 'month': 'Mes', 'year': 'Año',
        'cluster': 'Rutina Diaria (Cluster)', 'time_band_Tarde': 'Franja Tarde',
        'time_band_Mañana': 'Franja Mañana', 'time_band_Noche': 'Franja Noche',
        'is_weekend': '¿Es fin de semana?', 'time_band_Madrugada': 'Franja Madrugada'
    }

    # 1. Perfiles de Clustering
    path = os.path.join(DATA_DIR, "DASHBOARD_KMEANS_Results.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        hour_cols = [c for c in df.columns if c not in ['cluster', 'date', 'Unnamed: 0']]
        resumen = []
        for c in df['cluster'].unique():
            filas = df[df['cluster'] == c]
            prom = filas[hour_cols].mean().mean()
            pico_hora = filas[hour_cols].mean().idxmax()
            valle_hora = filas[hour_cols].mean().idxmin()
            resumen.append(
                f"  - Cluster {c}: promedio {prom:,.0f} tiendas/hora. "
                f"Pico en hora {pico_hora}, valle en hora {valle_hora}."
            )
        context_parts.append("CLUSTERING K-MEANS (perfiles horarios):\n" + "\n".join(resumen))

    # 2. PCA con días de la semana
    path = os.path.join(DATA_DIR, "DASHBOARD_PCA_Clusters.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        df['date_parsed'] = pd.to_datetime(df['date'].astype(str).str.split(' ').str[0], errors='coerce')
        df['dia'] = df['date_parsed'].dt.day_name()
        dias_por_cluster = df.groupby('cluster')['dia'].apply(list).to_dict()
        resumen = [f"  - Cluster {c}: días [{', '.join(dias)}]" for c, dias in dias_por_cluster.items()]
        context_parts.append("MAPA PCA (días por cluster):\n" + "\n".join(resumen))

    # 3. Métricas del modelo Random Forest
    path = os.path.join(DATA_DIR, "DASHBOARD_FORECAST_MetricsSummary.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        metricas = df.set_index('Metrica')['Valor'].to_dict()
        resumen = "\n".join([f"  - {k}: {v:.4f}" for k, v in metricas.items()])
        context_parts.append(f"MÉTRICAS RANDOM FOREST:\n{resumen}")

    # 4. Pronóstico próximas 24 horas — tabla completa hora a hora
    path = os.path.join(DATA_DIR, "DASHBOARD_FORECAST_Future24H.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        filas = []
        for _, row in df.iterrows():
            hora = str(row['timestamp'])[11:16]   # extrae "HH:MM"
            tiendas = int(row['visible_stores_futuro'])
            filas.append(f"  {hora} → {tiendas:,} tiendas disponibles")
        context_parts.append("PRONÓSTICO 24H (hora a hora):\n" + "\n".join(filas))

    # 5. Feature Importance
    path = os.path.join(DATA_DIR, "DASHBOARD_FEATURE_IMPORTANCE.csv")
    if os.path.exists(path):
        df = pd.read_csv(path).sort_values('Importance', ascending=False)
        resumen = "\n".join([
            f"  {i+1}. {nombre_map.get(r['Unnamed: 0'], r['Unnamed: 0'])}: {r['Importance']:.5f}"
            for i, (_, r) in enumerate(df.head(6).iterrows())
        ])
        context_parts.append(f"IMPORTANCIA DE VARIABLES (top 6):\n{resumen}")

    return "\n\n".join(context_parts)


@app.on_event("startup")
async def startup_event():
    """Al arrancar el servidor se cachea el contexto de datos en memoria."""
    global _DATA_CONTEXT_CACHE, _HISTORICAL_DF
    _DATA_CONTEXT_CACHE = build_data_context()
    
    # Cargar historial completo para consultas específicas
    hist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../DATOS/DATOS_PROCESADOS/AVAILABILITY-procesado.csv"))
    if os.path.exists(hist_path):
        _HISTORICAL_DF = pd.read_csv(hist_path)
        print(f"✅ Historial completo cargado ({len(_HISTORICAL_DF)} filas).")
    
    print("✅ Contexto de datos cacheado en memoria al iniciar.")


# ======== HEALTH CHECK ========

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend de Inteligencia Operativa de Rappi en vivo."}

# ======== ENDPOINTS DE CLUSTERING ========

@app.get("/api/clustering/profiles")
def get_clustering_profiles():
    path = os.path.join(DATA_DIR, "DASHBOARD_KMEANS_Results.csv")
    if os.path.exists(path):
        return pd.read_csv(path).to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

@app.get("/api/clustering/pca")
def get_pca_scatter():
    path = os.path.join(DATA_DIR, "DASHBOARD_PCA_Clusters.csv")
    if os.path.exists(path):
        return pd.read_csv(path).to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

# ======== ENDPOINTS DE FORECASTING ========

@app.get("/api/forecast/test")
def get_forecast_test():
    path = os.path.join(DATA_DIR, "DASHBOARD_FORECAST_TestMetrics.csv")
    if os.path.exists(path):
        return pd.read_csv(path).to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

@app.get("/api/forecast/future")
def get_forecast_future():
    path = os.path.join(DATA_DIR, "DASHBOARD_FORECAST_Future24H.csv")
    if os.path.exists(path):
        return pd.read_csv(path).to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

@app.get("/api/forecast/metrics")
def get_forecast_metrics():
    path = os.path.join(DATA_DIR, "DASHBOARD_FORECAST_MetricsSummary.csv")
    if os.path.exists(path):
        return pd.read_csv(path).to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

# ======== ENDPOINTS DE EXPLICABILIDAD ========

@app.get("/api/features/importance")
def get_feature_importance():
    path = os.path.join(DATA_DIR, "DASHBOARD_FEATURE_IMPORTANCE.csv")
    if os.path.exists(path):
        return pd.read_csv(path).to_dict(orient="records")
    return {"error": "Archivo no encontrado"}

# ======== AGENTE IA: GEMINI 2.5 FLASH ========

SYSTEM_PROMPT = """Eres RappiBot, un analista de datos experto del equipo de Operaciones e Inteligencia de Negocio de Rappi.
Tu rol es ayudar a ejecutivos y equipos de operaciones a comprender los datos de disponibilidad de tiendas.

REGLAS:
- Responde SIEMPRE en español
- Usa lenguaje claro y ejecutivo, sin jerga técnica innecesaria
- Basa tus respuestas ÚNICAMENTE en los datos proporcionados
- IMPORTANTE: En este dataset, los términos "Tiendas", "Restaurantes" y "Establecimientos" son SINÓNIMOS. Si te preguntan por oferta de restaurantes, usa los datos de tiendas.
- Si no tienes información suficiente, dilo honestamente
- Sé conciso: máximo 4-5 párrafos. Usa **negrita** para cifras clave

DATOS DEL SISTEMA (contexto pre-cacheado al inicio del servidor):

{data_context}
"""

class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
async def chat_with_agent(request: ChatRequest):
    """Endpoint del Agente IA. Usa el contexto cacheado en memoria y Groq (Llama 3.3 70B)."""
    try:
        from groq import Groq

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"response": "Error: GROQ_API_KEY no encontrada en el archivo .env", "status": "error"}

        client = Groq(api_key=api_key)

        # El contexto ya está cacheado en memoria desde el startup
        base_context = _DATA_CONTEXT_CACHE
        
        # Búsqueda dinámica en el historial si el usuario pregunta por el pasado
        historical_context = get_historical_context(request.message)
        
        system_content = SYSTEM_PROMPT.format(data_context=base_context + historical_context)

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user",   "content": request.message},
            ],
            temperature=0.4,
            max_tokens=1024,
        )
        answer = completion.choices[0].message.content
        return {"response": answer, "status": "ok"}

    except Exception as e:
        return {"response": f"Error al procesar tu pregunta: {str(e)}", "status": "error"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
