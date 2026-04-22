
#  Rappi Availability & AI Operational Insights c:

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una solución integral de **Business Intelligence e Inteligencia Artificial** diseñada para optimizar la toma de decisiones en la oferta de Rappi. El proyecto combina analítica avanzada, predicción de disponibilidad y un agente conversacional experto.

---

## Tabla de Contenidos

- [Objetivo del Proyecto](#-objetivo-del-proyecto)
- [Metodología CRISP-DM](#-metodología-crisp-dm)
- [Arquitectura y Racional Tecnológico](#-arquitectura-y-racional-tecnológico)
- [Estructura del Repositorio](#-estructura-del-repositorio)
- [Requisitos Previos](#-requisitos-previos)
- [Despliegue con Docker (Recomendado)](#-despliegue-con-docker-recomendado)
- [Ejecución Manual (Sin Docker)](#-ejecución-manual-sin-docker)
- [Verificación del Sistema](#-verificación-del-sistema)
- [Solución de Problemas Comunes](#-solución-de-problemas-comunes)
- [RappiBot (Inteligencia Operacional)](#-rappibot-inteligencia-operacional)

---

## Objetivo del Proyecto

Maximizar la disponibilidad de tiendas y restaurantes mediante el análisis de datos históricos para predecir vacíos en la disponibilidad. El sistema proporciona un dashboard interactivo para visualizar clusters de comportamiento y un chatbot de IA para consultas operativas rápidas.

---

## Metodología CRISP-DM

El ciclo de vida del dato en este proyecto sigue el estándar **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*), documentado en el Bloque 1:

1. **Business Understanding:** Definición de KPIs de disponibilidad y necesidades del negocio.
2. **Data Understanding:** Exploración de snapshots de disponibilidad y detección de patrones iniciales.
3. **Data Preparation:** Limpieza, manejo de nulos y feature engineering (extracción de horas, días y franjas).
4. **Modeling:** Implementación de K-Means para clustering de perfiles diarios y Random Forest para forecasting.
5. **Evaluation:** Validación de métricas de error (MAE) y relevancia de variables (Feature Importance).
6. **Deployment:** Integración de los modelos en una API productiva y un dashboard interactivo.

---

## Arquitectura y Racional Tecnológico

### Backend: FastAPI
Elegimos FastAPI por su alto rendimiento y manejo nativo de asincronía. Es ideal para integrar el SDK de Groq, permitiendo que la IA responda sin bloquear otras peticiones del dashboard.

### Frontend: Next.js + Tailwind CSS
Next.js 14 ofrece una estructura robusta para aplicaciones de datos. Tailwind CSS permite una interfaz limpia y profesional acorde a la identidad visual de Rappi.

### IA: Groq Cloud (Llama 3.3 70B)
El uso de Groq garantiza respuesta en tiempo real (milisegundos). Este modelo fue seleccionado en lugar de Gemini por las limitaciones de tokens en su versión gratuita. El modelo Llama 3.3 es capaz de interpretar los resultados de los modelos de ML y el historial CSV cargado en memoria.

---

## Estructura del Repositorio

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

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu máquina:

| Herramienta | Versión mínima | Verificar instalación |
|---|---|---|
| [Git](https://git-scm.com/) | cualquiera | `git --version` |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | 24+ | `docker --version` |
| [Docker Compose](https://docs.docker.com/compose/) | 2.0+ | `docker compose version` |

> **Nota:** Docker Desktop incluye Docker Compose en versiones recientes. Si usas Linux, puede que necesites instalarlo por separado.

---

## Despliegue con Docker (Recomendado)

Esta es la forma más sencilla y confiable de correr el proyecto en cualquier máquina. Sigue los pasos **en orden**.

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/JairoVillegas/AVALIAVILITY-ANALISYS.git
cd AVALIAVILITY-ANALISYS
```

### Paso 2 — Crear el archivo de variables de entorno

Este archivo contiene tu API Key y **no se incluye en el repositorio por seguridad**. Debes crearlo a partir de la plantilla.

**En Windows (CMD o PowerShell):**
```cmd
copy .env.example PROYECTO\BLOQUE_3\backend\.env
```

**En Mac / Linux:**
```bash
cp .env.example PROYECTO/BLOQUE_3/backend/.env
```

### Paso 3 — Agregar tu API Key de Groq

Abre el archivo que acabas de crear:
PROYECTO/BLOQUE_3/backend/.env

Verás algo como esto:

```env
GROQ_API_KEY=
```

Reemplázalo con tu clave real:

```env
GROQ_API_KEY=tu_api_key_aqui
```

> **¿Dónde obtengo la API Key?** Regístrate gratis en [console.groq.com](https://console.groq.com) y genera una clave desde el panel de API Keys.

### Paso 4 — Construir y levantar los contenedores

Desde la raíz del repositorio (la carpeta `AVALIAVILITY-ANALISYS`), ejecuta:

```bash
docker compose up --build
```

Este comando realizará automáticamente:
- Construcción de la imagen del Backend (FastAPI)
- Construcción de la imagen del Frontend (Next.js)
- Instalación de todas las dependencias dentro de los contenedores
- Inicio de ambos servicios en red

La primera vez puede tardar varios minutos. Espera hasta ver en la terminal mensajes similares a:
backend   | INFO:     Application startup complete.
frontend  | ✓ Ready on http://localhost:3000

### Paso 5 — Acceder a la aplicación

Una vez que ambos servicios estén activos, abre tu navegador:

| Servicio | URL |
|---|---|
| **Dashboard (Frontend)** | http://localhost:3000 |
| **API Docs (Backend)** | http://localhost:8000/docs |

### Detener el sistema

Para detener todos los contenedores, presiona `Ctrl + C` en la terminal donde corre Docker, o ejecuta en otra terminal:

```bash
docker compose down
```

### Reiniciar sin reconstruir

Si ya construiste las imágenes antes y no hubo cambios en el código, puedes levantar el sistema más rápido con:

```bash
docker compose up
```

### Reconstruir desde cero

Si modificaste dependencias (`requirements.txt`, `package.json`) o archivos de configuración de Docker, fuerza una reconstrucción limpia:

```bash
docker compose down
docker compose up --build
```

---

## Ejecución Manual (Sin Docker)

Si prefieres correr el proyecto sin Docker, necesitarás tener instalado **Python 3.11+** y **Node.js 18+**.

Requiere dos terminales activas:

### Terminal 1 — Backend (API)

```bash
# Crear y activar entorno virtual
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (si no lo hiciste antes)
cp .env.example PROYECTO/BLOQUE_3/backend/.env
# Edita el .env y agrega tu GROQ_API_KEY

# Iniciar la API
cd PROYECTO/BLOQUE_3/backend
python main.py
```

### Terminal 2 — Frontend (Web)

```bash
cd PROYECTO/BLOQUE_2/frontend
npm install
npm run dev
```

---

## Verificación del Sistema

Una vez levantado el proyecto (por Docker o manual), puedes comprobar que todo funciona:

**Verificar el Backend:**
```bash
curl http://localhost:8000/health
```
Respuesta esperada: `{"status": "ok"}`

**Verificar el Frontend:**  
Abre http://localhost:3000 en tu navegador. Deberías ver el dashboard de Rappi.

**Verificar la documentación de la API:**  
Abre http://localhost:8000/docs para explorar todos los endpoints disponibles con Swagger UI.

---

## Solución de Problemas Comunes

### El comando `docker compose` no se reconoce
En versiones antiguas de Docker, el comando era `docker-compose` (con guion). Prueba:
```bash
docker-compose up --build
```

### El puerto 3000 u 8000 ya está en uso
Otro proceso está ocupando ese puerto. Para liberar el puerto en Windows:
```cmd
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```
En Mac / Linux:
```bash
lsof -ti:3000 | xargs kill -9
```

### Error: `GROQ_API_KEY` no encontrada
Asegúrate de que el archivo `.env` existe en `PROYECTO/BLOQUE_3/backend/` y que contiene la clave correctamente escrita (sin espacios ni comillas extras alrededor del valor).

### Docker construye pero el frontend no carga
Espera unos segundos adicionales. Next.js puede tardar en compilar. Revisa los logs del contenedor:
```bash
docker compose logs frontend
```

### Cambios en el código no se reflejan
Si modificaste archivos y no se actualizan, reinicia el contenedor afectado:
```bash
docker compose restart backend
# o
docker compose restart frontend
```

### Limpiar todo y empezar desde cero
```bash
docker compose down --volumes --rmi all
docker compose up --build
```

---

## RappiBot (Inteligencia Operacional)

RappiBot actúa como un analista experto en la disponibilidad de la plataforma:

- **Sinónimos Operativos:** Entiende lenguaje natural y puede responder preguntas asociadas al dashboard, explicar términos desconocidos o buscar un dato específico.
- **Memoria Histórica:** Consulta directamente `AVAILABILITY-procesado.csv` para dar datos exactos de fechas pasadas. Está contextualizado con todos los resultados del Bloque 1 y la metodología CRISP-DM para evitar alucinaciones.
- **Visión Predictiva:** Conoce los clusters y pronósticos de las próximas 24 horas generados por los modelos de ML, y puede identificar cuáles son las features más importantes al momento de la predicción.