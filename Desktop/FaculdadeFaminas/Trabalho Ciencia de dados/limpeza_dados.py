# Limpeza de Dados - MegaSuper Vendas
# Este script implementa o processo de limpeza de dados para o conjunto de dados da MegaSuper Vendas

# Importação das bibliotecas necessárias
import pandas as pd
import numpy as np
from datetime import datetime
import re
import warnings
import os
warnings.filterwarnings('ignore')
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Criação de diretórios se não existirem
os.makedirs("dadosLimpos", exist_ok=True)
os.makedirs("relatorios", exist_ok=True)

def carregar_dados(caminho_arquivo):
    """
    Carrega o arquivo CSV de vendas e retorna um DataFrame.
    
    Args:
        caminho_arquivo (str): Caminho do arquivo CSV a ser carregado.
        
    Returns:
        pandas.DataFrame: DataFrame contendo os dados de vendas.
        
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
        pd.errors.EmptyDataError: Se o arquivo estiver vazio.
    """
    return pd.read_csv(caminho_arquivo)

def limpar_texto(texto):
    """
    Remove espaços extras e converte texto para minúsculas.
    
    Args:
        texto (str): Texto a ser limpo.
        
    Returns:
        str: Texto limpo, sem espaços extras e em minúsculas.
    """
    if pd.isna(texto):
        return texto
    return str(texto).strip().lower()

