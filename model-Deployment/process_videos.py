from ultralytics import YOLO
import os

# Ruta del volumen compartido donde estarán los videos
input_path = "/app/videos"  # Carpeta donde estarán los videos montados desde el volumen
output_path = "/app/videos/results"  # Carpeta donde se guardarán los resultados

# Crear directorio de resultados si no existe
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Cargar el modelo YOLO
model = YOLO("/app/best.pt")  # Asegúrate de que el modelo esté en la ruta /app/best.pt en el contenedor

# Obtener el primer archivo de video en la carpeta de entrada
video_files = [f for f in os.listdir(input_path) if f.endswith(".mp4")]

if len(video_files) == 0:
    print("No se encontraron videos en la carpeta de entrada.")
else:
    # Procesar solo el primer video
    first_video = video_files[0]
    video_path = os.path.join(input_path, first_video)
    print(f"Procesando el primer video: {video_path}")

    # Realizar predicción en el video
    results = model.predict(
        source=video_path,       # Ruta del video de entrada
        stream=True,             # Habilitar streaming para liberar memoria frame por frame
        show=False,              # No mostrar los resultados en tiempo real
        save=True,               # Guardar el video procesado con las detecciones
        project=output_path,    # Carpeta donde se guardará el resultado
        conf=0.45,                # Umbral de confianza
        line_width=2,            # Grosor de las líneas de los bounding boxes
        save_crop=False,         # No guardar recortes individuales de los objetos detectados
        save_txt=True,           # Guardar las predicciones en formato de texto
        show_labels=True,        # Mostrar etiquetas de las clases en las detecciones
        show_conf=True,          # Mostrar el nivel de confianza en las etiquetas
        classes=[0, 1, 2]        # Detectar únicamente las clases con IDs 0, 1 y 2
    )
    # Iterar sobre los resultados frame por frame
    for r in results:
    # Accede a las detecciones del frame actual
        boxes = r.boxes  # Bounding boxes detectados
        masks = r.masks  # Máscaras (si aplica)
        probs = r.probs  # Probabilidades de las clases (si aplica)

    # Ejemplo: Imprimir coordenadas de los bounding boxes
        print(boxes.xyxy)  # Coordenadas [x_min, y_min, x_max, y_max]
        print(boxes.conf)  # Niveles de confianza
        print(boxes.cls)   # Clases detectadas

    print(f"El video procesado y los resultados se han guardado en: {output_path}")