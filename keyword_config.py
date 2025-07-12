"""
Configuração de palavras-chave para categorização inteligente.
Permite personalizar facilmente as regras de categorização.
"""

# Configuração de categorias e palavras-chave
CATEGORY_KEYWORDS = {
    "Alimentação": [
        # Delivery e fast food
        "ifood", "rappi", "uber eats", "99 food", "mcdonalds", "burger king", 
        "subway", "starbucks", "dominos", "pizza hut", "habibs", "bobs",
        "pix qrs ifood", "ifood com", "ifood com a",
        
        # Restaurantes e lanchonetes
        "padaria", "restaurante", "lanchonete", "pizzaria", "bakery", "cafe", 
        "coffee", "restaurant", "food", "comida", "lanche", "pão", "pizza", 
        "hamburger", "sandwich", "sorvete", "doceria", "pastelaria",
        
        # Supermercados e mercados
        "supermercado", "super", "extra", "carrefour", "pão de açúcar", "assai", 
        "atacadão", "big", "walmart", "sam's club", "makro", "sacolão", 
        "hortifruti", "natural da terra", "emporio", "mercearia", "mini mercado",
        
        # Específicos brasileiros
        "casa do pão", "padaria são paulo", "padaria real", "padaria do seu joão",
        "restaurante japonês", "restaurante italiano", "restaurante árabe",
        "lanchonete do zé", "pizzaria do tio", "doceria da maria"
    ],
    
    "Transporte": [
        # Apps de transporte
        "uber", "99", "cabify", "taxi", "uberx", "uber black", "uber comfort",
        "99 taxi", "99 premium", "99 rides", "uber rides", "uber parking",
        "99 parking",
        
        # Transporte público
        "metrô", "ônibus", "passagem", "bilhete único", "vem", "metro",
        
        # Combustível e postos
        "combustível", "gasolina", "etanol", "diesel", "posto", "shell",
        "petrobras", "ipiranga", "texaco", "petrobrás", "br", "petrobras",
        
        # Estacionamento e pedágio
        "estacionamento", "parking", "pedágio", "sem parar", "veloe", "conectcar",
        "uber parking", "99 parking",
        
        # Específicos brasileiros
        "uber eats", "99 food", "uber eats", "99 food"
    ],
    
    "Saúde": [
        # Farmácias e drogarias
        "farmácia", "drogaria", "drogasil", "raia", "panvel", "pacheco",
        "drograria", "drogaria são paulo", "drogaria araujo", "drogaria pacheco",
        "farmácia popular", "farmácia do povo", "drogaria do centro",
        
        # Planos de saúde
        "unimed", "amil", "sulamerica", "bradesco saúde", "porto seguro saúde",
        "hapvida", "notredame", "golden cross", "blue cross", "allianz",
        
        # Serviços médicos
        "hospital", "clínica", "médico", "dentista", "fisioterapeuta", 
        "psicólogo", "psiquiatra", "laboratório", "exame", "consulta", 
        "medicamento", "remédio", "consulta médica", "exame laboratorial",
        
        # Específicos brasileiros
        "farmácia popular", "drogaria são paulo", "drogaria araujo"
    ],
    
    "Moradia": [
        # Contas básicas
        "aluguel", "condomínio", "iptu", "energia", "luz", "eletropaulo",
        "enel", "copel", "cemig", "energisa", "água", "sabesp", "sanepar",
        "copasa", "esgoto", "gás", "comgás", "gás natural",
        
        # Internet e TV
        "internet", "net", "claro", "oi", "vivo", "tim", "sky", "directv",
        "netflix", "spotify", "youtube premium", "amazon prime", "disney+",
        "hbo max", "paramount+", "globoplay", "pluto tv", "crunchyroll",
        
        # Específicos brasileiros
        "eletropaulo", "sabesp", "comgás", "net", "claro", "oi", "vivo"
    ],
    
    "Educação": [
        # Instituições de ensino
        "escola", "colégio", "universidade", "faculdade", "curso", "treinamento",
        "cursinho", "vestibular", "enem", "material escolar", "livro didático",
        "biblioteca", "escola de inglês", "cultura inglesa", "wizard", "ccaa",
        "yazigi", "fisk", "senac", "senai", "escola técnica", "pós-graduação",
        "mestrado", "doutorado", "bolsa de estudos", "fies", "prouni",
        
        # Específicos brasileiros
        "cultura inglesa", "wizard", "ccaa", "yazigi", "fisk", "senac", "senai"
    ],
    
    "Lazer": [
        # Entretenimento
        "cinema", "teatro", "show", "concerto", "festival", "museu", "zoo",
        "parque", "aquário", "shopping", "mall", "loja", "store", "shop",
        
        # Esportes e fitness
        "academia", "fitness", "crossfit", "pilates", "yoga", "natação",
        "futebol", "basquete", "tênis", "golfe", "esporte", "sport",
        "smart fit", "fitness one", "academia smart", "academia do seu joão",
        
        # Viagens
        "viagem", "hotel", "airbnb", "booking", "decolar", "hoteis.com",
        "passagem aérea", "passagem rodoviária", "aluguel de carro",
        
        # Específicos brasileiros
        "smart fit", "fitness one", "academia smart", "academia do seu joão"
    ],
    
    "Vestuário": [
        # Roupas e calçados
        "roupa", "camisa", "calça", "vestido", "sapato", "tênis", "bolsa",
        "mochila", "carteira", "relógio", "joia", "bijuteria", "perfume",
        
        # Higiene pessoal
        "cosmético", "maquiagem", "shampoo", "condicionador", "sabonete",
        "creme", "protetor solar", "desodorante", "escova de dente",
        "pasta de dente", "fio dental", "escova de cabelo", "pente",
        
        # Lojas específicas
        "renner", "c&a", "marisa", "riachuelo", "lojas americanas", "magazine luiza",
        "nike", "adidas", "puma", "reebok", "converse", "vans", "timberland",
        
        # Palavras-chave específicas
        "pay shopping", "shopping", "loja de roupas", "loja de calçados", "pay shopping"
    ],
    
    "Serviços": [
        # Serviços pessoais
        "manicure", "pedicure", "cabeleireiro", "barbeiro", "salão de beleza",
        "spa", "massagem", "fisioterapia", "psicologia", "psiquiatria",
        
        # Serviços profissionais
        "advogado", "contador", "consultoria", "assessoria", "seguro",
        "previdência", "investimento", "corretora", "banco", "financiamento",
        "empréstimo", "cartão de crédito", "boleto", "pix", "transferência",
        
        # Específicos brasileiros
        "salão de beleza", "cabeleireiro", "barbeiro", "manicure", "pedicure"
    ],
    
    "Investimentos": [
        # Tipos de investimento
        "rendimento", "dividendo", "juros", "aplicação", "resgate", "cdb",
        "lci", "lca", "tesouro direto", "ações", "fii", "criptomoeda",
        "bitcoin", "ethereum", "binance", "coinbase", "mercado bitcoin",
        "rend pag", "aplic aut", "aplicação automática", "rendimento pago",
        
        # Instituições financeiras
        "nubank", "inter", "xp", "rico", "clear", "easynvest", "modalmais",
        "btg pactual", "itau", "bradesco", "santander", "caixa", "banco do brasil",
        
        # Específicos brasileiros
        "tesouro direto", "cdb", "lci", "lca", "fii", "criptomoeda"
    ],
    
    "Transferências": [
        # PIX e transferências (apenas correspondências exatas)
        "pix transf", "pix receb", "pix enviado", "transferência", "ted",
        "doc", "pix qr", "pix pago", "pix recebido", "pix enviado",
        "transferência bancária", "ted doc", "pix transferência"
    ]
}

