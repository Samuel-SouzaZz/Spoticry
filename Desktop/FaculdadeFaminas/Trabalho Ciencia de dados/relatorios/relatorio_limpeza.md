# Relatório de Limpeza de Dados - MegaSuper Vendas

## 1. Estatísticas Gerais
- Total de registros: 289813
- Registros duplicados removidos: 0

## 2. Tratamento de Dados
### Valores Ausentes
- id_da_compra: 0 valores ausentes
- data: 0 valores ausentes
- hora: 0 valores ausentes
- cliente: 0 valores ausentes
- produto: 0 valores ausentes
- valor: 0 valores ausentes
- quantidade: 0 valores ausentes
- total: 0 valores ausentes
- status: 0 valores ausentes
- cidade: 0 valores ausentes
- estado: 0 valores ausentes
- pais: 0 valores ausentes
- cep: 0 valores ausentes
- frete: 0 valores ausentes
- pagamento: 0 valores ausentes
- vendedor: 0 valores ausentes
- marca: 0 valores ausentes

### Tipos de Dados
- id_da_compra: int64
- data: object
- hora: object
- cliente: object
- produto: object
- valor: float64
- quantidade: int64
- total: float64
- status: object
- cidade: object
- estado: object
- pais: object
- cep: object
- frete: float64
- pagamento: object
- vendedor: object
- marca: object

### Problemas Corrigidos
- Espaços extras removidos de todas as colunas de texto
- Produtos padronizados para nomes consistentes
- Valores monetários validados e corrigidos
- Quantidades validadas e corrigidas
- Fretes validados e corrigidos
- Totais recalculados e corrigidos
- CEPs ausentes preenchidos com valores sintéticos baseados no estado

## 3. Análise de Produtos
### Top 5 Produtos Mais Vendidos
- pasta de dente: 17971 unidades
- queijo mussarela: 17761 unidades
- manteiga: 17078 unidades
- sabonete: 16789 unidades
- açúcar: 15448 unidades