def padronizar_produto(produto):
    """
    Padroniza nomes de produtos organizados por categorias.
    
    Esta função mapeia diferentes variações de nomes de produtos para um nome padrão,
    organizados por categorias como Higiene Pessoal, Laticínios, Limpeza, etc.
    
    Args:
        produto (str): Nome do produto a ser padronizado.
        
    Returns:
        str: Nome padronizado do produto ou o próprio produto se não encontrar correspondência.
    """
    if pd.isna(produto):
        return produto
    
    produto = str(produto).lower().strip()
    
    # Pré-processamento para remover caracteres especiais e termos comuns irrelevantes
    produto = re.sub(r'[^\w\s]', ' ', produto)  # Remove caracteres especiais
    produto = re.sub(r'\s+', ' ', produto)      # Remove espaços duplicados
    produto = produto.replace('produto', '').replace('item', '').strip()
    
    # Correção para erros de digitação específicos encontrados nos dados
    correcoes_especificas = {
        'amaciayte': 'amaciante',
        'arroc': 'arroz',
        'açúcaz': 'açúcar',
        'cafc': 'café',
        'caff': 'café',
        'caft': 'café',
        'clfé': 'café',
        'cnfé': 'café',
        'condibionador': 'condicionador',
        'condicioiador': 'condicionador',
        'deqergente': 'detergente',
        'desinfekante': 'desinfetante',
        'desinfetanue': 'desinfetante',
        'deterwente': 'detergente',
        'ieijão': 'feijão',
        'macawrão': 'macarrão',
        'macirrão': 'macarrão',
        'majarrão': 'macarrão',
        'manteigt': 'manteiga',
        'mqcarrão': 'macarrão',
        'presuntd': 'presunto',
        'sabonepe': 'sabonete',
        'scl': 'sal',
        'tal': 'sal',
        'zabonete': 'sabonete'
    }
    
    # Verifica se o produto está na lista de correções específicas
    if produto in correcoes_especificas:
        return correcoes_especificas[produto]
    
    # Mapeamento organizado por categorias
    mapeamento = {
        # Higiene Pessoal
        'pasta de dente': [
            'pasta dental', 'creme dental', 'pasta', 'colgate', 'sensodyne', 
            'oral-b', 'creme de dente', 'gel dental', 'dentifrício', 'pasta oral',
            'close up', 'sorriso', 'oral b', 'escova e pasta', 'pasta dentes'
        ],
        'sabonete': [
            'sabão', 'sabonete líquido', 'sabonete em barra', 'sabonete antibacteriano', 
            'sabonete íntimo', 'sabão em barra', 'dove', 'lux', 'protex', 'palmolive',
            'nivea', 'sabonete hidratante', 'sabonete perfumado', 'soap'
        ],
        'condicionador': [
            'condicionador capilar', 'creme de pentear', 'máscara de tratamento', 
            'creme de cabelo', 'condicionador antiqueda', 'condicionador hidratante',
            'conditioner', 'acondicionador', 'creme rinse', 'condicionador cabelos'
        ],
        'shampoo': [
            'xampu', 'shampoo anticaspa', 'shampoo hidratante', 'shampoo antiqueda',
            'shampoo para cabelos', 'shampoo especializado', 'xampu', 'shampo',
            'champô', 'shampoo cabelo', 'pantene', 'head shoulders', 'h s',
            'head and shoulders', 'elseve', 'seda', 'clear men', 'clear'
        ],
        'desodorante': [
            'desodorante roll on', 'desodorante aerosol', 'antitranspirante', 
            'desodorante spray', 'deo', 'rexona', 'nivea men', 'axe', 'dove deo'
        ],
        'papel higiênico': [
            'papel higienico', 'papel sanitário', 'rolo de papel', 'papel de banheiro',
            'paper higienico', 'neve', 'personal', 'papel wc', 'papel de toilet'
        ],

        # Laticínios
        'queijo mussarela': [
            'mussarela', 'queijo', 'queijo muçarela', 'queijo muzzarela', 
            'queijo mozarela', 'queijo fatiado', 'queijo para lanche', 'queijo musarela',
            'queijo muzarela', 'mozzarella', 'queijo branco', 'queijo para pizza'
        ],
        'manteiga': [
            'margarina', 'manteiga sem sal', 'manteiga com sal', 'manteiga light',
            'manteiga vegetal', 'creme vegetal', 'margarina light', 'qualy',
            'doriana', 'delícia', 'becel', 'manteiga extra', 'butter', 'margarine'
        ],
        'leite': [
            'leite integral', 'leite desnatado', 'leite semidesnatado', 
            'leite em pó', 'leite condensado', 'leite zero lactose', 'leite uht',
            'leite caixinha', 'leite garrafa', 'leite pasteurizado', 'milk',
            'leite longa vida', 'leite fresco', 'ninho', 'molico', 'itambé', 'parmalat'
        ],
        'iogurte': [
            'yogurt', 'iogurte natural', 'iogurte grego', 'iogurte light',
            'iogurte desnatado', 'iogurte integral', 'danone', 'yakult',
            'iogurte de frutas', 'activia', 'yoghurt', 'coalhada', 'danoninho',
            'iogurte liquido', 'iogurte batido', 'iogurte de morango'
        ],
        'requeijão': [
            'requeijao', 'requeijão cremoso', 'requeijão light', 'cream cheese',
            'catupiry', 'philadelphia', 'requeijão tradicional', 'queijo cremoso'
        ],

        # Limpeza
        'papel toalha': [
            'toalha de papel', 'papel absorvente', 'papel toalha interfolhado',
            'guardanapo', 'papel multiuso', 'papel de cozinha', 'snob',
            'kitchen paper', 'papel descartavel', 'toalha papel'
        ],
        'desinfetante': [
            'desinfetante líquido', 'desinfetante em pó', 'desinfetante concentrado',
            'desinfetante spray', 'água sanitária', 'cloro', 'pinho sol', 'kalipto',
            'lysoform', 'veja', 'ajax', 'casa e perfume', 'alvejante', 'sanitizer'
        ],
        'detergente': [
            'detergente líquido', 'detergente em pó', 'detergente concentrado',
            'sabão em pó', 'lava louças', 'detergente neutro', 'ypê', 'limpol',
            'minuano', 'omo', 'ariel', 'brilhante', 'ace', 'washing powder',
            'detergente para pratos', 'sabão para louça', 'dish soap'
        ],
        'amaciante': [
            'amaciante de roupas', 'amaciante concentrado', 'comfort', 'downy',
            'mon bijou', 'baby soft', 'fofo', 'softener', 'amaciador', 
            'amaciante de tecidos', 'suavizante'
        ],

        # Bebidas
        'cerveja': [
            'cerveja lata', 'cerveja garrafa', 'cerveja long neck', 
            'cerveja artesanal', 'chopp', 'cerveja pilsen', 'cerveja puro malte',
            'skol', 'brahma', 'antarctica', 'heineken', 'budweiser', 'stella artois',
            'beer', 'cerveja 600ml', 'cerveja pack', 'cerveja latinha'
        ],
        'refrigerante': [
            'refri', 'coca', 'guaraná', 'fanta', 'sprite', 'soda',
            'bebida gaseificada', 'refrigerante cola', 'refrigerante zero',
            'coca cola', 'coca-cola', 'zero', 'pepsi', 'kuat', 'guarana antarctica',
            'sukita', 'soda limonada', 'soft drink', 'coke', 'tonica', 'h2oh'
        ],
        'café': [
            'café em pó', 'café solúvel', 'café torrado', 'café moído',
            'café expresso', 'café instantâneo', 'cápsula de café', 'nespresso',
            'pilão', 'melitta', '3 corações', 'café forte', 'café tradicional',
            'coffee', 'café especial', 'café gourmet', 'café prima', 'nescafé'
        ],
        'suco': [
            'suco de fruta', 'suco natural', 'suco de caixinha', 'suco em pó',
            'tang', 'del valle', 'juice', 'néctar', 'suco integral',
            'suco concentrado', 'refresco', 'suco de laranja', 'suco de uva'
        ],
        'água': [
            'agua', 'água mineral', 'água com gás', 'água sem gás', 'água de coco',
            'crystal', 'indaiá', 'bonafont', 'mineral water', 'h2o',
            'água garrafa', 'água galão', 'água 500ml', 'água natural'
        ],
        'vinho': [
            'vinho tinto', 'vinho branco', 'vinho rose', 'vinho suave', 'vinho seco',
            'vinho de mesa', 'vinho fino', 'wine', 'vinhos', 'espumante', 'champagne',
            'prosecco'
        ],

        # Alimentos Básicos
        'arroz': [
            'arroz branco', 'arroz integral', 'arroz parboilizado',
            'arroz arbório', 'arroz basmati', 'arroz japonês', 'tio joão',
            'camil', 'prato fino', 'arroz agulhinha', 'rice', 'arroz solto'
        ],
        'feijão': [
            'feijão carioca', 'feijão preto', 'feijão branco',
            'feijão fradinho', 'feijão verde', 'feijão vermelho', 'feijao',
            'beans', 'feijão kilo', 'feijão pacote', 'feijão camil', 'kicaldo'
        ],
        'macarrão': [
            'massa', 'espaguete', 'penne', 'parafuso', 'nhoque',
            'talharim', 'fettuccine', 'massa para lasanha', 'spaghetti',
            'pasta', 'adria', 'barilla', 'renata', 'galo', 'macarrão instantâneo',
            'miojo', 'cup noodles', 'nissin', 'macarrão integral'
        ],
        'molho de tomate': [
            'molho', 'extrato de tomate', 'polpa de tomate',
            'molho pronto', 'molho de pizza', 'passata', 'pomarola', 'quero',
            'heinz', 'tomato sauce', 'molho de macarrão', 'sauce', 'ketchup'
        ],
        'farinha': [
            'farinha de trigo', 'farinha de milho', 'farinha de mandioca',
            'farinha de rosca', 'fubá', 'polvilho', 'maizena', 'farinha panko',
            'flour', 'amido de milho', 'farinha lactea', 'farinha integral'
        ],
        'carvão': [
            'carvão vegetal', 'briquete', 'carvão para churrasco', 'carvão especial',
            'carvão ecológico'
        ],

        # Temperos e Condimentos
        'óleo': [
            'óleo de soja', 'óleo de girassol', 'óleo de canola',
            'óleo vegetal', 'azeite', 'óleo de milho', 'óleo de coco',
            'soya', 'oil', 'óleo de oliva', 'lisa', 'liza', 'sadia',
            'gordura', 'azeite extra virgem', 'azeite gallo', 'azeite andorinha'
        ],
        'açúcar': [
            'açúcar refinado', 'açúcar cristal', 'açúcar mascavo',
            'açúcar demerara', 'adoçante', 'açúcar orgânico', 'açucar',
            'sugar', 'união', 'guarani', 'stevia', 'sucralose', 'açúcar light',
            'açúcar confeiteiro', 'açúcar de confeiteiro', 'açúcar em pó'
        ],
        'sal': [
            'sal refinado', 'sal grosso', 'sal marinho',
            'sal light', 'sal iodado', 'sal rosa', 'sal do himalaia',
            'salt', 'sal de cozinha', 'saleiro', 'sal cisne', 'sal temperado'
        ],
        'tempero': [
            'tempero pronto', 'mix de temperos', 'tempero sazon', 'knorr', 'ajinomoto',
            'tempero completo', 'caldo', 'caldo em pó', 'caldo em cubos', 'seasoning',
            'pimenta', 'cominho', 'orégano', 'manjericão', 'alecrim', 'louro'
        ],

        # Frutas e Vegetais
        'banana': [
            'banana prata', 'banana nanica', 'banana da terra', 'banana maçã',
            'cacho de banana', 'banana ouro', 'banana verde', 'bananas'
        ],
        'maçã': [
            'maça', 'maça fuji', 'maça gala', 'maça verde', 'maça argentina',
            'apple', 'maças', 'maçãs', 'maçãs vermelhas'
        ],
        'batata': [
            'batata inglesa', 'batata doce', 'batata baroa', 'batata asterix',
            'batatas', 'potato', 'potatoes', 'batata kg', 'batata lavada'
        ],
        'tomate': [
            'tomate italiano', 'tomate cereja', 'tomate salada', 'tomate longa vida',
            'tomates', 'tomato', 'tomate kg', 'tomate para molho'
        ],
        'cebola': [
            'cebola branca', 'cebola roxa', 'cebola amarela', 'cebola nacional',
            'onion', 'cebolas', 'cebola kg', 'cebola média'
        ],

        # Outros
        'fralda': [
            'fralda descartável', 'fralda geriátrica', 'fralda infantil',
            'fralda pampers', 'fralda noturna', 'fralda premium', 'pampers',
            'huggies', 'mamy poko', 'diapers', 'fralda tamanho', 'fralda pacote'
        ],
        'chocolate': [
            'chocolate ao leite', 'chocolate amargo', 'chocolate branco',
            'barra de chocolate', 'bombom', 'chocolate em pó', 'cacau em pó',
            'garoto', 'nestlé', 'lacta', 'milka', 'lindt', 'hershey', 'chocolates'
        ],
        'pão': [
            'pão francês', 'pão de forma', 'pão integral', 'pão de centeio',
            'pão sírio', 'pão de hambúrguer', 'pão de hot dog', 'bread',
            'pão pullman', 'bisnaguinha', 'pão caseiro', 'pão light'
        ],
        'biscoito': [
            'bolacha', 'cookie', 'biscoito doce', 'biscoito salgado', 'biscoito recheado',
            'wafer', 'cracker', 'rosquinha', 'cookies', 'oreo', 'passatempo',
            'trakinas', 'club social', 'água e sal', 'cream cracker'
        ],
        'presunto': [
            'presunto cozido', 'presunto parma', 'presunto royale', 'presunto defumado',
            'apresuntado', 'ham', 'presunto fatiado', 'presunto magro'
        ]
    }
    
    # Busca pelo produto no mapeamento - match exato
    for padrao, variacoes in mapeamento.items():
        if produto in variacoes or produto == padrao:
            return padrao
    
    # Busca pelo produto no mapeamento - substring match
    for padrao, variacoes in mapeamento.items():
        if any(variacao in produto for variacao in variacoes) or padrao in produto:
            return padrao
    
    # Busca pelo produto no mapeamento - palavras-chave
    palavras_produto = set(produto.split())
    for padrao, variacoes in mapeamento.items():
        # Cria um conjunto de todas as palavras nas variações
        palavras_variacoes = set()
        for variacao in variacoes:
            palavras_variacoes.update(variacao.split())
        
        # Verifica se há pelo menos 2 palavras em comum ou uma proporção significativa
        palavras_comuns = palavras_produto.intersection(palavras_variacoes)
        if len(palavras_comuns) >= 2 or (palavras_produto and len(palavras_comuns) / len(palavras_produto) >= 0.5):
            return padrao
    
    # Busca por similaridade para casos específicos - distância de edição
    if len(produto) > 3:  # Apenas para produtos com mais de 3 caracteres
        for padrao in list(mapeamento.keys()) + list(correcoes_especificas.values()):
            # Calcula a distância de edição (Levenshtein)
            distancia = sum(1 for a, b in zip(produto, padrao) if a != b) + abs(len(produto) - len(padrao))
            # Se a distância for pequena em relação ao tamanho do produto
            if distancia <= len(produto) * 0.3:  # Até 30% de diferença
                return padrao
            
    # Se não encontrou em nenhuma categoria, retorna o próprio produto
    return produto