# Configuração de prioridades (quanto maior, maior a prioridade)
CATEGORY_PRIORITIES = {
    "Alimentação": 10,
    "Transporte": 10,
    "Saúde": 9,
    "Moradia": 9,
    "Educação": 8,
    "Vestuário": 8,  # Aumentada para ter prioridade sobre Lazer
    "Lazer": 7,
    "Serviços": 5,
    "Investimentos": 5,
    "Transferências": 1,  # Baixa prioridade para não conflitar
    "Outros": 0
}

# Regras contextuais baseadas em valores
VALUE_BASED_RULES = {
    "high_value_threshold": 1000,  # Valores acima de R$ 1000
    "low_value_threshold": 50,      # Valores abaixo de R$ 50
    "investment_threshold": 5000,   # Valores acima de R$ 5000 são investimentos
}

# Palavras-chave que indicam transferências (correspondência exata)
TRANSFER_KEYWORDS = [
    "pix transf", "pix receb", "pix enviado", "transferência", "ted",
    "doc", "pix qr", "pix pago", "pix recebido", "pix enviado"
]

# Configuração de limpeza de texto
TEXT_CLEANING = {
    "remove_special_chars": True,
    "normalize_spaces": True,
    "convert_to_lowercase": True,
    "remove_numbers": False,  # Mantém números pois podem ser importantes
}

# Configuração de score mínimo para categorização
MIN_SCORE_THRESHOLD = 0.3

# Configuração de eficácia desejada
EFFICIENCY_TARGETS = {
    "excellent": 30,  # Menos de 30% em "Outros" = Excelente
    "good": 50,       # Menos de 50% em "Outros" = Bom
    "needs_improvement": 50  # Acima de 50% em "Outros" = Precisa melhorar
} 