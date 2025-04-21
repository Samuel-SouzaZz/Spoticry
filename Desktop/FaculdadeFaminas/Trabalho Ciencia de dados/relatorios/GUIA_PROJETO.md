# Guia do Projeto MegaSuper Análise de Vendas

Este documento serve como um guia para facilitar a navegação e avaliação do projeto de análise de dados da MegaSuper Vendas.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

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
│   ├── TRATAMENTO_DADOS_FALTANTES.md
│   └── GUIA_PROJETO.md
│
├── requirements.txt           # Dependências do projeto
├── README.md                  # Visão geral do projeto
├── .gitignore                 # Configuração de arquivos ignorados
└── .gitattributes             # Configuração para Git LFS
```

## Sequência de Avaliação Recomendada

Para uma melhor compreensão do projeto, recomendamos seguir esta sequência de avaliação:

1. **README.md** - Fornece uma visão geral do projeto e suas funcionalidades
2. **relatorios/GUIA_PROJETO.md** (este documento) - Orienta a navegação pelo projeto
3. **relatorios/TRATAMENTO_DADOS_FALTANTES.md** - Detalha como os dados faltantes foram tratados
4. **relatorios/relatorio_limpeza.md** - Apresenta os resultados do processo de limpeza de dados
5. **relatorios/relatorio_associacao.md** - Mostra as regras de associação encontradas
6. **limpeza_dados.py** - O código-fonte, totalmente documentado

## Processo de Limpeza de Dados

O script `limpeza_dados.py` implementa um pipeline completo de limpeza de dados:

1. **Carregamento e Inspeção**: Carrega o dataset original e analisa sua estrutura
2. **Padronização de Dados**: Padroniza nomes de produtos, datas e outros campos
3. **Validação de Valores**: Verifica e corrige valores monetários, quantidades e fretes
4. **Tratamento de CEPs**: Preenche e formata CEPs ausentes ou inválidos
5. **Remoção de Duplicatas**: Identifica e remove registros duplicados
6. **Preenchimento de Valores Ausentes**: Trata valores faltantes em todas as colunas
7. **Verificação de Cálculos**: Garante a consistência nos cálculos de totais
8. **Geração de Relatórios**: Produz relatórios detalhados do processo

## Tratamento de Dados Faltantes

O projeto aborda especificamente o problema de dados faltantes em três colunas principais:
- **Coluna `total`**: 3.685 valores ausentes (de 368.752 registros)
- **Coluna `frete`**: 7.371 valores ausentes (de 368.752 registros)
- **Coluna `vendedor`**: 3.680 valores ausentes (de 368.752 registros)

A abordagem para tratamento destes valores está detalhada no arquivo `TRATAMENTO_DADOS_FALTANTES.md`.

## Análise de Regras de Associação

Após a limpeza dos dados, o script implementa o algoritmo Apriori para encontrar associações entre produtos frequentemente comprados juntos. As regras são avaliadas por:
- **Suporte**: Frequência relativa da ocorrência conjunta
- **Confiança**: Probabilidade condicional
- **Lift**: Força da associação

As regras encontradas podem ser usadas para estratégias de marketing como:
- Disposição de produtos na loja
- Promoções combinadas
- Recomendações personalizadas
- Pacotes de produtos

## Como Executar o Projeto

Para executar o projeto:

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

2. Execute o script principal:
   ```
   python limpeza_dados.py
   ```

O script processará o arquivo de entrada `dadosSujos/vendas_modificado (2).csv` e gerará todos os arquivos de saída nas pastas apropriadas. 