# Usa una imagen base para construir la app
FROM node:18 AS builder

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios para instalar dependencias
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto del proyecto y construye la app
COPY . .
RUN npm run build

# Usa una imagen ligera para servir la app construida
FROM nginx:alpine

# Copia los archivos estáticos generados por el build
COPY --from=builder /app/dist /usr/share/nginx/html

# Copia la configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expone el puerto
EXPOSE 80

# Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]