# Usamos una imagen de Node.js ligera
FROM node:20-alpine

# Directorio de trabajo
WORKDIR /app

# Copiamos archivos de configuración de npm
COPY PROYECTO/BLOQUE_2/frontend/package*.json ./

# Instalamos dependencias
RUN npm install

# Copiamos el resto del código del frontend
COPY PROYECTO/BLOQUE_2/frontend .

# Construimos la aplicación de Next.js
RUN npm run build

# Exponemos el puerto 3000
EXPOSE 3000

# Comando para ejecutar en modo producción
CMD ["npm", "start"]
