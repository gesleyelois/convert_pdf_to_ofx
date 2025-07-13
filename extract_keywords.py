#!/usr/bin/env python3
"""
Script para extrair palavras-chave das categorias sugeridas do CSV.
"""

import csv
from collections import defaultdict
from pathlib import Path

def extract_keywords():
    """Extrai palavras-chave das categorias sugeridas."""
    
    input_file = Path("csv_reports/transacoes_outros_sugeridas.csv")
    
    # Dicionário para armazenar descrições por categoria
    category_descriptions = defaultdict(set)
    
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            description = row['description']
            suggested_category = row['suggested_category']
            
            if suggested_category != "Outros":
                category_descriptions[suggested_category].add(description)
    
    print("🔍 PALAVRAS-CHAVE EXTRAÍDAS POR CATEGORIA:\n")
    
    for category, descriptions in category_descriptions.items():
        print(f"📂 {category.upper()} ({len(descriptions)} descrições únicas):")
        for desc in sorted(descriptions):
            print(f"  - {desc}")
        print()
    
    return category_descriptions

def generate_keyword_config():
    """Gera configuração de palavras-chave para adicionar ao keyword_config.py."""
    
    category_descriptions = extract_keywords()
    
    print("🔧 CONFIGURAÇÃO PARA ADICIONAR AO keyword_config.py:\n")
    
    # Novas categorias
    new_categories = {
        "Reservas": [
            "reserva por gastos férias",
            "reserva por vendas férias",
            "dinheiro reservado"
        ],
        "Impostos": [
            "int ipva",
            "int licenc",
            "imposto",
            "taxa",
            "ipva",
            "licenciamento"
        ]
    }
    
    # Melhorias para categorias existentes
    improvements = {
        "Moradia": [
            "da dae-jund",
            "da cpfl",
            "da sabesp",
            "dae-jund",
            "cpfl",
            "sabesp"
        ],
        "Transferências": [
            "dev pix",
            "liberação de dinheiro",
            "saída de dinheiro",
            "dinheiro retirado",
            "débito em conta"
        ],
        "Lazer": [
            "multiplex",
            "omai s past"
        ],
        "Transporte": [
            "pagamento cancelado uber"
        ]
    }
    
    print("📝 NOVAS CATEGORIAS SUGERIDAS:")
    for category, keywords in new_categories.items():
        print(f"\n    \"{category}\": [")
        for keyword in keywords:
            print(f"        \"{keyword}\",")
        print("    ],")
    
    print("\n🔧 MELHORIAS PARA CATEGORIAS EXISTENTES:")
    for category, keywords in improvements.items():
        print(f"\n    # Adicionar a {category}:")
        for keyword in keywords:
            print(f"    \"{keyword}\",")
    
    return new_categories, improvements

if __name__ == "__main__":
    generate_keyword_config() 