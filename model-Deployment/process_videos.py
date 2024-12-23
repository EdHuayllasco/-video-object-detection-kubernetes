from ultralytics import YOLO
import os
import psycopg2
import boto3
import requests

# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "viratdata"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root1997+"),
    "host": os.getenv("DB_HOST", "postgres"),
    "port": os.getenv("DB_PORT", "5432"),
}

# Inicializar el cliente de S3
S3_BUCKET = "viratvideos"  # Reemplaza con el nombre de tu bucket
S3_REGION = "us-east-1"  # Reemplaza con tu región
s3 = boto3.client("s3", region_name=S3_REGION)

# Directorio temporal para guardar videos descargados
temp_video_path = "/tmp/videos"

if not os.path.exists(temp_video_path):
    os.makedirs(temp_video_path)

# Cargar el modelo YOLO
model = YOLO("/app/best.pt")

# Conectar a la base de datos
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
    exit()

# Verificar si el video ya ha sido procesado
def video_ya_procesado(video_name):
    try:
        cursor.execute("SELECT id FROM videos WHERE name = %s;", (video_name,))
        result = cursor.fetchone()
        return result is not None  # Si hay un resultado, el video ya fue procesado
    except Exception as e:
        print(f"Error al verificar si el video ya ha sido procesado: {e}")
        return True  # Evitar procesar en caso de error

# Procesar un solo video basado en una URL proporcionada
def procesar_video(video_url):
    # Obtener el nombre del archivo desde la URL
    video_name = os.path.basename(video_url)
    if not video_name.endswith(".mp4"):
        print("La URL no apunta a un archivo .mp4 válido.")
        return

    # Verificar si el video ya fue procesado
    if video_ya_procesado(video_name):
        print(f"El video '{video_name}' ya ha sido procesado. Saliendo.")
        return

    # Descargar el video
    local_file_path = os.path.join(temp_video_path, video_name)
    print(f"Descargando video: {video_url}")
    r = requests.get(video_url, stream=True)
    with open(local_file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Video descargado en: {local_file_path}")

    # Insertar el video en la base de datos
    try:
        cursor.execute("INSERT INTO videos (name) VALUES (%s) RETURNING id;", (video_name,))
        video_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Video registrado en la base de datos con ID: {video_id}")
    except Exception as e:
        print(f"Error al insertar el video en la base de datos: {e}")
        return

    # Carpeta de resultados con el nombre del video (sin extensión)
    output_path = os.path.join("/tmp", os.path.splitext(video_name)[0])
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Realizar predicción en el video
    print(f"Procesando el video: {local_file_path}")
    results = model.predict(
        source=local_file_path,
        stream=True,
        show=False,
        save=True,
        project=output_path,
        conf=0.45,
        line_width=2,
        save_crop=False,
        save_txt=True,
        show_labels=True,
        show_conf=True,
        classes=[0, 1, 2],
    )

    # Iterar sobre los resultados frame por frame
    frame_number = 0
    for r in results:
        frame_number += 1

        # Insertar el frame en la tabla "frames"
        cursor.execute(
            "INSERT INTO frames (video_id, frame_number) VALUES (%s, %s) RETURNING id;",
            (video_id, frame_number),
        )
        frame_id = cursor.fetchone()[0]
        conn.commit()

        # Accede a las detecciones del frame actual
        boxes = r.boxes  # Bounding boxes detectados

        # Iterar sobre cada detección y guardar en "frame_data"
        for box in boxes:
            x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
            confidence = box.conf[0].item()
            cls = int(box.cls[0].item())

            cursor.execute(
                """
                INSERT INTO frame_data (frame_id, class, x, y, width, height, confidence)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (frame_id, cls, x_min, y_min, x_max - x_min, y_max - y_min, confidence),
            )
        conn.commit()

    print(f"El video procesado y los resultados se han guardado en: {output_path}")
    cursor.execute("SELECT calculate_class_intervals();")
    conn.commit()
    print("Función calculate_class_intervals ejecutada exitosamente.")

    # Subir resultados a S3
    print(f"Subiendo resultados al bucket {S3_BUCKET}...")
    for root, dirs, files in os.walk(output_path):
        for file in files:
            result_file_path = os.path.join(root, file)
            s3_key = os.path.join(os.path.splitext(video_name)[0], os.path.basename(file))
            s3.upload_file(result_file_path, S3_BUCKET, s3_key)
            print(f"Subido: {s3_key}")

# Ejemplo de uso:
video_url = "https://viratvideos.s3.us-east-1.amazonaws.com/VIRAT_S_000202_01_001334_001520.mp4"
procesar_video(video_url)

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()
print("Conexión cerrada.")