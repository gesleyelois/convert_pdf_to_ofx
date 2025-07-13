#!/usr/bin/env python3
"""
Teste específico para as novas categorias adicionadas baseadas no CSV.
"""

from services.smart_keyword_categorizer import SmartKeywordCategorizer
from services.logger import StructuredLogger

def test_new_categories():
    """Testa as novas categorias adicionadas."""
    
    logger = StructuredLogger()
    categorizer = SmartKeywordCategorizer(logger)
    
    print("=== TESTE DAS NOVAS CATEGORIAS ===\n")
    
    # Testes para a nova categoria "Reservas"
    reservas_tests = [
        ("Reserva por gastos Férias", -5.0, "Reservas"),
        ("Reserva por vendas Férias", -3.86, "Reservas"),
        ("Dinheiro reservado", -10.0, "Reservas"),
    ]
    
    # Testes para a nova categoria "Impostos"
    impostos_tests = [
        ("INT IPVA-SP FGQ-1370", -261.32, "Impostos"),
        ("INT LICENC SP 98409066", -164.46, "Impostos"),
        ("IPVA 2025", -500.0, "Impostos"),
        ("Licenciamento 2025", -200.0, "Impostos"),
    ]
    
    # Testes para melhorias em categorias existentes
    moradia_tests = [
        ("DA DAE-JUND 00000118677", -168.23, "Moradia"),
        ("DA CPFL PIR 10040315436", -203.16, "Moradia"),
        ("DA SABESP 00000118677", -120.0, "Moradia"),
    ]
    
    transferencias_tests = [
        ("DEV PIX VELOX TICKE08/01", 42.0, "Transferências"),
        ("Liberação de dinheiro", 86.99, "Transferências"),
        ("Saída de dinheiro", -5.0, "Transferências"),
    ]
    
    lazer_tests = [
        ("RSCSS-MULTIPLEX I-08/01", -97.5, "Lazer"),
        ("OMAI S PAST", -50.0, "Lazer"),
    ]
    
    transporte_tests = [
        ("Pagamento cancelado Uber * pending", 29.75, "Transporte"),
        ("DEV PIX UBER26/03", 15.0, "Transporte"),
    ]
    
    alimentacao_tests = [
        ("AGENCIA DE RESTAURANTES ONLINE", -30.0, "Alimentação"),
    ]
    
    print("=== TESTES DA NOVA CATEGORIA 'RESERVAS' ===")
    correct_reservas = 0
    total_reservas = len(reservas_tests)
    
    for description, amount, expected in reservas_tests:
        result = categorizer.categorize_transaction(description, amount)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (esperado: {expected})")
        if result == expected:
            correct_reservas += 1
    
    print(f"\nReservas: {correct_reservas}/{total_reservas} corretas ({correct_reservas/total_reservas*100:.1f}%)")
    
    print("\n=== TESTES DA NOVA CATEGORIA 'IMPOSTOS' ===")
    correct_impostos = 0
    total_impostos = len(impostos_tests)
    
    for description, amount, expected in impostos_tests:
        result = categorizer.categorize_transaction(description, amount)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (esperado: {expected})")
        if result == expected:
            correct_impostos += 1
    
    print(f"\nImpostos: {correct_impostos}/{total_impostos} corretos ({correct_impostos/total_impostos*100:.1f}%)")
    
    print("\n=== TESTES DE MELHORIAS EM 'MORADIA' ===")
    correct_moradia = 0
    total_moradia = len(moradia_tests)
    
    for description, amount, expected in moradia_tests:
        result = categorizer.categorize_transaction(description, amount)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (esperado: {expected})")
        if result == expected:
            correct_moradia += 1
    
    print(f"\nMoradia: {correct_moradia}/{total_moradia} corretas ({correct_moradia/total_moradia*100:.1f}%)")
    
    print("\n=== TESTES DE MELHORIAS EM 'TRANSFERÊNCIAS' ===")
    correct_transferencias = 0
    total_transferencias = len(transferencias_tests)
    
    for description, amount, expected in transferencias_tests:
        result = categorizer.categorize_transaction(description, amount)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (esperado: {expected})")
        if result == expected:
            correct_transferencias += 1
    
    print(f"\nTransferências: {correct_transferencias}/{total_transferencias} corretas ({correct_transferencias/total_transferencias*100:.1f}%)")
    
    print("\n=== TESTES DE MELHORIAS EM 'LAZER' ===")
    correct_lazer = 0
    total_lazer = len(lazer_tests)
    
    for description, amount, expected in lazer_tests:
        result = categorizer.categorize_transaction(description, amount)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (esperado: {expected})")
        if result == expected:
            correct_lazer += 1
    
    print(f"\nLazer: {correct_lazer}/{total_lazer} corretos ({correct_lazer/total_lazer*100:.1f}%)")
    
    print("\n=== TESTES DE MELHORIAS EM 'TRANSPORTE' ===")
    correct_transporte = 0
    total_transporte = len(transporte_tests)
    
    for description, amount, expected in transporte_tests:
        result = categorizer.categorize_transaction(description, amount)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (esperado: {expected})")
        if result == expected:
            correct_transporte += 1
    
    print(f"\nTransporte: {correct_transporte}/{total_transporte} corretos ({correct_transporte/total_transporte*100:.1f}%)")
    
    print("\n=== TESTES DE MELHORIAS EM 'ALIMENTAÇÃO' ===")
    correct_alimentacao = 0
    total_alimentacao = len(alimentacao_tests)
    
    for description, amount, expected in alimentacao_tests:
        result = categorizer.categorize_transaction(description, amount)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description} (R$ {amount:.2f}) -> {result} (esperado: {expected})")
        if result == expected:
            correct_alimentacao += 1
    
    print(f"\nAlimentação: {correct_alimentacao}/{total_alimentacao} corretas ({correct_alimentacao/total_alimentacao*100:.1f}%)")
    
    # Estatísticas finais
    total_correct = correct_reservas + correct_impostos + correct_moradia + correct_transferencias + correct_lazer + correct_transporte + correct_alimentacao
    total_tests = total_reservas + total_impostos + total_moradia + total_transferencias + total_lazer + total_transporte + total_alimentacao
    
    print(f"\n=== RESULTADO FINAL ===")
    print(f"Total de testes: {total_tests}")
    print(f"Acertos: {total_correct}")
    print(f"Taxa de acerto: {total_correct/total_tests*100:.1f}%")
    
    if total_correct/total_tests >= 0.8:
        print("🎉 Novas categorias funcionando corretamente!")
    else:
        print("⚠️  Algumas categorias precisam de ajustes.")

if __name__ == "__main__":
    test_new_categories() 