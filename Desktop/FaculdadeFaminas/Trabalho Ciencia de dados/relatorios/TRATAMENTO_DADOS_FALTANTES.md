# Tratamento de Dados Faltantes

## Identificação de Valores Ausentes no Dataset Original

Na análise inicial do dataset `vendas_modificado (2).csv`, foram identificados os seguintes valores ausentes:

- **Coluna `total`**: 3.685 valores ausentes (de 368.752 registros)
- **Coluna `frete`**: 7.371 valores ausentes (de 368.752 registros)
- **Coluna `vendedor`**: 3.680 valores ausentes (de 368.752 registros)

## Estratégias de Tratamento Implementadas

### 1. Valores Monetários Ausentes (total e frete)

Para lidar com valores ausentes nas colunas `total` e `frete`, as seguintes abordagens foram implementadas:

```python
def validar_valor(valor):
    """
    Valida e converte valores monetários para float.
    
    Trata valores ausentes, strings vazias e formatos inválidos.
    Garante que valores estejam dentro de uma faixa razoável (0 a 10.000).
    """
    # Código de implementação
```

```python
def validar_frete(frete):
    """
    Valida e corrige valores de frete.
    
    Trata valores ausentes ou inválidos, garantindo que estejam dentro de uma
    faixa razoável (0 a 1.000).
    """
    # Código de implementação
```

```python
def verificar_calculos(df):
    """
    Verifica e corrige inconsistências nos cálculos de total (valor * quantidade).
    
    Recalcula valores ausentes ou inconsistentes da coluna total.
    """
    # Código de implementação
```

### 2. Valores de Vendedor Ausentes

```python
def tratar_valores_ausentes(df):
    """
    Trata todos os valores ausentes do DataFrame.
    
    Para a coluna vendedor, usa um método de imputação baseado nos vendedores
    mais frequentes por região.
    """
    # Implementação específica para a coluna vendedor
```

### 3. CEPs Ausentes ou Inválidos

Embora no conjunto de dados atual não haja CEPs ausentes após o pré-processamento, o script mantém uma função robusta para lidar com esse cenário:

```python
def tratar_ceps_ausentes(df):
    """
    Preenche CEPs ausentes com valores sintéticos baseados nas informações
    geográficas disponíveis (cidade/estado).
    
    Utiliza um mapeamento dos CEPs mais comuns por cidade para fazer a imputação.
    """
    # Código de implementação
```

## Resultados do Tratamento

Após a aplicação das estratégias de tratamento de dados faltantes, o dataset resultante (`dados_limpos.csv`) não apresenta nenhum valor ausente em qualquer coluna, conforme documentado no relatório de limpeza:

```
### Valores Ausentes
- id_da_compra: 0 valores ausentes
- data: 0 valores ausentes
- hora: 0 valores ausentes
...
- frete: 0 valores ausentes
- pagamento: 0 valores ausentes
- vendedor: 0 valores ausentes
- marca: 0 valores ausentes
```

## Impacto nas Análises Subsequentes

O tratamento adequado dos dados faltantes foi essencial para garantir a qualidade das análises de regras de associação, uma vez que o algoritmo Apriori requer dados completos e consistentes para gerar regras confiáveis.

As estratégias implementadas preservaram a integridade dos dados originais enquanto corrigiam inconsistências e preenchiam valores ausentes de maneira estatisticamente válida. 