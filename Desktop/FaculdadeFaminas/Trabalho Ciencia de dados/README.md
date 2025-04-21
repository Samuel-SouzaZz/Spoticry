# Análise de Dados de Vendas - MegaSuper

Este repositório contém a análise de dados de vendas da MegaSuper, incluindo limpeza de dados e análise de regras de associação entre produtos.

## Estrutura do Projeto

```
MegaSuper-Analise-Vendas/
│
├── limpeza_dados.py           # Script principal de limpeza e análise
│
├── dadosSujos/                # Dados originais
│   └── vendas_modificado (2).csv
│
├── dadosLimpos/               # Dados processados
│   ├── dados_limpos.csv
│   └── regras_associacao.csv
│
├── relatorios/                # Documentação e relatórios
│   ├── relatorio_limpeza.md
│   ├── relatorio_associacao.md
│   └── TRATAMENTO_DADOS_FALTANTES.md
│
├── requirements.txt           # Dependências do projeto
├── README.md                  # Este arquivo
├── .gitignore                 # Configuração de arquivos ignorados
└── .gitattributes             # Configuração para Git LFS
```

## Funcionalidades do Script

O script `limpeza_dados.py` implementa as seguintes funcionalidades:

1. **Limpeza de Dados:**
   - Tratamento de valores ausentes
   - Padronização de nomes de produtos
   - Validação e correção de valores monetários
   - Tratamento de CEPs ausentes
   - Validação de quantidades e fretes

2. **Análise de Associação:**
   - Implementação do algoritmo Apriori
   - Geração de regras de associação entre produtos
   - Análise de métricas como suporte, confiança e lift

## Como Executar o Projeto

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o script: `python limpeza_dados.py`

## Resultados

Os principais resultados incluem:
- Relatório de limpeza com estatísticas sobre o processo (`relatorios/relatorio_limpeza.md`)
- Conjunto de regras de associação que podem ser usadas para estratégias de marketing (`relatorios/relatorio_associacao.md`)
- Dataset limpo pronto para análises adicionais (`dadosLimpos/dados_limpos.csv`)
- Documento detalhado sobre o tratamento de dados faltantes (`relatorios/TRATAMENTO_DADOS_FALTANTES.md`)

## Tecnologias Utilizadas

- Python 3.x
- Pandas para manipulação de dados
- MLxtend para implementação do algoritmo Apriori
- Numpy para operações numéricas
- Matplotlib e Seaborn para visualizações (quando aplicável) 