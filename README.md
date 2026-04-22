#  Rappi Availability & AI Operational Insights :>

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una solución integral de **Business Intelligence e Inteligencia Artificial** diseñada para optimizar la toma de decisiones en la oferta de Rappi. El proyecto combina analítica avanzada, predicción de disponibilidad y un agente conversacional experto.

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
Maximizar la disponibilidad de tiendas y restaurantes mediante el análisis de datos históricos para predecir vacíos en la disponibilidad. El sistema proporciona un dashboard interactivo para vizualizar clusters de comportamiento y un chatbot de IA para consultas operativas rápidas.

---

##  Metodología CRISP-DM
El ciclo de vida del dato en este proyecto sigue el estándar **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*), documentado en el Bloque 1:

1.  **Business Understanding:** Definición de KPIs de disponibilidad y necesidades del negocio.
2.  **Data Understanding:** Exploración de snapshots de disponibilidad y detección de patrones iniciales.
3.  **Data Preparation:** Limpieza, manejo de nulos y feature engineering (extracción de horas, días y franjas).
4.  **Modeling:** Implementación de K-Means para clustering de perfiles diarios y Random Forest para forecasting.
5.  **Evaluation:** Validación de métricas de error (MAE) y relevancia de variables (Feature Importance).
6.  **Deployment:** Integración de los modelos en una API productiva y un dashboard interactivo.

---

##  Arquitectura y Racional Tecnológico

###  Backend: FastAPI
*   **Racional:** Elegimos FastAPI por su alto rendimiento y manejo nativo de asincronía. Es ideal para integrar el SDK de Groq, permitiendo que la IA responda sin bloquear otras peticiones del dashboard.

###  Frontend: Next.js + Tailwind CSS
*   **Racional:** Next.js 14 ofrece una estructura robusta para aplicaciones de datos. Tailwind CSS permite una interfaz limpia y profesional acorde a la identidad visual de Rappi.

###  IA: Groq Cloud (Llama 3.3 70B)
*   **Racional:** El uso de Groq garantiza una respuesta en tiempo real (milisegundos), este modelo fue usado en lugar de gemini por temas de limitaciones en la cantidad de tokens que se pueden usar en la version gratuita de gemini. El modelo Llama 3.3 es capaz de interpretar los resultados de los modelos de ML y el historial CSV cargado en memoria.

---

##  Estructura del Repositorio
```text
├── DATOS/                       # Base de datos (Crudos, Procesados, Resultados)
├── DOCUMENTACION/               # Guías técnicas y bitácoras de fase
├── PROYECTO/
│   ├── BLOQUE_1/                # Ciencia de Datos (CRISP-DM Notebooks)
│   ├── BLOQUE_2/                # Aplicación Web (Next.js)
│   └── BLOQUE_3/                # API Engine & IA (FastAPI)
├── Dockerfile                   # Configuración del contenedor (Backend)
├── .env.example                 # Plantilla de variables de entorno
├── docker-compose.yml           # Orquestación de contenedores
├── requirements.txt             # Dependencias de Python completas
└── README.md                    # Este documento
```

---

##  Guía de Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/JairoVillegas/AVALIAVILITY-ANALISYS.git
cd AVALIAVILITY-ANALISYS
```

### 2. Configurar Variables de Entorno
Copia la plantilla de ejemplo y añade tu API Key:
```bash
cp .env.example PROYECTO/BLOQUE_3/backend/.env
# Edita el archivo y pon tu GROQ_API_KEY
```

### 3. Instalación Local (Python)
```bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Instalación Local (Frontend)
```bash
cd PROYECTO/BLOQUE_2/frontend
npm install
```

---

##  Ejecución Manual

Requiere dos terminales activas:

**Terminal 1 (API):**
```bash
cd PROYECTO/BLOQUE_3/backend
python main.py
```

**Terminal 2 (Web):**
```bash
cd PROYECTO/BLOQUE_2/frontend
npm run dev
```

---

##  Dockerización
Para una ejecución rápida y aislada:

```bash
docker-compose up --build
```
Esto levantará el Backend en el puerto **8000** y el Frontend en el puerto **3000**.

---

##  RappiBot (Inteligencia Operacional)
RappiBot actúa como un analista experto en la disponibilidad de la plataforma:
*   **Sinónimos Operativos:** Entiende lenguaje natural y es capaz de responder preguntas asociadas al dashboard, como por ejemplo explicar terminos que nos conozcamos o buscar un dato en especifico en el dashboard y darnoslo.
*   **Memoria Histórica:** Consulta directamente `AVAILABILITY-procesado.csv` para dar datos exactos de fechas pasadas además de que está contextualizado con todos los resulados del bloque 1 y la metodología crisp dm para evitar alucinaciones.
*   **Visión Predictiva:** Conoce los clusters y pronósticos de las próximas 24 horas generados por los modelos de ML en el bloque 1 ademas de que puede reconocer cuales son las features más importantes al momento de la predicción.
