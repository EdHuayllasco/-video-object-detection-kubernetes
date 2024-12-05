FROM python:3.9-slim

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*

# Instalar las dependencias de Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar el modelo y el script
COPY best.pt /app/best.pt
COPY process_videos.py /app/process_videos.py

# Establecer el directorio de trabajo
WORKDIR /app

# Comando para ejecutar el script
CMD ["python", "process_videos.py"]