# 🛒 Olist GCP Pipeline

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white"/>
  <img src="https://img.shields.io/badge/BigQuery-669DF6?style=for-the-badge&logo=googlebigquery&logoColor=white"/>
  <img src="https://img.shields.io/badge/Cloud_Storage-AECBFA?style=for-the-badge&logo=googlecloud&logoColor=black"/>
  <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Data_Studio-4285F4?style=for-the-badge&logo=googledatastudio&logoColor=white"/>
</p>

<p align="center">
  Pipeline de dados end-to-end no Google Cloud Platform analisando <strong>1,55 milhão de registros</strong> de e-commerce brasileiro.
</p>

<p align="center">
  <a href="https://datastudio.google.com/reporting/c4670068-54ff-403d-82a5-bab428a33d99">
    <img src="https://img.shields.io/badge/📊 Acessar Dashboard ao vivo-Click aqui-success?style=for-the-badge"/>
  </a>
</p>

---

## 📌 Visão Geral

Pipeline completo de engenharia de dados construído com GCP, Python e SQL, processando dados reais da **Olist**, maior plataforma de marketplace do Brasil.

> 💡 O dataset contém **1.550.922 registros** distribuídos em 9 tabelas. Para referência, o Microsoft Excel suporta no máximo 1.048.576 linhas por planilha — ou seja, esse volume de dados simplesmente não caberia em uma planilha tradicional. O BigQuery processa tudo isso em menos de 1 segundo.

---

## 🏗️ Arquitetura

```
CSVs (Kaggle/Olist)
        |
        v
[Python 3.12] --> [Cloud Storage] --> [BigQuery] --> [Google Data Studio]
  ingestão          zona de pouso      analytics       dashboard BI
```

---

## 🛠️ Stack

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.12 | Scripts de ingestão e carga |
| google-cloud-storage | 3.10.1 | Upload para Cloud Storage |
| google-cloud-bigquery | 3.41.0 | Carga e queries no BigQuery |
| pandas | 2.3.3 | Leitura e inspeção dos dados |
| gcloud CLI | 566.0.0 | Automação via linha de comando |
| Google Data Studio | - | Dashboard de BI interativo (antigo Looker Studio) |

---

## 📊 Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| customers | 99.441 | Dados dos clientes |
| orders | 99.441 | Pedidos realizados |
| order_items | 112.650 | Itens de cada pedido |
| order_payments | 103.886 | Pagamentos |
| order_reviews | 99.224 | Avaliações dos clientes |
| products | 32.951 | Catálogo de produtos |
| sellers | 3.095 | Vendedores cadastrados |
| geolocation | 1.000.163 | Coordenadas geográficas |
| product_category_translation | 71 | Tradução das categorias |
| **Total** | **1.550.922** | |

---

## 📁 Estrutura do Projeto

```
olist-gcp-pipeline/
├── src/
│   ├── upload_to_gcs.py       # upload dos CSVs para o Cloud Storage
│   └── load_to_bigquery.py    # carga das tabelas no BigQuery
├── sql/
│   ├── 01_receita_mensal.sql
│   ├── 02_top_categorias.sql
│   ├── 03_status_pedidos.sql
│   ├── 04_prazo_entrega_por_estado.sql
│   └── 05_ticket_medio_por_estado.sql
├── data/
│   └── raw/                   # CSVs originais (não versionados)
├── requirements.txt
└── README.md
```

---

## 🔍 Principais Insights

- 📍 **SP** concentra 43% dos pedidos com ticket médio de R$ 137
- 💄 **Health & Beauty** é a categoria com maior receita (R$ 1,25 milhão)
- ✅ **97%** dos pedidos foram entregues com sucesso
- 🛍️ Pico de vendas em **novembro de 2017** (Black Friday): R$ 1,15 milhão
- 🚚 **Roraima** tem o maior prazo médio de entrega: 29 dias

---

## 🚀 Como Reproduzir

### Pré-requisitos

- Conta no Google Cloud Platform
- Python 3.10+
- gcloud CLI instalado e autenticado

### Instalação

```bash
git clone https://github.com/felipecezar01/olist-gcp-pipeline.git
cd olist-gcp-pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuração

```bash
gcloud auth application-default login
gcloud config set project SEU_PROJECT_ID
```

### Execução

```bash
# 1. Upload dos dados para o Cloud Storage
python src/upload_to_gcs.py

# 2. Carga no BigQuery
python src/load_to_bigquery.py
```

---

## 👤 Autor

**Felipe Cezar**

<p>
  <a href="https://linkedin.com/in/felipecezarcruz/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
  </a>
  <a href="https://felipecezar.dev">
    <img src="https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=vercel&logoColor=white"/>
  </a>
  <a href="https://github.com/felipecezar01">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
  </a>
</p>