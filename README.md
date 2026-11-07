# NPS Preditivo — Tech Challenge Fase 1

Projeto de Ciência de Dados desenvolvido como Tech Challenge da Fase 1 da pós-graduação **PosTech (FIAP)** na área de **Ciência de Dados com ênfase em Inteligência Artificial**.

---

## Objetivo do projeto

Uma empresa de e-commerce enfrenta alta variabilidade no Net Promoter Score (NPS) entre diferentes perfis de clientes. Atualmente, o NPS só é coletado **após** o encerramento da jornada de compra, o que impede ações preventivas.

Este projeto tem dois objetivos principais:

1. **Entender quais fatores operacionais** (logística, atendimento, perfil do cliente) realmente influenciam a satisfação do cliente, traduzindo dados em recomendações acionáveis para as áreas de negócio.
2. **Propor um modelo preditivo** capaz de antecipar o NPS antes da aplicação da pesquisa, permitindo que a empresa aja de forma proativa.

---

## Base de dados

Arquivo: `data/desafio_nps_fase_1.csv`

Dataset com **2.500 registros** de pedidos realizados em e-commerce nacional, sem valores nulos. Cada linha representa um pedido único de um cliente.

### Dicionário de variáveis

| Variável | Tipo | Descrição |
|---|---|---|
| `customer_id` | int | Identificador único do cliente |
| `order_id` | int | Identificador único do pedido |
| `customer_age` | int | Idade do cliente (anos) |
| `customer_region` | str | Região geográfica (Norte, Nordeste, Centro-Oeste, Sudeste, Sul) |
| `customer_tenure_months` | int | Tempo de relacionamento com a empresa (meses) |
| `order_value` | float | Valor total do pedido (R$) |
| `items_quantity` | int | Quantidade de itens no pedido |
| `discount_value` | float | Valor de desconto aplicado (R$) |
| `payment_installments` | int | Número de parcelas do pagamento |
| `delivery_time_days` | int | Tempo total de entrega (dias) |
| `delivery_delay_days` | int | Dias de atraso em relação ao prazo prometido |
| `freight_value` | float | Valor do frete (R$) |
| `delivery_attempts` | int | Número de tentativas de entrega (1–3) |
| `customer_service_contacts` | int | Número de contatos do cliente com o suporte |
| `resolution_time_days` | int | Tempo para resolução de problemas (dias) |
| `complaints_count` | int | Número de reclamações registradas |
| `repeat_purchase_30d` | int | Recompra em até 30 dias (0 = não, 1 = sim) |
| `csat_internal_score` | float | Score interno de satisfação (0–10) |
| `nps_score` | float | **Variável alvo** — nota NPS do cliente (0–10) |

### Classificação do NPS

| Faixa | Categoria |
|---|---|
| 9 – 10 | Promotor |
| 7 – 8 | Neutro |
| 0 – 6 | Detrator |

---

## Metodologia

O projeto segue o fluxo padrão de um projeto de Data Science orientado a negócio:

```
1. Entendimento do negócio
       ↓
2. Definição da variável alvo (target)
       ↓
3. Análise Exploratória dos Dados (EDA)
       ↓
4. Pré-processamento e feature engineering
       ↓
5. Modelagem preditiva
       ↓
6. Avaliação e interpretação dos resultados
       ↓
7. Recomendações para o negócio
```

### Abordagem de modelagem

O problema foi tratado como **classificação multiclasse** (Detrator / Neutro / Promotor), por oferecer saídas acionáveis diretamente pelos times de negócio.

Modelos avaliados:
- Baseline: Dummy Classifier (referência mínima)
- Random Forest Classifier
- XGBoost Classifier

Métricas de avaliação: acurácia, F1-score macro, matriz de confusão e feature importance.

---

## Estrutura de pastas

```
projeto1/
├── data/               # Dataset original (não modificar)
│   └── desafio_nps_fase_1.csv
├── notebooks/          # Análises e experimentos em Jupyter Notebook
├── models/             # Modelos treinados e artefatos de pipeline
├── reports/            # Visualizações e outputs gerados para apresentação
└── README.md
```

---

## Como reproduzir os resultados

### Pré-requisitos

- Python 3.9+
- pip

### Instalação das dependências

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost jupyter
```

### Executando a análise

1. Clone ou baixe este repositório
2. Certifique-se de que o arquivo `data/desafio_nps_fase_1.csv` está presente
3. Abra o Jupyter Notebook:

```bash
jupyter notebook notebooks/
```

4. Execute os notebooks na ordem indicada pela numeração dos arquivos (ex.: `01_eda.ipynb`, `02_modelo.ipynb`)

---

## Principais achados

- **NPS da empresa: -80** (84,4% dos clientes são detratores)
- O **atraso na entrega** é o fator com maior impacto negativo no NPS (correlação: -0,60)
- O **número de reclamações** é o segundo fator mais crítico (correlação: -0,50)
- Clientes **sem reclamações** recompram em 69,6% dos casos; com 4+ reclamações, esse número cai para menos de 6%
- Clientes que **recompraram em 30 dias** têm NPS médio de 9,01 vs 3,94 dos que não recompraram
- Região geográfica, idade e valor do pedido têm impacto desprezível no NPS

---

## Autores

Projeto desenvolvido para a Fase 1 do Tech Challenge — PosTech FIAP.
