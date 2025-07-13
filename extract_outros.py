#!/usr/bin/env python3
"""
Script para extrair todas as transações classificadas como "Outros" e gerar um arquivo CSV.
"""

import csv
import argparse
from pathlib import Path
from typing import List, Dict
from ofxparse import OfxParser
from services.logger import StructuredLogger
from services.smart_keyword_categorizer import SmartKeywordCategorizer
import hashlib

class ExtractOutrosTransactions:
    """Classe para extrair transações classificadas como 'Outros'."""
    
    def __init__(self):
        self.logger = StructuredLogger()
        self.categorizer = SmartKeywordCategorizer(self.logger)
        self.ofxs_dir = Path("ofxs_gerados")
        self.output_file = Path("csv_reports/transacoes_outros.csv")
    
    def run(self) -> None:
        """Executa a extração das transações 'Outros'."""
        try:
            self._setup_directories()
            outros_transactions = self._extract_outros_transactions()
            self._save_csv(outros_transactions)
            self._show_statistics(outros_transactions)
        except Exception as e:
            self.logger.error(f"Erro crítico na aplicação: {e}")
            raise
    
    def _setup_directories(self) -> None:
        """Configura diretórios necessários."""
        if not self.ofxs_dir.exists():
            self.logger.error(f"Diretório {self.ofxs_dir} não encontrado!")
            raise FileNotFoundError(f"Diretório {self.ofxs_dir} não encontrado")
        
        self.logger.info("Diretórios configurados com sucesso")
    
    def _extract_outros_transactions(self) -> List[Dict]:
        """Extrai todas as transações classificadas como 'Outros'."""
        outros_transactions = []
        ofx_files = list(self.ofxs_dir.glob("*.ofx"))
        
        if not ofx_files:
            self.logger.warning(f"Nenhum arquivo OFX encontrado em {self.ofxs_dir}")
            return outros_transactions
        
        self.logger.info(f"Processando {len(ofx_files)} arquivos OFX para extrair transações 'Outros'")
        
        for ofx_file in ofx_files:
            self.logger.info(f"Processando: {ofx_file.name}")
            file_outros = self._process_single_file(outros_transactions, ofx_file)
            self.logger.info(f"Encontradas {file_outros} transações 'Outros' em {ofx_file.name}")
        
        return outros_transactions
    
    def _process_single_file(self, outros_transactions: List[Dict], ofx_file: Path) -> int:
        """Processa um único arquivo OFX e extrai transações 'Outros'."""
        try:
            # Lê o arquivo OFX usando ofxparse com diferentes encodings
            encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            parsed_ofx = None
            
            for encoding in encodings_to_try:
                try:
                    with open(ofx_file, 'r', encoding=encoding, errors='ignore') as file:
                        ofx = OfxParser()
                        parsed_ofx = ofx.parse(file)
                    break  # Se chegou aqui, o encoding funcionou
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    # Se não for erro de encoding, tenta o próximo
                    if 'codec' in str(e).lower():
                        continue
                    else:
                        raise e
            
            if parsed_ofx is None:
                raise Exception("Não foi possível ler o arquivo com nenhum encoding suportado")
            
            # Extrai transações
            transactions = self._extract_transactions_from_ofx(parsed_ofx)
            
            if not transactions:
                return 0
            
            # Categoriza e filtra apenas as transações 'Outros'
            outros_count = 0
            for transaction in transactions:
                description = transaction.get('description', '')
                amount = transaction.get('amount', 0.0)
                
                # Categoriza a transação
                category = self.categorizer.categorize_transaction(description, amount)
                
                # Se for 'Outros', adiciona à lista
                if category == "Outros":
                    outros_transactions.append({
                        'description': description,
                        'category': category,
                        'amount': amount,
                        'date': transaction.get('date', 'N/A'),
                        'file': ofx_file.name
                    })
                    outros_count += 1
            
            return outros_count
            
        except Exception as e:
            self.logger.error(f"Erro ao processar {ofx_file.name}: {e}")
            return 0
    
    def _extract_transactions_from_ofx(self, parsed_ofx) -> List[Dict]:
        """Extrai todas as transações do arquivo OFX usando ofxparse."""
        transactions = []
        
        # Tenta extrair de diferentes tipos de conta
        for account in parsed_ofx.accounts:
            if hasattr(account, 'statement') and account.statement:
                for transaction in account.statement.transactions:
                    transaction_dict = {
                        'description': transaction.memo or transaction.type or '',
                        'amount': float(transaction.amount) if transaction.amount else 0.0,
                        'date': transaction.date,
                        'type': transaction.type,
                        'id': transaction.id if hasattr(transaction, 'id') else None
                    }
                    transactions.append(transaction_dict)
        
        return transactions
    
    def _save_csv(self, outros_transactions: List[Dict]) -> None:
        """Salva as transações 'Outros' em um arquivo CSV."""
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['fitid', 'description', 'category', 'amount', 'date', 'file']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Escreve o cabeçalho
                writer.writeheader()
                
                # Escreve as transações
                for transaction in outros_transactions:
                    fitid = transaction.get('fitid', '')
                    if not fitid:
                        # Gera hash SHA1 de date+amount+description
                        base = f"{transaction.get('date','')}_{transaction.get('amount','')}_{transaction.get('description','')}"
                        fitid = hashlib.sha1(base.encode('utf-8')).hexdigest()
                        transaction['fitid'] = fitid
                    writer.writerow(transaction)
            
            self.logger.info(f"Arquivo CSV salvo: {self.output_file}")
            self.logger.info(f"Total de transações 'Outros' exportadas: {len(outros_transactions)}")
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar arquivo CSV: {e}")
            raise
    
    def _show_statistics(self, outros_transactions: List[Dict]) -> None:
        """Mostra estatísticas das transações 'Outros'."""
        if not outros_transactions:
            self.logger.info("Nenhuma transação 'Outros' encontrada!")
            return
        
        self.logger.info("=== ESTATÍSTICAS DAS TRANSAÇÕES 'OUTROS' ===")
        self.logger.info(f"Total de transações 'Outros': {len(outros_transactions)}")
        
        # Estatísticas por arquivo
        file_stats = {}
        for transaction in outros_transactions:
            file_name = transaction['file']
            file_stats[file_name] = file_stats.get(file_name, 0) + 1
        
        self.logger.info("\nDistribuição por arquivo:")
        for file_name, count in sorted(file_stats.items()):
            self.logger.info(f"  {file_name}: {count} transações")
        
        # Estatísticas de valores
        total_amount = sum(t['amount'] for t in outros_transactions)
        avg_amount = total_amount / len(outros_transactions) if outros_transactions else 0
        
        self.logger.info(f"\nValor total das transações 'Outros': R$ {total_amount:.2f}")
        self.logger.info(f"Valor médio por transação: R$ {avg_amount:.2f}")
        
        # Mostra algumas descrições para análise
        self.logger.info("\nExemplos de descrições 'Outros':")
        for i, transaction in enumerate(outros_transactions[:10]):  # Primeiras 10
            self.logger.info(f"  {i+1}. {transaction['description']}")
        
        if len(outros_transactions) > 10:
            self.logger.info(f"  ... e mais {len(outros_transactions) - 10} transações")

def main():
    parser = argparse.ArgumentParser(
        description="Extrai transações classificadas como 'Outros' e gera arquivo CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python extract_outros.py
  python extract_outros.py --output transacoes_nao_categorizadas.csv
        """
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="transacoes_outros.csv",
        help="Nome do arquivo CSV de saída (padrão: transacoes_outros.csv)"
    )
    
    args = parser.parse_args()
    
    app = ExtractOutrosTransactions()
    app.output_file = Path(args.output)
    app.run()

if __name__ == '__main__':
    main() 