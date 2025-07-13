#!/usr/bin/env python3
"""
Script de teste para verificar a categorização.
"""

from services.logger import StructuredLogger
from services.smart_keyword_categorizer import SmartKeywordCategorizer
from keyword_config import CATEGORY_KEYWORDS
import re

def test_categorization():
    """Testa a categorização de transações específicas."""
    
    # Inicializa o logger
    logger = StructuredLogger()
    
    # Inicializa o categorizador
    categorizer = SmartKeywordCategorizer(logger)
    
    # Testa transações de reserva
    test_transactions = [
        ("Reserva por gastos Férias", -5.0),
        ("Reserva por vendas Férias", -0.86),
        ("Dinheiro reservado", -5.0),
        ("Reserva por gastos", -5.0),
        ("Reserva por vendas", -1.82),
    ]
    
    print("🔍 TESTE DE CATEGORIZAÇÃO")
    print("=" * 50)
    
    for description, amount in test_transactions:
        category = categorizer.categorize_transaction(description, amount)
        print(f"Descrição: {description}")
        print(f"Valor: R$ {amount}")
        print(f"Categoria: {category}")
        print("-" * 30)
    
    # Mostra as palavras-chave da categoria Reservas
    print("\n📋 PALAVRAS-CHAVE DA CATEGORIA 'RESERVAS':")
    if "Reservas" in CATEGORY_KEYWORDS:
        for keyword in CATEGORY_KEYWORDS["Reservas"]:
            print(f"  - {keyword}")
    else:
        print("  ❌ Categoria 'Reservas' não encontrada!")

def test_ofx_processing():
    """Testa o processamento de OFX específico."""
    
    # Inicializa o logger
    logger = StructuredLogger()
    
    # Inicializa o categorizador
    categorizer = SmartKeywordCategorizer(logger)
    
    # Simula o processamento de uma transação OFX
    ofx_memo = "Reserva por gastos Férias"
    amount = -5.0
    
    print("\n🔍 TESTE DE PROCESSAMENTO OFX")
    print("=" * 50)
    print(f"Descrição OFX: {ofx_memo}")
    print(f"Valor: R$ {amount}")
    
    # Categoriza
    category = categorizer.categorize_transaction(ofx_memo, amount)
    print(f"Categoria: {category}")
    
    # Testa limpeza de texto
    cleaned = categorizer._clean_description(ofx_memo)
    print(f"Texto limpo: '{cleaned}'")
    
    # Testa correspondência
    for keyword in CATEGORY_KEYWORDS.get("Reservas", []):
        if keyword.lower() in cleaned:
            print(f"✅ Correspondência encontrada: '{keyword}'")
        else:
            print(f"❌ Sem correspondência: '{keyword}'")

if __name__ == "__main__":
    test_categorization()
    test_ofx_processing() 