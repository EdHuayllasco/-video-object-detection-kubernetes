FROM node:18-slim

# Crea el directorio de la aplicación
WORKDIR /app

# Copia el package.json e instala las dependencias
COPY package*.json ./
RUN npm install

# Copia el resto de los archivos
COPY . .

# Exponer el puerto
EXPOSE 3000

# Comando para iniciar el servidor
CMD ["node", "server.js"]