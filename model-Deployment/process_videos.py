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

# Configuración del bucket S3
S3_BUCKET = "viratvideos"  # Reemplaza con el nombre de tu bucket
S3_REGION = "us-east-1"  # Reemplaza con tu región

# Inicializar el cliente de S3
s3 = boto3.client("s3", region_name=S3_REGION)

# Directorio temporal para guardar videos descargados
temp_video_path = "/tmp/videos"
output_path = "/tmp/results"  # Resultados locales antes de subir a S3

if not os.path.exists(temp_video_path):
    os.makedirs(temp_video_path)

if not os.path.exists(output_path):
    os.makedirs(output_path)

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

# Listar los videos desde el bucket S3
response = s3.list_objects_v2(Bucket=S3_BUCKET)
if "Contents" not in response:
    print("No se encontraron videos en el bucket.")
    exit()

# Procesar cada video en el bucket
for obj in response["Contents"]:
    file_key = obj["Key"]
    if not file_key.endswith(".mp4"):
        continue

    # Descargar el video desde la URL pública
    file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_key}"
    local_file_path = os.path.join(temp_video_path, os.path.basename(file_key))
    print(f"Descargando video: {file_url}")
    r = requests.get(file_url, stream=True)
    with open(local_file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Procesando el video: {local_file_path}")

    # Insertar el video en la base de datos
    cursor.execute("INSERT INTO videos (name) VALUES (%s) RETURNING id;", (os.path.basename(file_key),))
    video_id = cursor.fetchone()[0]
    conn.commit()
    print(f"Video registrado en la base de datos con ID: {video_id}")

    # Realizar predicción en el video
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
            s3_key = os.path.join("results", os.path.basename(file))
            s3.upload_file(result_file_path, S3_BUCKET, s3_key)
            print(f"Subido: {s3_key}")

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()
print("Conexión cerrada.")