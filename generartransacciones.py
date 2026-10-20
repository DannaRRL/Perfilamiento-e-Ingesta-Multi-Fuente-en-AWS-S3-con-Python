
import boto3
import pandas as pd
import numpy as np
import json
import io
from datetime import datetime, timedelta
from botocore.exceptions import ClientError, BotoCoreError

# Configuración de AWS
BUCKET_NAME = "aws-academy-datacenter-bucket-23-02-024"
REGION = "us-west-2"
FILE_KEY = "raw/logs_m2m.json"

# Leer credenciales desde JSON
with open("credenciales.json", "r", encoding="utf-8") as archivo:
    credenciales = json.load(archivo)

# Crear cliente S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=credenciales["aws_access_key_id"],
    aws_secret_access_key=credenciales["aws_secret_access_key"],
    aws_session_token=credenciales["aws_session_token"],
    region_name=REGION
)

def generar_logs(num_registros=200):
    np.random.seed(42)
    logs = []

    for i in range(num_registros):
        fecha = datetime(2026, 1, 1) + timedelta(
            minutes=int(np.random.randint(0, 129600))
        )

        log = {
            "log_id": f"LOG-{1000 + i}",
            "dispositivo": f"DEVICE-{np.random.randint(100, 200)}",
            "timestamp": fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "tipo_evento": np.random.choice(
                ["Conexion", "Desconexion", "Transferencia", "Error"]
            ),
            "estado": np.random.choice(
                ["Exitoso", "Fallido", "Pendiente"]
            ),
            "datos": {
                "temperatura": round(float(np.random.uniform(20, 80)), 2),
                "latencia_ms": int(np.random.randint(1, 500))
            }
        }
        logs.append(log)

    return logs

def subir_logs_s3(logs):
    # Convertir JSON a bytes en memoria
    json_buffer = io.BytesIO()
    json_buffer.write(
        json.dumps(logs, ensure_ascii=False, indent=2).encode("utf-8")
    )
    json_buffer.seek(0)

    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=FILE_KEY,
            Body=json_buffer.getvalue(),
            ContentType="application/json"
        )
        print("¡logs_m2m.json subido correctamente a AWS S3!")

    except (ClientError, BotoCoreError) as e:
        print(f"Error al subir archivo: {e}")

if __name__ == "__main__":
    print("Generando 200 registros de logs M2M...")
    logs = generar_logs()
    subir_logs_s3(logs)