def validar_valor(valor):
    """
    Valida e converte valores monetários.
    
    Args:
        valor (str/float): Valor a ser validado.
        
    Returns:
        float: Valor convertido e validado ou np.nan se inválido.
    """
    try:
        valor = float(str(valor).replace('R$', '').replace(',', '.').strip())
        if 0 <= valor <= 10000:  # Limite razoável para um item
            return valor
    except:
        pass
    return np.nan

def validar_quantidade(quantidade):
    """
    Valida e corrige quantidades de produtos.
    
    Args:
        quantidade (int/str): Quantidade a ser validada.
        
    Returns:
        int: Quantidade validada ou 1 se inválida.
    """
    try:
        quantidade = int(quantidade)
        if 1 <= quantidade <= 100:  # Limite razoável para uma compra
            return quantidade
    except:
        pass
    return 1

def validar_frete(frete):
    """
    Valida e corrige valores de frete.
    
    Args:
        frete (float/str): Valor do frete a ser validado.
        
    Returns:
        float: Valor do frete validado ou 0 se inválido.
    """
    try:
        frete = float(str(frete).replace('R$', '').replace(',', '.').strip())
        if 0 <= frete <= 1000:  # Limite razoável para frete
            return frete
    except:
        pass
    return 0

def tratar_ceps_ausentes(df):
    """
    Trata CEPs ausentes usando o padrão mais comum por cidade.
    
    Args:
        df (pandas.DataFrame): DataFrame contendo os dados.
        
    Returns:
        pandas.DataFrame: DataFrame com CEPs ausentes preenchidos.
    """
    # Criar uma cópia para não modificar o original
    df_temp = df.copy()
    
    # Encontrar o CEP mais comum por cidade
    cep_por_cidade = df_temp.groupby('cidade')['cep'].agg(
        lambda x: x.mode()[0] if not x.mode().empty and not pd.isna(x.mode()[0]) else None
    )
    
    # Encontrar o CEP mais comum por estado para usar como fallback
    cep_por_estado = df_temp.groupby('estado')['cep'].agg(
        lambda x: x.mode()[0] if not x.mode().empty and not pd.isna(x.mode()[0]) else None
    )
    
    # Encontrar o CEP mais comum geral para usar como último recurso
    cep_geral = df_temp['cep'].mode()[0] if not df_temp['cep'].mode().empty else None
    
    # Mapeamento de prefixos de CEP por estado para gerar CEPs sintéticos
    prefixos_cep = {
        'sp': '01000',
        'rj': '20000',
        'mg': '30000',
        'es': '29000',
        'ba': '40000',
        'se': '49000',
        'pe': '50000',
        'al': '57000',
        'pb': '58000',
        'rn': '59000',
        'ce': '60000',
        'pi': '64000',
        'ma': '65000',
        'pa': '66000',
        'ap': '68900',
        'am': '69000',
        'ac': '69900',
        'rr': '69300',
        'df': '70000',
        'go': '74000',
        'to': '77000',
        'mt': '78000',
        'ms': '79000',
        'pr': '80000',
        'sc': '88000',
        'rs': '90000'
    }
    
    # Função para preencher CEPs ausentes
    def preencher_cep(row):
        if pd.isna(row['cep']):
            # Tenta usar o CEP da cidade
            cep_cidade = cep_por_cidade.get(row['cidade'])
            if cep_cidade is not None:
                return cep_cidade
            
            # Se não tiver CEP da cidade, tenta usar o CEP do estado
            cep_estado = cep_por_estado.get(row['estado'])
            if cep_estado is not None:
                return cep_estado
            
            # Se não tiver nenhum dos anteriores, usa o CEP geral
            if cep_geral is not None:
                return cep_geral
            
            # Se ainda não tiver CEP, gera um sintético baseado no estado
            estado = str(row['estado']).lower().strip()
            if estado in prefixos_cep:
                # Usa o prefixo do estado + 3 dígitos aleatórios
                import random
                sufixo = str(random.randint(0, 999)).zfill(3)
                return f"{prefixos_cep[estado]}-{sufixo}"
            
            # Último recurso - CEP genérico para o Brasil
            return "00000-000"
        
        return row['cep']
    
    # Aplica a função de preenchimento
    df_temp['cep'] = df_temp.apply(preencher_cep, axis=1)
    
    return df_temp

