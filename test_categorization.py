#!/usr/bin/env python3
"""
Script de teste para verificar a categorização baseada em tipo de transação.
"""

from services.smart_keyword_categorizer import SmartKeywordCategorizer
from services.logger import StructuredLogger

def test_categorization_by_type():
    """Testa a categorização baseada no tipo de transação."""
    
    logger = StructuredLogger()
    categorizer = SmartKeywordCategorizer(logger)
    
    print("=== TESTE DE CATEGORIZAÇÃO POR TIPO DE TRANSAÇÃO ===\n")
    
    # Testes para despesas (valores negativos)
    expense_tests = [
        ("PIX QRS IFOOD COM A18/06", -45.90, "Alimentação"),
        ("PAY UBER 14/06", -25.50, "Transporte"),
        ("DA DROGASIL 19/06", -15.80, "Saúde"),
        ("DA SABESP 00000118677", -120.00, "Moradia"),
        ("PAY SHOPPING 22/06", -200.00, "Vestuário"),
        ("PAY CINEMA 20/06", -35.00, "Lazer"),
        ("PAY ADVOGADO 25/06", -800.00, "Serviços"),
        ("PAY ESCOLA 28/06", -500.00, "Educação"),
        ("PAY AMAZON 30/06", -150.00, "Compras Variadas"),
        ("PAY MERCADO LIVRE 01/07", -75.00, "Compras Variadas"),
    ]
    
    # Testes para receitas (valores positivos)
    income_tests = [
        ("SALARIO RECEBIDO 05/07", 5000.00, "Salário"),
        ("13O SALARIO 15/12", 5000.00, "Salário"),
        ("FERIAS + 1/3 20/01", 3500.00, "Salário"),
        ("VALE REFEICAO 10/07", 500.00, "Salário"),
        ("REND PAGO APLIC AUT MAIS", 150.00, "Investimentos"),
        ("DIVIDENDO ACOES 25/07", 200.00, "Investimentos"),
        ("PIX RECEBIDO 30/07", 1000.00, "Transferências"),
        ("TED RECEBIDO 05/08", 2000.00, "Transferências"),
    ]
    
    # Testes para valores zero (deve considerar ambos os tipos)
    zero_tests = [
        ("PIX TRANSF 15/08", 0.00, "Transferências"),
        ("AJUSTE SALDO 20/08", 0.00, "Outros"),
    ]
    
    print("=== TESTES DE DESPESAS (valores negativos) ===")
    correct_expense = 0
    total_expense = len(expense_tests)
    
    for description, amount, expected in expense_tests:
        result = categorizer.categorize_transaction(description, amount)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (esperado: {expected})")
        if result == expected:
            correct_expense += 1
    
    print(f"\nDespesas: {correct_expense}/{total_expense} corretas ({correct_expense/total_expense*100:.1f}%)")
    
    print("\n=== TESTES DE RECEITAS (valores positivos) ===")
    correct_income = 0
    total_income = len(income_tests)
    
    for description, amount, expected in income_tests:
        result = categorizer.categorize_transaction(description, amount)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (esperado: {expected})")
        if result == expected:
            correct_income += 1
    
    print(f"\nReceitas: {correct_income}/{total_income} corretas ({correct_income/total_income*100:.1f}%)")
    
    print("\n=== TESTES DE VALORES ZERO ===")
    correct_zero = 0
    total_zero = len(zero_tests)
    
    for description, amount, expected in zero_tests:
        result = categorizer.categorize_transaction(description, amount)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (esperado: {expected})")
        if result == expected:
            correct_zero += 1
    
    print(f"\nValores zero: {correct_zero}/{total_zero} corretos ({correct_zero/total_zero*100:.1f}%)")
    
    # Testes específicos para verificar se categorias de despesa não são aplicadas a receitas
    print("\n=== TESTES DE CONFLITO DESPESA/RECEITA ===")
    
    conflict_tests = [
        ("PIX QRS IFOOD COM A18/06", 45.90, "Alimentação"),  # Receita com palavra-chave de despesa
        ("SALARIO RECEBIDO 05/07", -5000.00, "Salário"),      # Despesa com palavra-chave de receita
    ]
    
    for description, amount, expected in conflict_tests:
        result = categorizer.categorize_transaction(description, amount)
        # Para estes testes, esperamos que NÃO seja a categoria esperada devido ao tipo
        status = "✅" if result != expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (NÃO deveria ser: {expected})")
    
    # Estatísticas finais
    total_correct = correct_expense + correct_income + correct_zero
    total_tests = total_expense + total_income + total_zero
    
    print(f"\n=== RESULTADO FINAL ===")
    print(f"Total de testes: {total_tests}")
    print(f"Acertos: {total_correct}")
    print(f"Taxa de acerto: {total_correct/total_tests*100:.1f}%")
    
    if total_correct/total_tests >= 0.8:
        print("🎉 Sistema de categorização por tipo funcionando corretamente!")
    else:
        print("⚠️  Sistema precisa de ajustes.")

if __name__ == "__main__":
    test_categorization_by_type() 