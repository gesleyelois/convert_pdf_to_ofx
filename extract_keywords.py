#!/usr/bin/env python3
"""
Script para extrair palavras-chave das categorias sugeridas do CSV e atualizar keywords.json.
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

def extract_keywords():
    """Extrai palavras-chave das categorias sugeridas."""
    
    input_file = Path("csv_reports/transacoes_outros_sugeridas.csv")
    
    if not input_file.exists():
        print("❌ Arquivo transacoes_outros_sugeridas.csv não encontrado!")
        print("💡 Execute primeiro: python suggest_categories.py")
        return {}
    
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

def extract_keywords_from_descriptions(descriptions):
    """Extrai palavras-chave únicas das descrições."""
    keywords = set()
    
    for description in descriptions:
        # Remove caracteres especiais e normaliza
        clean_desc = re.sub(r'[^\w\s]', ' ', description.lower())
        words = clean_desc.split()
        
        # Filtra palavras muito curtas ou muito longas
        for word in words:
            if 3 <= len(word) <= 20 and word not in ['por', 'com', 'para', 'para', 'com', 'sem', 'sob', 'sobre']:
                keywords.add(word)
        
        # Adiciona frases específicas
        if 'uber' in description.lower():
            keywords.add('uber')
        if 'pix' in description.lower():
            keywords.add('pix')
        if 'dev pix' in description.lower():
            keywords.add('dev pix')
        if 'liberação' in description.lower():
            keywords.add('liberação de dinheiro')
        if 'reserva' in description.lower():
            keywords.add('reserva')
    
    return sorted(list(keywords))

def update_keywords_json():
    """Atualiza o arquivo keywords.json com novas palavras-chave."""
    
    category_descriptions = extract_keywords()
    
    if not category_descriptions:
        print("❌ Nenhuma categoria encontrada para atualizar!")
        return
    
    # Carrega o arquivo JSON atual
    json_file = Path("keywords.json")
    
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            current_keywords = json.load(f)
    else:
        current_keywords = {}
    
    print("🔄 ATUALIZANDO KEYWORDS.JSON...\n")
    
    # Atualiza com novas palavras-chave
    for category, descriptions in category_descriptions.items():
        new_keywords = extract_keywords_from_descriptions(descriptions)
        
        if category not in current_keywords:
            current_keywords[category] = []
        
        # Adiciona novas palavras-chave sem duplicatas
        existing_keywords = set(current_keywords[category])
        for keyword in new_keywords:
            if keyword not in existing_keywords:
                current_keywords[category].append(keyword)
                print(f"✅ Adicionado '{keyword}' à categoria '{category}'")
    
    # Salva o arquivo atualizado
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(current_keywords, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Arquivo keywords.json atualizado com sucesso!")
    print(f"📁 Total de categorias: {len(current_keywords)}")
    
    # Mostra estatísticas
    total_keywords = sum(len(keywords) for keywords in current_keywords.values())
    print(f"📊 Total de palavras-chave: {total_keywords}")
    
    return current_keywords

def show_keywords_summary():
    """Mostra um resumo das palavras-chave atuais."""
    
    json_file = Path("keywords.json")
    
    if not json_file.exists():
        print("❌ Arquivo keywords.json não encontrado!")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        keywords = json.load(f)
    
    print("📊 RESUMO DAS PALAVRAS-CHAVE ATUAIS:\n")
    
    for category, words in keywords.items():
        print(f"📂 {category}: {len(words)} palavras-chave")
        if len(words) <= 10:
            for word in words:
                print(f"  - {word}")
        else:
            print(f"  - Primeiras 5: {', '.join(words[:5])}")
            print(f"  - ... e mais {len(words) - 5} palavras-chave")
        print()

if __name__ == "__main__":
    print("🔧 EXTRATOR DE PALAVRAS-CHAVE")
    print("=" * 40)
    
    # Atualiza o arquivo JSON
    updated_keywords = update_keywords_json()
    
    if updated_keywords:
        print("\n" + "=" * 40)
        show_keywords_summary() 