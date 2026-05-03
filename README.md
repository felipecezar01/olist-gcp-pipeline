# 🛒 Olist GCP Pipeline

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white"/>
  <img src="https://img.shields.io/badge/BigQuery-669DF6?style=for-the-badge&logo=googlebigquery&logoColor=white"/>
  <img src="https://img.shields.io/badge/Cloud_Storage-AECBFA?style=for-the-badge&logo=googlecloud&logoColor=black"/>
  <img src="https://img.shields.io/badge/Cloud_Functions-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Data_Studio-4285F4?style=for-the-badge&logo=googledatastudio&logoColor=white"/>
</p>

<p align="center">
  Pipeline <strong>ELT</strong> end-to-end no Google Cloud Platform analisando <strong>1,55 milhão de registros</strong> de e-commerce brasileiro.
</p>

<p align="center">
  <a href="https://datastudio.google.com/reporting/c4670068-54ff-403d-82a5-bab428a33d99">
    <img src="https://img.shields.io/badge/📊 Acessar Dashboard ao vivo-Click aqui-success?style=for-the-badge"/>
  </a>
</p>

---

## 📌 Visão Geral

Pipeline completo de engenharia de dados construído com GCP, Python e SQL, processando dados reais da **Olist**, plataforma brasileira de e-commerce que conecta lojistas aos principais marketplaces do país.

> 💡 O dataset contém **1.550.922 registros** distribuídos em 9 tabelas. Para referência, o Microsoft Excel suporta no máximo 1.048.576 linhas por planilha — esse volume de dados simplesmente não caberia em uma planilha tradicional. O BigQuery processa tudo isso em menos de 1 segundo.

---

## 🏗️ Arquitetura

```
CSVs (Kaggle/Olist)
        |
     [Extract]
        |
        v
[Python 3.12] --> [Cloud Storage] --> [BigQuery] --> [Google Data Studio]
   ingestão         zona de pouso      analytics       dashboard BI
                   (Data Lake)      [Load + Transform]
                        |
                        v
              [Cloud Functions]
              [Cloud Scheduler]
               automação ELT
```

---

## 🧠 Conceitos Aplicados

### ELT vs ETL

Este projeto implementa o padrão **ELT (Extract, Load, Transform)**, que é o padrão moderno de engenharia de dados, diferente do ETL tradicional.

No **ETL** antigo, os dados eram transformados antes de chegar ao destino, exigindo servidores intermediários e dificultando o reprocessamento. No **ELT**, os dados são carregados brutos primeiro e as transformações acontecem dentro do próprio data warehouse com SQL. Isso é possível porque ferramentas modernas como o BigQuery têm poder computacional suficiente para transformar dados em escala diretamente na nuvem.

Neste projeto: os CSVs foram extraídos do Kaggle, carregados brutos no BigQuery via Cloud Storage, e as transformações analíticas acontecem nas queries SQL em tempo de consulta.

---

### Data Warehouse Colunar

O **BigQuery** é um **data warehouse colunar serverless**. Bancos de dados tradicionais como PostgreSQL e MySQL armazenam dados orientados a linha, o que é eficiente para buscar registros individuais. O BigQuery armazena dados orientados a coluna: todas as células de uma mesma coluna ficam juntas no disco. Quando você roda `SELECT SUM(valor) FROM pedidos`, ele lê apenas a coluna `valor`, ignorando todas as outras. Em tabelas com milhões de linhas e dezenas de colunas, isso representa uma diferença brutal de performance.

---

### Data Lake e Camadas de Dados

O **Cloud Storage** funciona como a camada **raw** do Data Lake do projeto, seguindo a arquitetura de camadas:

- **Raw (bruto):** dados exatamente como vieram da fonte, nunca modificados
- **Processed (processado):** dados transformados e prontos para análise

Essa separação garante que, se algo der errado no processamento, sempre existe o dado original para reprocessar. É um princípio fundamental de arquitetura de dados.

---

### Serverless