def validar_cep(cep):
    """
    Valida e formata CEPs brasileiros.
    
    Args:
        cep (str): CEP a ser validado.
        
    Returns:
        str: CEP formatado (XXXXX-XXX) ou None se inválido.
    """
    if pd.isna(cep):
        return None
    
    # Converter para string e remover caracteres não numéricos
    cep = str(cep)
    cep = ''.join(filter(str.isdigit, cep))
    
    # Verificar se tem 8 dígitos
    if len(cep) != 8:
        return None
    
    # Formatar CEP (XXXXX-XXX)
    cep_formatado = f"{cep[:5]}-{cep[5:]}"
    
    return cep_formatado

def gerar_relatorio(df, df_original):
    """
    Gera um relatório detalhado do processo de limpeza.
    
    Args:
        df (pandas.DataFrame): DataFrame após a limpeza.
        df_original (pandas.DataFrame): DataFrame original.
        
    Returns:
        str: Conteúdo do relatório em formato markdown.
    """
    relatorio = []
    relatorio.append("# Relatório de Limpeza de Dados - MegaSuper Vendas\n")
    
    # Estatísticas Gerais
    relatorio.append("## 1. Estatísticas Gerais")
    relatorio.append(f"- Total de registros: {len(df)}")
    relatorio.append(f"- Registros duplicados removidos: {len(df_original) - len(df)}\n")
    
    # Valores Ausentes
    relatorio.append("## 2. Tratamento de Dados")
    relatorio.append("### Valores Ausentes")
    for coluna in df.columns:
        nulos = df[coluna].isnull().sum()
        relatorio.append(f"- {coluna}: {nulos} valores ausentes")
    
    # Tipos de Dados
    relatorio.append("\n### Tipos de Dados")
    for coluna in df.columns:
        tipo = df[coluna].dtype
        relatorio.append(f"- {coluna}: {tipo}")
    
    # Problemas Corrigidos
    relatorio.append("\n### Problemas Corrigidos")
    relatorio.append("- Espaços extras removidos de todas as colunas de texto")
    relatorio.append("- Produtos padronizados para nomes consistentes")
    relatorio.append("- Valores monetários validados e corrigidos")
    relatorio.append("- Quantidades validadas e corrigidas")
    relatorio.append("- Fretes validados e corrigidos")
    relatorio.append("- Totais recalculados e corrigidos")
    relatorio.append("- CEPs ausentes preenchidos com valores sintéticos baseados no estado")
    
    # Análise de Produtos
    relatorio.append("\n## 3. Análise de Produtos")
    relatorio.append("### Top 5 Produtos Mais Vendidos")
    top_produtos = df['produto'].value_counts().head(5)
    for produto, quantidade in top_produtos.items():
        relatorio.append(f"- {produto}: {quantidade} unidades")
    
    return "\n".join(relatorio)

