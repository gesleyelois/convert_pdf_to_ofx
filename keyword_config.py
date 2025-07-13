"""
Configuração de palavras-chave para categorização inteligente.
Permite personalizar facilmente as regras de categorização.
"""

import json
import os
from pathlib import Path

def load_keywords_from_json():
    """Carrega as palavras-chave do arquivo JSON."""
    json_file = Path("keywords.json")
    
    if not json_file.exists():
        # Cria arquivo JSON padrão se não existir
        default_keywords = {
            "Alimentação": [
                "ifood", "rappi", "uber eats", "99 food", "mcdonalds", "burger king", 
                "subway", "starbucks", "dominos", "pizza hut", "habibs", "bobs",
                "pix qrs ifood", "ifood com", "ifood com a",
                "padaria", "restaurante", "lanchonete", "pizzaria", "bakery", "cafe", 
                "coffee", "restaurant", "food", "comida", "lanche", "pão", "pizza", 
                "hamburger", "sandwich", "sorvete", "doceria", "pastelaria",
                "supermercado", "super", "extra", "carrefour", "pão de açúcar", "assai", 
                "atacadão", "big", "walmart", "sam's club", "makro", "sacolão", 
                "hortifruti", "natural da terra", "emporio", "mercearia", "mini mercado"
            ],
            "Transporte": [
                "uber", "99", "cabify", "taxi", "uberx", "uber black", "uber comfort",
                "99 taxi", "99 premium", "99 rides", "uber rides", "uber parking",
                "99 parking", "metrô", "ônibus", "passagem", "bilhete único", "vem", "metro",
                "combustível", "gasolina", "etanol", "diesel", "posto", "shell",
                "petrobras", "ipiranga", "texaco", "petrobrás", "br", "petrobras",
                "estacionamento", "parking", "pedágio", "sem parar", "veloe", "conectcar"
            ],
            "Saúde": [
                "farmácia", "drogaria", "drogasil", "raia", "panvel", "pacheco",
                "drograria", "drogaria são paulo", "drogaria araujo", "drogaria pacheco",
                "farmácia popular", "farmácia do povo", "drogaria do centro",
                "unimed", "amil", "sulamerica", "bradesco saúde", "porto seguro saúde",
                "hapvida", "notredame", "golden cross", "blue cross", "allianz",
                "hospital", "clínica", "médico", "dentista", "fisioterapeuta", 
                "psicólogo", "psiquiatra", "laboratório", "exame", "consulta", 
                "medicamento", "remédio", "consulta médica", "exame laboratorial"
            ],
            "Moradia": [
                "aluguel", "condomínio", "iptu", "energia", "luz", "eletropaulo",
                "enel", "copel", "cemig", "energisa", "água", "sabesp", "sanepar",
                "copasa", "esgoto", "gás", "comgás", "gás natural",
                "internet", "net", "claro", "oi", "vivo", "tim", "sky", "directv",
                "netflix", "spotify", "youtube premium", "amazon prime", "disney+",
                "hbo max", "paramount+", "globoplay", "pluto tv", "crunchyroll"
            ],
            "Educação": [
                "escola", "colégio", "universidade", "faculdade", "curso", "treinamento",
                "cursinho", "vestibular", "enem", "material escolar", "livro didático",
                "biblioteca", "escola de inglês", "cultura inglesa", "wizard", "ccaa",
                "yazigi", "fisk", "senac", "senai", "escola técnica", "pós-graduação",
                "mestrado", "doutorado", "bolsa de estudos", "fies", "prouni"
            ],
            "Lazer": [
                "cinema", "teatro", "show", "concerto", "festival", "museu", "zoo",
                "parque", "aquário", "shopping", "mall", "loja", "store", "shop",
                "academia", "fitness", "crossfit", "pilates", "yoga", "natação",
                "futebol", "basquete", "tênis", "golfe", "esporte", "sport",
                "smart fit", "fitness one", "academia smart", "academia do seu joão",
                "viagem", "hotel", "airbnb", "booking", "decolar", "hoteis.com",
                "passagem aérea", "passagem rodoviária", "aluguel de carro"
            ],
            "Vestuário": [
                "roupa", "camisa", "calça", "vestido", "sapato", "tênis", "bolsa",
                "mochila", "carteira", "relógio", "joia", "bijuteria", "perfume",
                "cosmético", "maquiagem", "shampoo", "condicionador", "sabonete",
                "creme", "protetor solar", "desodorante", "escova de dente",
                "pasta de dente", "fio dental", "escova de cabelo", "pente",
                "renner", "c&a", "marisa", "riachuelo", "lojas americanas", "magazine luiza",
                "nike", "adidas", "puma", "reebok", "converse", "vans", "timberland"
            ],
            "Serviços": [
                "manicure", "pedicure", "cabeleireiro", "barbeiro", "salão de beleza",
                "spa", "massagem", "fisioterapia", "psicologia", "psiquiatria",
                "advogado", "contador", "consultoria", "assessoria", "seguro",
                "previdência", "investimento", "corretora", "banco", "financiamento",
                "empréstimo", "cartão de crédito", "boleto", "pix", "transferência"
            ],
            "Investimentos": [
                "rendimento", "dividendo", "juros", "aplicação", "resgate", "cdb",
                "lci", "lca", "tesouro direto", "ações", "fii", "criptomoeda",
                "bitcoin", "ethereum", "binance", "coinbase", "mercado bitcoin",
                "rend pag", "aplic aut", "aplicação automática", "rendimento pago",
                "nubank", "inter", "xp", "rico", "clear", "easynvest", "modalmais",
                "btg pactual", "itau", "bradesco", "santander", "caixa", "banco do brasil"
            ],
            "Transferências": [
                "pix transf", "pix receb", "pix enviado", "transferência", "ted",
                "doc", "pix qr", "pix pago", "pix recebido", "pix enviado",
                "transferência bancária", "ted doc", "pix transferência",
                "dev pix", "liberação de dinheiro", "saída de dinheiro", "dinheiro retirado",
                "débito em conta", "dev pix velox ticke", "dev pix 99 tecnolog",
                "dev pix uber"
            ],
            "Compras Variadas": [
                "compra", "pagamento", "purchase", "payment", "cobrança", "charge",
                "debito", "credito", "cartão", "card", "pagto", "pag", "pgt",
                "loja", "store", "shop", "mercado", "supermercado", "shopping",
                "centro comercial", "mall", "plaza", "galeria", "feira", "bazar",
                "atacado", "varejo", "varejista", "distribuidor", "fornecedor",
                "empresa", "comercio", "comércio", "estabelecimento", "estabelecimento comercial",
                "amazon", "mercado livre", "americanas", "magazine luiza", "casas bahia",
                "kabum", "terabyte", "pichau", "aliexpress", "shopee", "wish",
                "olx", "enjoei", "b2w", "submarino", "shoptime", "extra", "carrefour",
                "pão de açúcar", "assai", "atacadão", "big", "walmart", "sam's club"
            ],
            "Salário": [
                "salário", "salario", "remuneração", "remuneracao", "ordenado", "vencimento",
                "pagamento salário", "pagamento salario", "pag salário", "pag salario",
                "salário recebido", "salario recebido", "remuneração recebida", "remuneracao recebida",
                "ordenado recebido", "vencimento recebido", "pagamento de salário", "pagamento de salario",
                "13º salário", "13o salario", "décimo terceiro", "decimo terceiro",
                "férias", "ferias", "pagamento de férias", "pagamento de ferias",
                "férias proporcionais", "ferias proporcionais", "férias vencidas", "ferias vencidas",
                "férias + 1/3", "ferias + 1/3", "férias mais um terço", "ferias mais um terco",
                "vale refeição", "vale refeicao", "vale alimentação", "vale alimentacao",
                "vale transporte", "vale combustível", "vale combustivel",
                "comissão", "comissao", "bônus", "bonus", "gratificação", "gratificacao",
                "prêmio", "premio", "incentivo", "participação nos lucros", "participacao nos lucros",
                "plr", "participação", "participacao", "lucros", "lucro"
            ],
            "Reservas": [
                "reserva por gastos férias", "reserva por vendas férias", "dinheiro reservado",
                "reserva por gastos", "reserva por vendas", "reserva por gastos férias",
                "reserva por vendas férias", "reserva por gastos férias", "reserva por vendas férias"
            ],
            "Impostos": [
                "int ipva", "int licenc", "imposto", "taxa", "ipva", "licenciamento",
                "int ipva-sp", "int licenc sp", "ipva-sp", "licenc sp", "impostos",
                "taxas", "imposto ipva", "imposto licenciamento", "taxa ipva", "taxa licenciamento"
            ]
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(default_keywords, f, ensure_ascii=False, indent=2)
        
        return default_keywords
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar keywords.json: {e}")
        return {}

# Carrega as palavras-chave do JSON
CATEGORY_KEYWORDS = load_keywords_from_json()

# Configuração do tipo de transação para cada categoria
# 'expense': apenas para despesas (débitos negativos)
# 'income': apenas para receitas (créditos positivos)  
# 'both': para ambos os tipos
CATEGORY_TYPES = {
    "Alimentação": "expense",
    "Transporte": "expense", 
    "Saúde": "expense",
    "Moradia": "expense",
    "Educação": "expense",
    "Lazer": "expense",
    "Vestuário": "expense",
    "Serviços": "expense",
    "Compras Variadas": "expense",
    "Investimentos": "both",  # Pode ser aplicação (despesa) ou rendimento (receita)
    "Transferências": "both",  # Pode ser envio (despesa) ou recebimento (receita)
    "Salário": "income",
    "Reservas": "expense",  # Reservas automáticas são sempre despesas
    "Impostos": "expense",  # Impostos são sempre despesas
    "Outros": "both"
}

# Configuração de prioridades (quanto maior, maior a prioridade)
CATEGORY_PRIORITIES = {
    "Alimentação": 15,  # Aumentada para ter prioridade sobre Transferências
    "Transporte": 15,   # Aumentada para ter prioridade sobre Transferências
    "Saúde": 14,
    "Moradia": 14,
    "Educação": 13,
    "Vestuário": 13,  # Aumentada para ter prioridade sobre Lazer
    "Lazer": 12,
    "Compras Variadas": 11,  # Prioridade média para compras gerais
    "Serviços": 10,
    "Investimentos": 9,
    "Salário": 8,  # Prioridade baixa para receitas
    "Reservas": 7,  # Prioridade baixa para reservas automáticas
    "Impostos": 8,  # Prioridade média para impostos
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