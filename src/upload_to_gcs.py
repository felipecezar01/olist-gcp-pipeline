import os
from pathlib import Path
from google.cloud import storage

# Configurações do projeto
BUCKET_NAME = "olist-gcp-pipeline-raw"
DATA_RAW_PATH = Path(__file__).parent.parent / "data" / "raw"


def upload_file(bucket, local_path: Path) -> None:
    """Faz upload de um arquivo local para o bucket no Cloud Storage."""
    blob_name = f"olist/{local_path.name}"
    blob = bucket.blob(blob_name)

    print(f"Enviando {local_path.name}...")
    blob.upload_from_filename(str(local_path))
    print(f"  OK -> gs://{BUCKET_NAME}/{blob_name}")


def upload_all_csvs() -> None:
    """Envia todos os CSVs da pasta data/raw para o Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    csv_files = list(DATA_RAW_PATH.glob("*.csv"))

    if not csv_files:
        print("Nenhum CSV encontrado em data/raw/")
        return

    print(f"Encontrados {len(csv_files)} arquivos para upload.\n")

    for csv_file in sorted(csv_files):
        upload_file(bucket, csv_file)

    print(f"\nUpload concluído! {len(csv_files)} arquivos enviados.")


if __name__ == "__main__":
    upload_all_csvs()