def padronizar_data(data):
    """
    Padroniza datas para o formato YYYY-MM-DD.
    
    Args:
        data (str): Data no formato original.
        
    Returns:
        str: Data padronizada no formato YYYY-MM-DD ou None se inválida.
    """
    if pd.isna(data):
        return None
    
    try:
        # Tenta converter para datetime
        data_dt = pd.to_datetime(data, format='%d/%m/%Y', errors='coerce')
        if pd.isna(data_dt):
            data_dt = pd.to_datetime(data, format='%Y-%m-%d', errors='coerce')
        
        if not pd.isna(data_dt):
            return data_dt.strftime('%Y-%m-%d')
    except:
        pass
    return None

def padronizar_hora(hora):
    """
    Padroniza horas para o formato HH:MM:SS.
    
    Args:
        hora (str): Hora no formato original.
        
    Returns:
        str: Hora padronizada no formato HH:MM:SS ou None se inválida.
    """
    if pd.isna(hora):
        return None
    
    try:
        # Remove caracteres não numéricos
        hora_limpa = re.sub(r'[^\d]', '', str(hora))
        
        # Completa com zeros à esquerda se necessário
        hora_limpa = hora_limpa.zfill(6)
        
        # Formata para HH:MM:SS
        hora_formatada = f"{hora_limpa[:2]}:{hora_limpa[2:4]}:{hora_limpa[4:]}"
        
        # Valida se é uma hora válida
        datetime.strptime(hora_formatada, '%H:%M:%S')
        return hora_formatada
    except:
        pass
    return None

def validar_valores_numericos(df):
    """
    Valida e converte colunas numéricas para o formato adequado.
    
    Args:
        df (pandas.DataFrame): DataFrame com os dados.
        
    Returns:
        pandas.DataFrame: DataFrame com valores numéricos padronizados.
    """
    # Colunas numéricas para processar
    colunas_numericas = ['valor', 'quantidade', 'total', 'frete']
    
    for coluna in colunas_numericas:
        if coluna in df.columns:
            # Função para limpar e converter valores
            def limpar_valor(x):
                if pd.isna(x) or str(x).strip() == '':
                    return np.nan
                
                # Remove caracteres não numéricos exceto ponto e vírgula
                valor_limpo = re.sub(r'[^\d.,]', '', str(x))
                
                # Se a string for muito longa, pega apenas os primeiros caracteres
                if len(valor_limpo) > 20:
                    valor_limpo = valor_limpo[:20]
                
                # Substitui vírgula por ponto
                valor_limpo = valor_limpo.replace(',', '.')
                
                # Remove pontos extras, mantendo apenas o último
                partes = valor_limpo.split('.')
                if len(partes) > 2:
                    valor_limpo = partes[0] + '.' + ''.join(partes[1:])
                
                try:
                    return float(valor_limpo)
                except:
                    return np.nan
            
            # Aplica a função de limpeza
            df[coluna] = df[coluna].apply(limpar_valor)
            
            # Substitui valores inválidos por NaN
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
    
    return df

def tratar_duplicatas(df):
    """
    Remove registros duplicados, mantendo o primeiro registro.
    
    Args:
        df (pandas.DataFrame): DataFrame com os dados.
        
    Returns:
        pandas.DataFrame: DataFrame sem duplicatas.
    """
    # Colunas para verificar duplicatas
    colunas_duplicadas = ['id_da_compra', 'data', 'hora', 'cliente', 'produto']
    colunas_disponiveis = [col for col in colunas_duplicadas if col in df.columns]
    
    # Remove duplicatas
    df_sem_duplicatas = df.drop_duplicates(subset=colunas_disponiveis, keep='first')
    
    return df_sem_duplicatas

