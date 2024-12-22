import boto3

# Configuración del bucket S3
S3_BUCKET = "viratvideos"  # Reemplaza con el nombre de tu bucket
S3_REGION = "us-east-1"  # Reemplaza con la región de tu bucket (si es diferente)

# Inicializar el cliente de S3
s3 = boto3.client("s3", region_name=S3_REGION)

# Listar los objetos en el bucket
response = s3.list_objects_v2(Bucket=S3_BUCKET)
if "Contents" in response:
    print("URLs de los archivos en el bucket:")
    for obj in response["Contents"]:
        file_key = obj["Key"]
        # Generar la URL pública
        file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_key}"
        print(file_url)
else:
    print("No se encontraron archivos en el bucket.")