Tanto o **Cloud Functions** quanto o **BigQuery** são serviços **serverless**, ou seja, não existe um servidor ligado 24 horas esperando trabalho. A infraestrutura é alocada dinamicamente quando necessária e desligada em seguida. Você paga apenas pelo tempo de execução real, o que torna o custo próximo de zero para cargas de trabalho intermitentes como pipelines diários.

---

### Infrastructure as Code (IaC)

Todo o ambiente de infraestrutura deste projeto foi criado e configurado via **gcloud CLI (Google Cloud Command Line Interface)**, sem nenhum clique manual no console. Criação do bucket, deploy da Cloud Function, configuração do Cloud Scheduler, regras de IAM e configurações de rede foram todas feitas por comandos reproduzíveis e versionáveis. Esse conceito é chamado de **Infrastructure as Code (IaC)**: tratar infraestrutura como código, permitindo reprodução, versionamento e automação do ambiente completo.

---

### Automação de Pipeline

O pipeline é automatizado com dois serviços do GCP:

- **Cloud Scheduler:** job cron que dispara todos os dias às 6h, enviando uma requisição HTTP autenticada
- **Cloud Functions:** função serverless que acorda, verifica se há arquivos novos no Cloud Storage e, se houver, carrega automaticamente no BigQuery

Essa arquitetura implementa **ingestão incremental**: o pipeline não reprocessa tudo toda vez, apenas o que é novo, economizando tempo e custo.

---

### IAM e Segurança

O projeto aplica o princípio de **menor privilégio** via **IAM (Identity and Access Management)**:

- A Cloud Function tem ingress configurado como `internal`, inacessível pela internet pública
- O Cloud Scheduler se autentica via conta de serviço OIDC antes de acionar a função
- Nenhuma credencial foi versionada no GitHub
- Dados sensíveis protegidos via `.gitignore`

---

### Window Functions SQL

As queries analíticas utilizam **window functions**, um recurso avançado de SQL. Por exemplo, na query de status dos pedidos:

```sql
ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentual
```

O `OVER()` calcula o total geral sem colapsar as linhas do `GROUP BY`, permitindo calcular percentuais em uma única query sem subqueries. É um dos recursos mais importantes do SQL analítico moderno.

---

### Modern Data Stack

A arquitetura do projeto segue o padrão **Modern Data Stack**, stack tecnológica moderna adotada por empresas de dados:

| Camada | Ferramenta | Papel |
|--------|------------|-------|
| Ingestão | Python + gcloud CLI | Extract e Load |
| Armazenamento raw | Cloud Storage | Data Lake |
| Analytics | BigQuery | Data Warehouse |
| Transformação | SQL no BigQuery | Transform |
| Visualização | Google Data Studio | BI |
| Orquestração | Cloud Functions + Scheduler | Automação |

---

## 🛠️ Stack

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.12 | Scripts de ingestão e carga |
| google-cloud-storage | 3.10.1 | Upload para Cloud Storage |
| google-cloud-bigquery | 3.41.0 | Carga e queries no BigQuery |
| pandas | 2.3.3 | Leitura e inspeção dos dados |
| gcloud CLI | 566.0.0 | Infrastructure as Code |
| Cloud Functions | Gen2 | Serverless pipeline automation |
| Cloud Scheduler | - | Cron jobs na nuvem |
| Cloud Logging | - | Observabilidade e monitoramento |
| Google Data Studio | - | Dashboard BI (antigo Looker Studio) |

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
├── cloud_function/
│   ├── main.py                # Cloud Function com lógica de ingestão incremental
│   └── requirements.txt       # dependências do ambiente serverless
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

### Deploy da automação

```bash
# Deploy da Cloud Function
gcloud functions deploy olist-pipeline \
  --gen2 \
  --runtime=python312 \
  --region=southamerica-east1 \
  --source=cloud_function \
  --entry-point=run_pipeline \
  --trigger-http \
  --no-allow-unauthenticated

# Criar job de agendamento diário às 6h
gcloud scheduler jobs create http olist-pipeline-job \
  --location=southamerica-east1 \
  --schedule="0 6 * * *" \
  --uri=SUA_FUNCTION_URL \
  --http-method=POST \
  --oidc-service-account-email=SEU_SERVICE_ACCOUNT
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