def verificar_calculos(df):
    """
    Verifica e corrige cálculos da coluna total.
    
    Args:
        df (pandas.DataFrame): DataFrame com os dados.
        
    Returns:
        pandas.DataFrame: DataFrame com cálculos corrigidos.
    """
    if all(col in df.columns for col in ['valor', 'quantidade', 'frete', 'total']):
        # Calcula o total correto
        df['total_calculado'] = df['valor'] * df['quantidade'] + df['frete']
        
        # Verifica diferenças maiores que 0.01
        df['diferenca'] = abs(df['total'] - df['total_calculado'])
        df.loc[df['diferenca'] > 0.01, 'total'] = df['total_calculado']
        
        # Remove colunas auxiliares
        df = df.drop(['total_calculado', 'diferenca'], axis=1)
    
    return df

def tratar_valores_ausentes(df):
    """
    Trata valores ausentes usando estratégias específicas para cada coluna.
    
    Args:
        df (pandas.DataFrame): DataFrame com os dados.
        
    Returns:
        pandas.DataFrame: DataFrame com valores ausentes tratados.
    """
    # Estratégias para cada coluna
    estrategias = {
        'valor': lambda x: x.fillna(x.mean()),
        'quantidade': lambda x: x.fillna(1),
        'frete': lambda x: x.fillna(0),
        'vendedor': lambda x: x.fillna('Não Especificado'),
        'marca': lambda x: x.fillna('Não Especificada')
    }
    
    # Aplica as estratégias para colunas individuais
    for coluna, estrategia in estrategias.items():
        if coluna in df.columns:
            df[coluna] = estrategia(df[coluna])
    
    # Trata a coluna total separadamente
    if 'total' in df.columns:
        df['total'] = df.apply(
            lambda row: row['valor'] * row['quantidade'] + row['frete'] 
            if pd.isna(row['total']) else row['total'],
            axis=1
        )
    
    return df

def validar_padronizacao_produtos(df):
    """
    Valida a eficácia da padronização de produtos, identificando possíveis
    produtos similares que não foram padronizados corretamente.
    
    Args:
        df (pandas.DataFrame): DataFrame contendo os dados com produtos padronizados.
        
    Returns:
        pandas.DataFrame: O mesmo DataFrame de entrada.
        
    Prints:
        Estatísticas de validação e alertas sobre possíveis produtos não padronizados.
    """
    produtos_unicos = df['produto'].unique()
    total_produtos = len(produtos_unicos)
    print(f"Total de categorias de produtos após padronização: {total_produtos}")
    
    # Verifica se há possíveis produtos similares usando distância de Levenshtein
    produtos_potencialmente_similares = []
    
    for i, prod1 in enumerate(produtos_unicos):
        for prod2 in produtos_unicos[i+1:]:
            # Calcula distância de Levenshtein simples
            distancia = sum(1 for a, b in zip(prod1, prod2) if a != b) + abs(len(prod1) - len(prod2))
            
            # Se a distância for pequena mas não zero, pode ser um produto similar não padronizado
            if 0 < distancia <= 3 and len(prod1) > 3 and len(prod2) > 3:
                produtos_potencialmente_similares.append((prod1, prod2, distancia))
    
    # Relatório de possíveis produtos similares
    if produtos_potencialmente_similares:
        print("\nAlerta: Possíveis produtos similares que poderiam ser padronizados:")
        for prod1, prod2, dist in sorted(produtos_potencialmente_similares, key=lambda x: x[2]):
            print(f"  - '{prod1}' e '{prod2}' (distância: {dist})")
    else:
        print("\nValidação concluída: Nenhum produto similar encontrado que precise de padronização adicional.")
    
    # Analisa frequência dos produtos padronizados
    contagem_produtos = df['produto'].value_counts()
    produtos_raros = contagem_produtos[contagem_produtos <= 5]
    
    if not produtos_raros.empty:
        print(f"\nProdutos com 5 ou menos ocorrências ({len(produtos_raros)} produtos):")
        for produto, contagem in produtos_raros.items():
            print(f"  - '{produto}': {contagem} ocorrências")
    
    return df

