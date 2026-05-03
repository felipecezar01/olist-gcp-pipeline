from pathlib import Path
from google.cloud import bigquery

PROJECT_ID = "olist-pipeline-495119"
DATASET_ID = "olist_ecommerce"
BUCKET_NAME = "olist-gcp-pipeline-raw"

# Mapeamento: nome do arquivo CSV -> nome da tabela no BigQuery
TABLES = {
    "olist_customers_dataset.csv": "customers",
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "product_category_translation",
}


def load_csv_to_bigquery(client: bigquery.Client, csv_filename: str, table_name: str) -> None:
    """Carrega um CSV do Cloud Storage para uma tabela no BigQuery."""
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    uri = f"gs://{BUCKET_NAME}/olist/{csv_filename}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        allow_quoted_newlines=True,   # permite quebras de linha dentro de campos
        allow_jagged_rows=True,       # tolera linhas com colunas faltando
        max_bad_records=1000,         # ignora até 1000 linhas corrompidas
    )

    print(f"Carregando {csv_filename} -> {table_name}...")
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()  # aguarda o job terminar

    table = client.get_table(table_id)
    print(f"  OK -> {table.num_rows} linhas carregadas\n")


def load_all_tables() -> None:
    """Carrega todos os CSVs do bucket para o BigQuery."""
    client = bigquery.Client(project=PROJECT_ID)

    print(f"Iniciando carga para o dataset {DATASET_ID}\n")
    print("=" * 50)

    for csv_filename, table_name in TABLES.items():
        load_csv_to_bigquery(client, csv_filename, table_name)

    print("=" * 50)
    print(f"Carga concluída! {len(TABLES)} tabelas criadas no BigQuery.")


if __name__ == "__main__":
    load_all_tables()
