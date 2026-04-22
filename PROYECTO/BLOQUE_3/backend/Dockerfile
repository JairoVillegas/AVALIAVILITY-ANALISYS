# Usamos una imagen ligera de Python
FROM python:3.11-slim

# Evitamos que Python genere archivos .pyc y habilitamos el logeo en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos los archivos necesarios manteniendo la estructura para que los paths funcionen
# Copiamos DATOS y la carpeta PROYECTO
COPY DATOS ./DATOS
COPY PROYECTO ./PROYECTO

# Exponemos el puerto 8000
EXPOSE 8000

# Ejecutamos el backend desde su ubicación original
CMD ["python", "PROYECTO/BLOQUE_3/backend/main.py"]