def analisar_regras_associacao(df, min_support=0.01, min_confidence=0.3):
    """
    Analisa regras de associação entre produtos usando o algoritmo Apriori.
    
    Args:
        df (pandas.DataFrame): DataFrame contendo os dados limpos.
        min_support (float): Suporte mínimo para regras de associação (padrão: 0.01).
        min_confidence (float): Confiança mínima para regras de associação (padrão: 0.3).
        
    Returns:
        tuple: (DataFrame com conjuntos frequentes, DataFrame com regras de associação)
        
    Prints:
        Informações sobre regras de associação mais relevantes.
    """
    print("Preparando dados para análise de regras de associação...")
    
    # Agrupar compras por ID da compra
    compras_por_id = df.groupby('id_da_compra')['produto'].apply(list).reset_index()
    
    # Converter para o formato de transações
    transacoes = compras_por_id['produto'].tolist()
    
    # Remover duplicatas em cada transação (se o mesmo produto foi comprado múltiplas vezes)
    transacoes = [list(set(transacao)) for transacao in transacoes]
    
    print(f"Total de transações para análise: {len(transacoes)}")
    
    # Aplicar algoritmo Apriori para encontrar conjuntos de itens frequentes
    print(f"Aplicando algoritmo Apriori (min_support={min_support})...")
    
    # Converter transações para formato binário
    te = TransactionEncoder()
    te_ary = te.fit(transacoes).transform(transacoes)
    df_transacoes = pd.DataFrame(te_ary, columns=te.columns_)
    
    # Encontrar conjuntos frequentes
    frequent_itemsets = apriori(df_transacoes, min_support=min_support, use_colnames=True)
    
    # Se nenhum conjunto frequente for encontrado, ajustar o suporte mínimo
    if len(frequent_itemsets) == 0:
        novo_min_support = min_support / 2
        print(f"Nenhum conjunto frequente encontrado. Reduzindo min_support para {novo_min_support}...")
        frequent_itemsets = apriori(df_transacoes, min_support=novo_min_support, use_colnames=True)
    
    print(f"Conjuntos frequentes encontrados: {len(frequent_itemsets)}")
    
    # Gerar regras de associação
    if len(frequent_itemsets) > 0:
        print(f"Gerando regras de associação (min_confidence={min_confidence})...")
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
        
        # Adicionar métricas de lift e conviction
        rules["lift"] = rules["lift"].round(4)
        
        # Ordenar por lift
        rules = rules.sort_values("lift", ascending=False)
        
        # Mostrar as regras mais relevantes (alto lift)
        print("\nRegras de associação mais relevantes (top 10 por lift):")
        for i, row in rules.head(10).iterrows():
            antecedentes = ', '.join(list(row['antecedents']))
            consequentes = ', '.join(list(row['consequents']))
            print(f"Regra {i+1}: {antecedentes} → {consequentes}")
            print(f"   Suporte: {row['support']:.4f}, Confiança: {row['confidence']:.4f}, Lift: {row['lift']:.4f}")
        
        # Salvar as regras em um arquivo CSV
        rules.to_csv("dadosLimpos/regras_associacao.csv", index=False)
        print("\nRegras de associação salvas em: dadosLimpos/regras_associacao.csv")
        
        return frequent_itemsets, rules
    else:
        print("Não foi possível encontrar regras de associação com os parâmetros especificados.")
        return frequent_itemsets, None

def gerar_relatorio_associacao(rules, file_path="relatorios/relatorio_associacao.md"):
    """
    Gera um relatório detalhado sobre as regras de associação encontradas.
    
    Args:
        rules (pandas.DataFrame): DataFrame contendo as regras de associação.
        file_path (str): Caminho onde o relatório será salvo.
        
    Returns:
        None
    """
    if rules is None or len(rules) == 0:
        print("Não há regras de associação para gerar relatório.")
        return
    
    relatorio = []
    relatorio.append("# Relatório de Regras de Associação - MegaSuper Vendas\n")
    
    # Estatísticas gerais
    relatorio.append("## 1. Estatísticas Gerais")
    relatorio.append(f"- Total de regras encontradas: {len(rules)}")
    relatorio.append(f"- Lift médio: {rules['lift'].mean():.4f}")
    relatorio.append(f"- Confiança média: {rules['confidence'].mean():.4f}\n")
    
    # Top regras por lift
    relatorio.append("## 2. Top 10 Regras por Lift")
    for i, row in rules.sort_values("lift", ascending=False).head(10).iterrows():
        antecedentes = ', '.join(list(row['antecedents']))
        consequentes = ', '.join(list(row['consequents']))
        relatorio.append(f"### Regra {i+1}: {antecedentes} → {consequentes}")
        relatorio.append(f"- Suporte: {row['support']:.4f}")
        relatorio.append(f"- Confiança: {row['confidence']:.4f}")
        relatorio.append(f"- Lift: {row['lift']:.4f}")
        relatorio.append("")
    
    # Top regras por confiança
    relatorio.append("## 3. Top 10 Regras por Confiança")
    for i, row in rules.sort_values("confidence", ascending=False).head(10).iterrows():
        antecedentes = ', '.join(list(row['antecedents']))
        consequentes = ', '.join(list(row['consequents']))
        relatorio.append(f"### Regra {i+1}: {antecedentes} → {consequentes}")
        relatorio.append(f"- Suporte: {row['support']:.4f}")
        relatorio.append(f"- Confiança: {row['confidence']:.4f}")
        relatorio.append(f"- Lift: {row['lift']:.4f}")
        relatorio.append("")
    
    # Insights e recomendações
    relatorio.append("## 4. Insights e Recomendações de Marketing")
    relatorio.append("Com base nas regras de associação encontradas, recomendamos:")
    relatorio.append("- **Disposição de produtos**: Colocar produtos frequentemente comprados juntos em locais próximos na loja.")
    relatorio.append("- **Promoções combinadas**: Criar ofertas do tipo 'leve X e Y com desconto'.")
    relatorio.append("- **Recomendações personalizadas**: Implementar sistema de recomendação baseado no histórico de compras.")
    relatorio.append("- **Pacotes de produtos**: Criar pacotes combinando itens com forte associação.")
    
    # Salvar o relatório
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(relatorio))
    
    print(f"Relatório de associação gerado com sucesso! Arquivo salvo como: {file_path}")

# 1. Carregamento dos Dados
print("\n=== 1. Carregamento e Inspeção Inicial dos Dados ===")
# Carrega o arquivo CSV para um DataFrame do Pandas e exibe informações sobre
# tipos de dados, contagem de valores não nulos, e uso de memória
df = carregar_dados("dadosSujos/vendas_modificado (2).csv")
print("\nInformações do DataFrame:")
print(df.info())

# 2. Funções de Limpeza e Validação
print("\n=== 2. Funções de Limpeza e Validação ===")
# Nesta etapa, todas as funções de limpeza e validação foram definidas anteriormente
# incluindo padronização de produtos, validação de valores monetários, etc.

