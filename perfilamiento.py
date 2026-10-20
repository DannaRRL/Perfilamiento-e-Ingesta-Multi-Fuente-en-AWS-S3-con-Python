
import boto3
import pandas as pd
import json
import io
from botocore.exceptions import ClientError, BotoCoreError

BUCKET = "aws-academy-datacenter-bucket-23-02-024"
REGION = "us-west-2"

# Leer credenciales
with open("credenciales.json", "r", encoding="utf-8") as archivo:
    credenciales = json.load(archivo)

# Conectar a S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=credenciales["aws_access_key_id"],
    aws_secret_access_key=credenciales["aws_secret_access_key"],
    aws_session_token=credenciales["aws_session_token"],
    region_name=REGION
)

def perfilamiento(nombre, ruta, formato):
    print(f"\n{'=' * 55}")
    print(f"PERFILAMIENTO: {nombre}")
    print("=" * 55)

    try:
        # Descargar archivo directamente a memoria
        respuesta = s3.get_object(Bucket=BUCKET, Key=ruta)
        contenido = io.BytesIO(respuesta["Body"].read())

        # Leer CSV o JSON
        if formato == "csv":
            df = pd.read_csv(contenido)
        else:
            datos = json.load(contenido)
            df = pd.json_normalize(datos)

        # Convertir fechas
        for columna in ["fecha", "timestamp"]:
            if columna in df.columns:
                df[columna] = pd.to_datetime(
                    df[columna], errors="coerce"
                )

        print("\nDIMENSIONES (filas, columnas):")
        print(df.shape)

        print("\nTIPOS DE DATOS:")
        print(df.dtypes)

        print("\nVALORES NULOS:")
        print(df.isnull().sum())

        print("\nESTADISTICAS DESCRIPTIVAS:")
        print(df.describe(include="all").to_string())

        print("\nPRIMEROS 5 REGISTROS:")
        print(df.head().to_string(index=False))

        print("\nPerfilamiento completado correctamente.")

    except (ClientError, BotoCoreError) as error:
        print(f"Error de AWS S3: {error}")
    except (ValueError, KeyError, TypeError) as error:
        print(f"Error al procesar datos: {error}")

# Perfilamiento del CSV
perfilamiento(
    "TRANSACCIONES CSV",
    "raw/transacciones.csv",
    "csv"
)

# Perfilamiento del JSON
perfilamiento(
    "LOGS M2M JSON",
    "raw/logs_m2m.json",
    "json"
)
