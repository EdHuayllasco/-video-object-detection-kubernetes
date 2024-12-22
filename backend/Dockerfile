# Usa una imagen base de Node.js
FROM node:18

# Instala herramientas como el cliente PostgreSQL
RUN apt update && apt install -y postgresql-client

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de configuración del backend
COPY package*.json ./

# Instala las dependencias y nodemon de forma global
RUN npm install && npm install -g nodemon

# Copia el resto del código
COPY . .

# Expone el puerto donde corre tu app
EXPOSE 3000

# Comando para iniciar el servidor con nodemon
CMD ["nodemon", "server.js"]