# 3. Aplicação das Funções de Limpeza
print("\n=== 3. Aplicação das Funções de Limpeza ===")
# Aplicação de funções de limpeza e padronização nos campos de texto
# e validação de campos numéricos para garantir consistência dos dados
df['cliente'] = df['cliente'].apply(limpar_texto)  # Remove espaços extra e converte para minúsculas
df['produto'] = df['produto'].apply(padronizar_produto)  # Padroniza nomes de produtos
df['data'] = df['data'].apply(padronizar_data)  # Converte para formato YYYY-MM-DD
df['hora'] = df['hora'].apply(padronizar_hora)  # Converte para formato HH:MM:SS
df = validar_valores_numericos(df)  # Trata todos os campos numéricos
df['valor'] = df['valor'].apply(validar_valor)  # Valida valores monetários entre 0 e 10.000
df['quantidade'] = df['quantidade'].apply(validar_quantidade)  # Valida quantidades entre 1 e 100
df['frete'] = df['frete'].apply(validar_frete)  # Valida fretes entre 0 e 1.000

# 3.1. Tratamento de CEPs
print("\n=== 3.1. Tratamento de CEPs ===")
# Preenche CEPs ausentes usando uma hierarquia de estratégias:
# 1. CEP mais comum da cidade
# 2. CEP mais comum do estado
# 3. CEP mais comum geral
# 4. CEP sintético baseado no estado
# Em seguida, formata todos os CEPs para o padrão XXXXX-XXX
df = tratar_ceps_ausentes(df)
df['cep'] = df['cep'].apply(validar_cep)

# 4. Tratamento de Duplicatas
print("\n=== 4. Tratamento de Duplicatas ===")
# Identifica e remove registros duplicados com base em colunas-chave:
# id_da_compra, data, hora, cliente e produto
# Mantém o primeiro registro quando encontra duplicatas
df = tratar_duplicatas(df)

# 5. Tratamento de Valores Ausentes
print("\n=== 5. Tratamento de Valores Ausentes ===")
# Trata valores ausentes usando estratégias específicas para cada coluna:
# - valor: preenche com a média
# - quantidade: preenche com 1
# - frete: preenche com 0
# - vendedor/marca: preenche com "Não Especificado"
# - total: recalcula baseado em valor * quantidade + frete
df = tratar_valores_ausentes(df)

# 6. Verificação de Cálculos
print("\n=== 6. Verificação de Cálculos ===")
# Verifica se a coluna 'total' está correta de acordo com a fórmula:
# total = valor * quantidade + frete
# Corrige valores que diferem do cálculo em mais de 0.01
df = verificar_calculos(df)

# 7. Análise de Padrões de Compra
print("\n=== 7. Análise de Padrões de Compra ===")
# Analisa os produtos mais vendidos após a padronização
# para identificar padrões de compra nos dados limpos
print("\nTop 10 produtos mais vendidos:")
print(df['produto'].value_counts().head(10))

# 7.1. Validação da Padronização de Produtos
print("\n=== 7.1. Validação da Padronização de Produtos ===")
# Verifica a eficácia do processo de padronização de produtos
# Identifica possíveis produtos similares que poderiam ser padronizados
# e produtos com poucas ocorrências que podem representar anomalias
df = validar_padronizacao_produtos(df)

# 7.2. Verificação final de CEPs nulos
print("\n=== 7.2 Verificação final de CEPs nulos ===")
# Verifica se ainda há CEPs nulos após todos os tratamentos
# e aplica uma estratégia final (preenchimento com '00000-000')
# para garantir completude dos dados
ceps_nulos = df['cep'].isnull().sum()
if ceps_nulos > 0:
    print(f"Ainda existem {ceps_nulos} CEPs nulos. Aplicando tratamento final...")
    # Aplicar uma estratégia mais agressiva para garantir que não haja nulos
    df['cep'] = df['cep'].fillna('00000-000')

# 8. Geração do Relatório
print("\n=== 8. Geração do Relatório de Limpeza ===")
# Gera um relatório detalhado em formato markdown com estatísticas sobre:
# - Total de registros
# - Registros duplicados removidos
# - Valores ausentes por coluna
# - Tipos de dados por coluna
# - Problemas corrigidos
# - Top 5 produtos mais vendidos
relatorio = gerar_relatorio(df, df)
with open("relatorios/relatorio_limpeza.md", "w", encoding="utf-8") as f:
    f.write(relatorio)
print("\nRelatório de limpeza gerado com sucesso!")
print("Arquivo salvo como: relatorios/relatorio_limpeza.md")

# 9. Salvando Dados Limpos
print("\n=== 9. Salvando Dados Limpos ===")
# Salva o DataFrame limpo e processado em um arquivo CSV
# para uso posterior em análises ou sistemas
df.to_csv("dadosLimpos/dados_limpos.csv", index=False)
print("Dados limpos salvos com sucesso!")
print("Arquivo salvo como: dadosLimpos/dados_limpos.csv")

# 10. Análise de Regras de Associação
print("\n=== 10. Análise de Regras de Associação ===")
# Aplica o algoritmo Apriori para encontrar padrões de compra
# e identifica regras de associação entre produtos
_, rules = analisar_regras_associacao(df, min_support=0.01, min_confidence=0.3)
# Salvar as regras em um arquivo CSV
rules.to_csv("dadosLimpos/regras_associacao.csv", index=False)
print("Regras de associação salvas em: dadosLimpos/regras_associacao.csv")

# 11. Geração de Relatório de Associação
print("\n=== 11. Geração de Relatório de Associação ===")
# Cria um relatório detalhado com as regras de associação encontradas
# incluindo métricas de avaliação e recomendações de marketing
gerar_relatorio_associacao(rules, "relatorios/relatorio_associacao.md")

print("\nProcesso de análise de dados concluído com sucesso!")