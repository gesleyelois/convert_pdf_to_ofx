#!/usr/bin/env python3
"""
Script para analisar transações 'Outros' e sugerir categorias baseadas na descrição.
"""

import csv
import re
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter

class CategorySuggester:
    """Classe para sugerir categorias baseadas na descrição das transações."""
    
    def __init__(self):
        self.input_file = Path("csv_reports/transacoes_outros.csv")
        self.output_file = Path("csv_reports/transacoes_outros_sugeridas.csv")
        
        # Mapeamento de padrões para categorias sugeridas
        self.pattern_mappings = {
            # Reservas e transações do MercadoPago
            r'reserva por gastos férias': 'Reservas',
            r'reserva por vendas férias': 'Reservas',
            r'liberação de dinheiro': 'Transferências',
            r'saída de dinheiro': 'Transferências',
            
            # Transporte
            r'uber': 'Transporte',
            r'99': 'Transporte',
            r'taxi': 'Transporte',
            r'pagamento cancelado uber': 'Transporte',
            
            # Contas e serviços
            r'da dae-jund': 'Moradia',
            r'da cpfl': 'Moradia',
            r'da sabesp': 'Moradia',
            r'energia': 'Moradia',
            r'água': 'Moradia',
            r'gás': 'Moradia',
            r'internet': 'Moradia',
            
            # Impostos e taxas
            r'int ipva': 'Impostos',
            r'int licenc': 'Impostos',
            r'imposto': 'Impostos',
            r'taxa': 'Impostos',
            r'ipva': 'Impostos',
            r'licenciamento': 'Impostos',
            
            # Entretenimento e lazer
            r'multiplex': 'Lazer',
            r'cinema': 'Lazer',
            r'teatro': 'Lazer',
            r'show': 'Lazer',
            r'concerto': 'Lazer',
            r'festival': 'Lazer',
            r'parque': 'Lazer',
            r'zoo': 'Lazer',
            r'aquário': 'Lazer',
            r'museu': 'Lazer',
            r'jogos': 'Lazer',
            r'game': 'Lazer',
            
            # Alimentação
            r'restaurante': 'Alimentação',
            r'padaria': 'Alimentação',
            r'lanchonete': 'Alimentação',
            r'pizzaria': 'Alimentação',
            r'fast food': 'Alimentação',
            r'ifood': 'Alimentação',
            r'rappi': 'Alimentação',
            r'uber eats': 'Alimentação',
            r'mcdonalds': 'Alimentação',
            r'burger king': 'Alimentação',
            r'starbucks': 'Alimentação',
            r'dominos': 'Alimentação',
            r'pizza hut': 'Alimentação',
            r'habibs': 'Alimentação',
            r'bobs': 'Alimentação',
            r'subway': 'Alimentação',
            
            # Saúde
            r'farmácia': 'Saúde',
            r'drogaria': 'Saúde',
            r'hospital': 'Saúde',
            r'clínica': 'Saúde',
            r'médico': 'Saúde',
            r'dentista': 'Saúde',
            r'fisioterapeuta': 'Saúde',
            r'psicólogo': 'Saúde',
            r'psiquiatra': 'Saúde',
            r'laboratório': 'Saúde',
            r'exame': 'Saúde',
            r'consulta': 'Saúde',
            r'medicamento': 'Saúde',
            r'remédio': 'Saúde',
            
            # Educação
            r'escola': 'Educação',
            r'colégio': 'Educação',
            r'universidade': 'Educação',
            r'faculdade': 'Educação',
            r'curso': 'Educação',
            r'treinamento': 'Educação',
            r'cursinho': 'Educação',
            r'vestibular': 'Educação',
            r'enem': 'Educação',
            r'material escolar': 'Educação',
            r'livro didático': 'Educação',
            r'biblioteca': 'Educação',
            r'cultura inglesa': 'Educação',
            r'wizard': 'Educação',
            r'ccaa': 'Educação',
            r'yazigi': 'Educação',
            r'fisk': 'Educação',
            r'senac': 'Educação',
            r'senai': 'Educação',
            
            # Vestuário e beleza
            r'roupa': 'Vestuário',
            r'camisa': 'Vestuário',
            r'calça': 'Vestuário',
            r'vestido': 'Vestuário',
            r'sapato': 'Vestuário',
            r'tênis': 'Vestuário',
            r'bolsa': 'Vestuário',
            r'mochila': 'Vestuário',
            r'carteira': 'Vestuário',
            r'relógio': 'Vestuário',
            r'joia': 'Vestuário',
            r'bijuteria': 'Vestuário',
            r'perfume': 'Vestuário',
            r'cosmético': 'Vestuário',
            r'maquiagem': 'Vestuário',
            r'shampoo': 'Vestuário',
            r'condicionador': 'Vestuário',
            r'sabonete': 'Vestuário',
            r'creme': 'Vestuário',
            r'protetor solar': 'Vestuário',
            r'desodorante': 'Vestuário',
            r'escova de dente': 'Vestuário',
            r'pasta de dente': 'Vestuário',
            r'fio dental': 'Vestuário',
            r'escova de cabelo': 'Vestuário',
            r'pente': 'Vestuário',
            r'manicure': 'Vestuário',
            r'pedicure': 'Vestuário',
            r'cabeleireiro': 'Vestuário',
            r'barbeiro': 'Vestuário',
            r'salão de beleza': 'Vestuário',
            r'spa': 'Vestuário',
            r'massagem': 'Vestuário',
            
            # Serviços
            r'advogado': 'Serviços',
            r'contador': 'Serviços',
            r'consultoria': 'Serviços',
            r'assessoria': 'Serviços',
            r'seguro': 'Serviços',
            r'previdência': 'Serviços',
            r'investimento': 'Serviços',
            r'corretora': 'Serviços',
            r'banco': 'Serviços',
            r'financiamento': 'Serviços',
            r'empréstimo': 'Serviços',
            r'cartão de crédito': 'Serviços',
            r'boleto': 'Serviços',
            r'pix': 'Transferências',
            r'transferência': 'Transferências',
            r'ted': 'Transferências',
            r'doc': 'Transferências',
            
            # Investimentos
            r'rendimento': 'Investimentos',
            r'dividendo': 'Investimentos',
            r'juros': 'Investimentos',
            r'aplicação': 'Investimentos',
            r'resgate': 'Investimentos',
            r'cdb': 'Investimentos',
            r'lci': 'Investimentos',
            r'lca': 'Investimentos',
            r'tesouro direto': 'Investimentos',
            r'ações': 'Investimentos',
            r'fii': 'Investimentos',
            r'criptomoeda': 'Investimentos',
            r'bitcoin': 'Investimentos',
            r'ethereum': 'Investimentos',
            r'binance': 'Investimentos',
            r'coinbase': 'Investimentos',
            r'mercado bitcoin': 'Investimentos',
            r'rend pag': 'Investimentos',
            r'aplic aut': 'Investimentos',
            r'aplicação automática': 'Investimentos',
            r'rendimento pago': 'Investimentos',
            
            # Compras online
            r'amazon': 'Compras Variadas',
            r'mercado livre': 'Compras Variadas',
            r'americanas': 'Compras Variadas',
            r'magazine luiza': 'Compras Variadas',
            r'casas bahia': 'Compras Variadas',
            r'kabum': 'Compras Variadas',
            r'terabyte': 'Compras Variadas',
            r'pichau': 'Compras Variadas',
            r'aliexpress': 'Compras Variadas',
            r'shopee': 'Compras Variadas',
            r'wish': 'Compras Variadas',
            r'olx': 'Compras Variadas',
            r'enjoei': 'Compras Variadas',
            r'b2w': 'Compras Variadas',
            r'submarino': 'Compras Variadas',
            r'shoptime': 'Compras Variadas',
            r'extra': 'Compras Variadas',
            r'carrefour': 'Compras Variadas',
            r'pão de açúcar': 'Compras Variadas',
            r'assai': 'Compras Variadas',
            r'atacadão': 'Compras Variadas',
            r'big': 'Compras Variadas',
            r'walmart': 'Compras Variadas',
            r'sam\'s club': 'Compras Variadas',
            r'makro': 'Compras Variadas',
            r'sacolão': 'Compras Variadas',
            r'hortifruti': 'Compras Variadas',
            r'natural da terra': 'Compras Variadas',
            r'emporio': 'Compras Variadas',
            r'mercearia': 'Compras Variadas',
            r'mini mercado': 'Compras Variadas',
            r'casa do pão': 'Compras Variadas',
            r'padaria são paulo': 'Compras Variadas',
            r'padaria real': 'Compras Variadas',
            r'padaria do seu joão': 'Compras Variadas',
            r'restaurante japonês': 'Compras Variadas',
            r'restaurante italiano': 'Compras Variadas',
            r'restaurante árabe': 'Compras Variadas',
            r'lanchonete do zé': 'Compras Variadas',
            r'pizzaria do tio': 'Compras Variadas',
            r'doceria da maria': 'Compras Variadas',
            
            # Lojas específicas
            r'renner': 'Vestuário',
            r'c&a': 'Vestuário',
            r'marisa': 'Vestuário',
            r'riachuelo': 'Vestuário',
            r'lojas americanas': 'Vestuário',
            r'magazine luiza': 'Vestuário',
            r'nike': 'Vestuário',
            r'adidas': 'Vestuário',
            r'puma': 'Vestuário',
            r'reebok': 'Vestuário',
            r'converse': 'Vestuário',
            r'vans': 'Vestuário',
            r'timberland': 'Vestuário',
            r'pay shopping': 'Vestuário',
            r'shopping': 'Vestuário',
            r'loja de roupas': 'Vestuário',
            r'loja de calçados': 'Vestuário',
            
            # Academia e fitness
            r'academia': 'Lazer',
            r'fitness': 'Lazer',
            r'crossfit': 'Lazer',
            r'pilates': 'Lazer',
            r'yoga': 'Lazer',
            r'natação': 'Lazer',
            r'futebol': 'Lazer',
            r'basquete': 'Lazer',
            r'tênis': 'Lazer',
            r'golfe': 'Lazer',
            r'esporte': 'Lazer',
            r'sport': 'Lazer',
            r'smart fit': 'Lazer',
            r'fitness one': 'Lazer',
            r'academia smart': 'Lazer',
            r'academia do seu joão': 'Lazer',
            
            # Viagens
            r'viagem': 'Lazer',
            r'hotel': 'Lazer',
            r'airbnb': 'Lazer',
            r'booking': 'Lazer',
            r'decolar': 'Lazer',
            r'hoteis.com': 'Lazer',
            r'passagem aérea': 'Lazer',
            r'passagem rodoviária': 'Lazer',
            r'aluguel de carro': 'Lazer',
            
            # Salário e remuneração
            r'salário': 'Salário',
            r'salario': 'Salário',
            r'remuneração': 'Salário',
            r'remuneracao': 'Salário',
            r'ordenado': 'Salário',
            r'vencimento': 'Salário',
            r'pagamento salário': 'Salário',
            r'pagamento salario': 'Salário',
            r'pag salário': 'Salário',
            r'pag salario': 'Salário',
            r'salário recebido': 'Salário',
            r'salario recebido': 'Salário',
            r'remuneração recebida': 'Salário',
            r'remuneracao recebida': 'Salário',
            r'ordenado recebido': 'Salário',
            r'vencimento recebido': 'Salário',
            r'pagamento de salário': 'Salário',
            r'pagamento de salario': 'Salário',
            r'13º salário': 'Salário',
            r'13o salario': 'Salário',
            r'décimo terceiro': 'Salário',
            r'decimo terceiro': 'Salário',
            r'férias': 'Salário',
            r'ferias': 'Salário',
            r'pagamento de férias': 'Salário',
            r'pagamento de ferias': 'Salário',
            r'férias proporcionais': 'Salário',
            r'ferias proporcionais': 'Salário',
            r'férias vencidas': 'Salário',
            r'ferias vencidas': 'Salário',
            r'férias \+ 1/3': 'Salário',
            r'ferias \+ 1/3': 'Salário',
            r'férias mais um terço': 'Salário',
            r'ferias mais um terco': 'Salário',
            r'vale refeição': 'Salário',
            r'vale refeicao': 'Salário',
            r'vale alimentação': 'Salário',
            r'vale alimentacao': 'Salário',
            r'vale transporte': 'Salário',
            r'vale combustível': 'Salário',
            r'vale combustivel': 'Salário',
            r'comissão': 'Salário',
            r'comissao': 'Salário',
            r'bônus': 'Salário',
            r'bonus': 'Salário',
            r'gratificação': 'Salário',
            r'gratificacao': 'Salário',
            r'prêmio': 'Salário',
            r'premio': 'Salário',
            r'incentivo': 'Salário',
            r'participação nos lucros': 'Salário',
            r'participacao nos lucros': 'Salário',
            r'plr': 'Salário',
            r'participação': 'Salário',
            r'participacao': 'Salário',
            r'lucros': 'Salário',
            r'lucro': 'Salário',
        }
    
    def run(self) -> None:
        """Executa a análise e geração do CSV com categorias sugeridas."""
        try:
            if not self.input_file.exists():
                print(f"❌ Arquivo {self.input_file} não encontrado!")
                return
            
            print("🔍 Analisando transações 'Outros'...")
            transactions = self._read_csv()
            
            print("💡 Sugerindo categorias...")
            categorized_transactions = self._suggest_categories(transactions)
            
            print("💾 Salvando arquivo com categorias sugeridas...")
            self._save_csv(categorized_transactions)
            
            print("📊 Gerando estatísticas...")
            self._show_statistics(categorized_transactions)
            
            print("✅ Processo concluído!")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            raise
    
    def _read_csv(self) -> List[Dict]:
        """Lê o arquivo CSV de transações 'Outros'."""
        transactions = []
        
        with open(self.input_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                transactions.append(row)
        
        print(f"📖 Lidas {len(transactions)} transações do arquivo CSV")
        return transactions
    
    def _suggest_categories(self, transactions: List[Dict]) -> List[Dict]:
        """Sugere categorias para as transações baseado na descrição."""
        categorized_transactions = []
        
        for transaction in transactions:
            description = transaction.get('description', '').lower()
            suggested_category = self._find_suggested_category(description)
            
            # Adiciona a categoria sugerida ao dicionário
            transaction['suggested_category'] = suggested_category
            categorized_transactions.append(transaction)
        
        return categorized_transactions
    
    def _find_suggested_category(self, description: str) -> str:
        """Encontra a categoria sugerida baseada na descrição."""
        for pattern, category in self.pattern_mappings.items():
            if re.search(pattern, description, re.IGNORECASE):
                return category
        
        # Se não encontrou nenhum padrão, retorna "Outros"
        return "Outros"
    
    def _save_csv(self, transactions: List[Dict]) -> None:
        """Salva o arquivo CSV com as categorias sugeridas."""
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['fitid', 'description', 'category', 'amount', 'date', 'file', 'suggested_category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Escreve o cabeçalho
            writer.writeheader()
            
            # Escreve as transações
            for transaction in transactions:
                fitid = transaction.get('fitid', '')
                if not fitid:
                    # Gera hash SHA1 de date+amount+description
                    import hashlib
                    base = f"{transaction.get('date','')}_{transaction.get('amount','')}_{transaction.get('description','')}"
                    fitid = hashlib.sha1(base.encode('utf-8')).hexdigest()
                    transaction['fitid'] = fitid
                writer.writerow(transaction)
        print(f"💾 Arquivo salvo: {self.output_file}")
    
    def _show_statistics(self, transactions: List[Dict]) -> None:
        """Mostra estatísticas das categorias sugeridas."""
        # Conta categorias sugeridas
        category_counts = Counter()
        for transaction in transactions:
            category = transaction.get('suggested_category', 'Outros')
            category_counts[category] += 1
        
        print("\n📊 ESTATÍSTICAS DAS CATEGORIAS SUGERIDAS:")
        print(f"Total de transações analisadas: {len(transactions)}")
        
        # Mostra as categorias mais frequentes
        print("\n🏆 TOP 10 CATEGORIAS SUGERIDAS:")
        for category, count in category_counts.most_common(10):
            percentage = (count / len(transactions)) * 100
            print(f"  {category}: {count} transações ({percentage:.1f}%)")
        
        # Mostra transações que ainda ficaram como "Outros"
        outros_count = category_counts.get("Outros", 0)
        outros_percentage = (outros_count / len(transactions)) * 100
        print(f"\n❓ Transações ainda como 'Outros': {outros_count} ({outros_percentage:.1f}%)")
        
        # Mostra exemplos de transações que ainda não foram categorizadas
        outros_transactions = [t for t in transactions if t.get('suggested_category') == 'Outros']
        if outros_transactions:
            print("\n🔍 EXEMPLOS DE TRANSAÇÕES AINDA NÃO CATEGORIZADAS:")
            for i, transaction in enumerate(outros_transactions[:10]):
                print(f"  {i+1}. {transaction['description']}")
            
            if len(outros_transactions) > 10:
                print(f"  ... e mais {len(outros_transactions) - 10} transações")
        
        # Mostra melhorias possíveis
        categorized_count = len(transactions) - outros_count
        improvement_percentage = (categorized_count / len(transactions)) * 100
        print(f"\n✅ Melhoria na categorização: {categorized_count} transações categorizadas ({improvement_percentage:.1f}%)")

def main():
    suggester = CategorySuggester()
    suggester.run()

if __name__ == '__main__':
    main() 