# 🟠 Rappi Availability & AI Operational Insights

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una solución integral de **Business Intelligence e Inteligencia Artificial** diseñada para optimizar la toma de decisiones en la oferta de Rappi. El proyecto combina analítica avanzada, predicción de demanda y un agente conversacional experto.

---

##  Tabla de Contenidos
- [ Objetivo del Proyecto](#-objetivo-del-proyecto)
- [ Metodología CRISP-DM](#-metodología-crisp-dm)
- [ Arquitectura y Racional Tecnológico](#-arquitectura-y-racional-tecnológico)
- [ Estructura del Repositorio](#-estructura-del-repositorio)
- [ Guía de Instalación](#-guía-de-instalación)
- [ Ejecución](#-ejecución)
- [ Dockerización](#-dockerización)
- [ RappiBot (Inteligencia Operacional)](#-rappibot-inteligencia-operacional)

---

##  Objetivo del Proyecto
Maximizar la disponibilidad de tiendas y restaurantes mediante el análisis de datos históricos para predecir vacíos en la oferta. El sistema proporciona un dashboard interactivo para vizualizar clusters de comportamiento y un chatbot de IA para consultas operativas rápidas.

---

##  Metodología CRISP-DM
El ciclo de vida del dato en este proyecto sigue el estándar **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*), documentado en el Bloque 1:

1.  **Business Understanding:** Definición de KPIs de disponibilidad.
2.  **Data Understanding:** Exploración de snapshots de disponibilidad.
3.  **Data Preparation:** Limpieza y feature engineering (series temporales).
4.  **Modeling:** Implementación de **K-Means** (Clustering) y modelos autorregresivos (Forecasting).
5.  **Evaluation:** Validación de métricas de error (MAE/RMSE).
6.  **Deployment:** Integración de resultados en una API REST para consumo en tiempo real.

---

##  Arquitectura y Racional Tecnológico

###  Backend: FastAPI
*   **¿Por qué?** Elegimos FastAPI por su alto rendimiento (basado en Starlette y Pydantic) y su capacidad nativa de manejar asincronía, ideal para las llamadas externas a modelos de lenguaje (LLMs) sin bloquear el hilo principal.

###  Frontend: Next.js + Tailwind CSS
*   **¿Por qué?** Next.js 14 permite una renderización híbrida y una experiencia de usuario fluida (SPA). Tailwind CSS facilita la creación de una interfaz personalizada siguiendo los lineamientos estéticos de Rappi.

###  IA: Groq Cloud (Llama 3.3 70B)
*   **¿Por qué?** Groq ofrece una latencia ultra-baja en inferencia, permitiendo que RappiBot responda en milisegundos. Usamos Llama 3.3 por su razonamiento avanzado sobre datos tabulares cargados en RAM.

---

##  Estructura del Repositorio
```text
├── DATOS/                       # Base de datos (Crudos, Procesados, Resultados)
├── DOCUMENTACION/               # Guías técnicas y bitácoras de fase
├── PROYECTO/
│   ├── BLOQUE_1/                # Ciencia de Datos (CRISP-DM Notebooks)
│   ├── BLOQUE_2/                # Aplicación Web (Next.js)
│   └── BLOQUE_3/                # API Engine & IA (FastAPI)
├── Dockerfile                   # Configuración de contenedor (API)
├── docker-compose.yml           # Orquestación de servicios
├── requirements.txt             # Dependencias de Python consolidadas
└── README.md                    # Este documento
```

---

##  Guía de Instalación

### 1. Prerrequisitos
*   **Python 3.11+**
*   **Node.js 18+**
*   **Git**

### 2. Clonar y Configurar Python
```bash
git clone https://github.com/JairoVillegas/AVALIAVILITY-ANALISYS.git
cd AVALIAVILITY-ANALISYS
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar Frontend
```bash
cd PROYECTO/BLOQUE_2/frontend
npm install
```

### 4. Variables de Entorno
Crea un archivo `.env` en `PROYECTO/BLOQUE_3/backend/`:
```env
GROQ_API_KEY=tu_api_key_aqui
```

---

##  Ejecución

### Terminal 1: Backend
```bash
cd PROYECTO/BLOQUE_3/backend
python main.py
```

### Terminal 2: Frontend
```bash
cd PROYECTO/BLOQUE_2/frontend
npm run dev
```
Visita [localhost:3000](http://localhost:3000)

---

##  Dockerización
Si prefieres correr el proyecto usando contenedores:

```bash
docker-compose up --build
```
Esto levantará automáticamente la API (8000) y el Frontend (3000).

---

##  RappiBot (Inteligencia Operacional)
RappiBot integra el conocimiento de los modelos de ML con el lenguaje natural.
*   **Synonym Engine:** Entiende que "tiendas", "restaurantes" y "oferta" son conceptos unificados.
*   **Time-Aware:** Capaz de responder sobre el comportamiento de fechas específicas consultando directamente `AVAILABILITY-procesado.csv`.
*   **Context Caching:** Mantiene la base de conocimientos operacional en memoria para respuestas instantáneas.

---

