import functions_framework
from google.cloud import bigquery, storage
from datetime import datetime, timedelta
import logging

PROJECT_ID = "olist-pipeline-495119"
BUCKET_NAME = "olist-gcp-pipeline-raw"
DATASET_ID = "olist_ecommerce"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.http
def run_pipeline(request):
    """
    Cloud Function principal do pipeline.
    Verifica se há arquivos novos no Cloud Storage
    e os carrega no BigQuery se necessário.
    """
    logger.info(f"Pipeline iniciado em {datetime.now()}")

    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bq_client = bigquery.Client(project=PROJECT_ID)

        bucket = storage_client.bucket(BUCKET_NAME)
        blobs = list(bucket.list_blobs(prefix="olist/"))

        if not blobs:
            logger.info("Nenhum arquivo encontrado no bucket.")
            return {"status": "skip", "message": "Nenhum arquivo encontrado."}, 200

        ontem = datetime.utcnow() - timedelta(days=1)
        arquivos_novos = [
            b for b in blobs
            if b.updated.replace(tzinfo=None) > ontem
        ]

        if not arquivos_novos:
            logger.info("Nenhum arquivo novo desde ontem. Pipeline encerrado.")
            return {
                "status": "skip",
                "message": "Nenhum arquivo novo encontrado.",
                "arquivos_verificados": len(blobs),
                "timestamp": datetime.utcnow().isoformat()
            }, 200

        logger.info(f"{len(arquivos_novos)} arquivo(s) novo(s) encontrado(s).")

        for blob in arquivos_novos:
            table_name = blob.name.split("/")[-1].replace(".csv", "").replace("olist_", "").replace("_dataset", "")
            table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
            uri = f"gs://{BUCKET_NAME}/{blob.name}"

            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                skip_leading_rows=1,
                autodetect=True,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                allow_quoted_newlines=True,
                max_bad_records=1000,
            )

            logger.info(f"Carregando {blob.name} -> {table_id}")
            load_job = bq_client.load_table_from_uri(uri, table_id, job_config=job_config)
            load_job.result()
            logger.info(f"OK: {blob.name} carregado.")

        return {
            "status": "success",
            "message": f"{len(arquivos_novos)} arquivo(s) carregado(s).",
            "timestamp": datetime.utcnow().isoformat()
        }, 200

    except Exception as e:
        logger.error(f"Erro no pipeline: {str(e)}")
        return {"status": "error", "message": str(e)}, 500