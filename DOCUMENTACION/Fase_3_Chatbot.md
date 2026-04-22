# Fase 3: Agente Semántico y Chatbot Integrado

**Ubicación de Trabajo:** `BLOQUE_3`

##  Objetivo
Complementar la analítica predictiva y descriptiva del dashboard (Fase 2) mediante la construcción e implementación de un asistente semántico capaz de responder preguntas en lenguaje natural sobre la disponibilidad de tiendas.

##  Funcionamiento del Chatbot
1. **Entrada:** El cliente escribe una pregunta de negocio en lenguaje humano en el chat dentro de la web (ej: *"¿Cuáles fueron los motivos principales por los que las tiendas fallaron el martes pasado?"*).
2. **Procesamiento NLP:** El agente traduce esta petición a consultas usando LLMs e inyecciones de contexto basadas en el Dataset de la Fase 1.
3. **Consulta en BD:** El sistema va al dataset final y extrae la respuesta estructurada.
4. **Respuesta Semántica:** El agente re-interpreta la data técnica y la entrega en texto digerible para la interfaz de chat en la web.

##  Entregable Esperado
Un **sistema conversacional en la página web** conectado eficientemente a la arquitectura de datos, siendo capaz de atender y guiar a cualquier usuario corporativo al que se le dificulte interpretar las visualizaciones por su cuenta.
