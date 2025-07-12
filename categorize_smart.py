"""
Categorização inteligente de arquivos OFX usando palavras-chave otimizadas.
Versão simplificada e eficiente para o contexto bancário brasileiro.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import xml.etree.ElementTree as ET
from ofxparse import OfxParser
from services.logger import StructuredLogger
from services.smart_keyword_categorizer import SmartKeywordCategorizer

class SmartCategorizeOFXApp:
    """Aplicação de categorização inteligente usando palavras-chave."""
    
    def __init__(self):
        self.logger = StructuredLogger()
        self.categorizer = SmartKeywordCategorizer(self.logger)
        self.ofxs_dir = Path("ofxs_gerados")
        self.output_dir = Path("ofxs_categorizados")
    
    def run(self) -> None:
        """Executa a categorização inteligente."""
        try:
            self._setup_directories()
            self._show_categorizer_info()
            self._process_ofx_files()
            self._show_statistics()
        except Exception as e:
            self.logger.error(f"Erro crítico na aplicação: {e}")
            raise
    
    def _setup_directories(self) -> None:
        """Configura diretórios necessários."""
        self.output_dir.mkdir(exist_ok=True)
        self.logger.info("Diretórios configurados com sucesso")
    
    def _show_categorizer_info(self) -> None:
        """Mostra informações sobre o categorizador."""
        categories = self.categorizer.get_available_categories()
        self.logger.info(f"Categorizador inteligente carregado com {len(categories)} categorias:")
        for category in categories:
            self.logger.info(f"  - {category}")
    
    def _process_ofx_files(self) -> None:
        """Processa todos os arquivos OFX encontrados."""
        ofx_files = list(self.ofxs_dir.glob("*.ofx"))
        
        if not ofx_files:
            self.logger.warning(f"Nenhum arquivo OFX encontrado em {self.ofxs_dir}")
            return
        
        self.logger.info(f"Encontrados {len(ofx_files)} arquivos OFX para categorizar")
        
        total_transactions = 0
        categorized_transactions = 0
        
        for ofx_file in ofx_files:
            self.logger.info(f"Processando: {ofx_file.name}")
            result = self._process_single_file(ofx_file)
            total_transactions += result['total']
            categorized_transactions += result['categorized']
        
        self.logger.info(f"Processamento concluído: {categorized_transactions}/{total_transactions} transações categorizadas")
    
    def _process_single_file(self, ofx_file: Path) -> Dict[str, int]:
        """Processa um único arquivo OFX."""
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
                self.logger.warning(f"Nenhuma transação encontrada em {ofx_file.name}")
                return {'total': 0, 'categorized': 0}
            
            # Categoriza as transações
            categorized_count = 0
            categorized_transactions = []
            
            for transaction in transactions:
                category = self._categorize_transaction(transaction)
                if category:
                    categorized_count += 1
                    transaction['category'] = category
                categorized_transactions.append(transaction)
            
            # Salva o arquivo categorizado
            output_file = self.output_dir / f"categorizado_{ofx_file.name}"
            self._save_categorized_ofx_file(ofx_file, categorized_transactions, output_file)
            
            self.logger.info(f"Arquivo processado: {categorized_count}/{len(transactions)} transações categorizadas")
            
            return {'total': len(transactions), 'categorized': categorized_count}
            
        except Exception as e:
            self.logger.error(f"Erro ao processar {ofx_file.name}: {e}")
            return {'total': 0, 'categorized': 0}
    
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
    
    def _categorize_transaction(self, transaction: Dict) -> str:
        """Categoriza uma transação individual."""
        try:
            description = transaction.get('description', '')
            amount = transaction.get('amount', 0.0)
            
            # Categoriza usando o sistema inteligente
            category = self.categorizer.categorize_transaction(description, amount)
            
            return category
            
        except Exception as e:
            self.logger.error(f"Erro ao categorizar transação: {e}")
            return "Outros"
    
    def _save_categorized_ofx_file(self, original_file: Path, categorized_transactions: List[Dict], output_file: Path) -> None:
        """Salva o arquivo OFX categorizado."""
        try:
            # Lê o conteúdo original do arquivo com encoding correto
            encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            original_content = None
            
            for encoding in encodings_to_try:
                try:
                    with open(original_file, 'r', encoding=encoding, errors='ignore') as f:
                        original_content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if original_content is None:
                original_content = "Erro ao ler arquivo original"
            
            # Cria um arquivo de relatório com as categorizações
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("=== RELATÓRIO DE CATEGORIZAÇÃO ===\n\n")
                f.write(f"Total de transações: {len(categorized_transactions)}\n\n")
                
                # Agrupa por categoria
                categories = {}
                for transaction in categorized_transactions:
                    category = transaction.get('category', 'Outros')
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(transaction)
                
                # Escreve estatísticas por categoria
                for category, transactions in sorted(categories.items()):
                    total_amount = sum(t.get('amount', 0) for t in transactions)
                    f.write(f"\n=== {category.upper()} ===\n")
                    f.write(f"Quantidade: {len(transactions)}\n")
                    f.write(f"Valor total: R$ {total_amount:.2f}\n")
                    f.write("Transações:\n")
                    
                    for transaction in transactions:
                        date = transaction.get('date', 'N/A')
                        amount = transaction.get('amount', 0)
                        description = transaction.get('description', '')
                        f.write(f"  {date}: R$ {amount:.2f} - {description}\n")
                
                f.write(f"\n\n=== CONTEÚDO ORIGINAL ===\n")
                f.write(original_content)
            
            self.logger.info(f"Arquivo salvo: {output_file.name}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar arquivo: {e}")
    
    def _show_statistics(self) -> None:
        """Mostra estatísticas da categorização."""
        self.logger.info("=== ESTATÍSTICAS DE CATEGORIZAÇÃO ===")
        
        # Conta transações por categoria nos arquivos processados
        category_stats = {}
        total_files = 0
        total_transactions = 0
        
        for output_file in self.output_dir.glob("categorizado_*.ofx"):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extrai estatísticas do arquivo de relatório
                lines = content.split('\n')
                in_category = False
                current_category = None
                
                for line in lines:
                    if line.startswith('=== ') and line.endswith(' ==='):
                        current_category = line[4:-4].strip()
                        if current_category != 'RELATÓRIO DE CATEGORIZAÇÃO' and current_category != 'CONTEÚDO ORIGINAL':
                            in_category = True
                        else:
                            in_category = False
                    elif in_category and line.strip().startswith('Quantidade:'):
                        try:
                            count = int(line.split(':')[1].strip())
                            category_stats[current_category] = category_stats.get(current_category, 0) + count
                            total_transactions += count
                        except (ValueError, IndexError):
                            pass
                
                total_files += 1
                
            except Exception as e:
                self.logger.error(f"Erro ao ler estatísticas de {output_file.name}: {e}")
        
        # Mostra estatísticas
        if total_transactions > 0:
            self.logger.info(f"Total de arquivos processados: {total_files}")
            self.logger.info(f"Total de transações categorizadas: {total_transactions}")
            self.logger.info("\nDistribuição por categoria:")
            
            for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_transactions) * 100
                self.logger.info(f"  {category}: {count} ({percentage:.1f}%)")
            
            # Mostra eficácia (quanto reduziu "Outros")
            outros_count = category_stats.get("Outros", 0)
            outros_percentage = (outros_count / total_transactions) * 100
            self.logger.info(f"\nEficácia da categorização:")
            self.logger.info(f"  Categoria 'Outros': {outros_count} ({outros_percentage:.1f}%)")
            
            try:
                from keyword_config import EFFICIENCY_TARGETS
            except ImportError:
                EFFICIENCY_TARGETS = {
                    "excellent": 30,
                    "good": 50,
                    "needs_improvement": 50
                }
            
            if outros_percentage < EFFICIENCY_TARGETS["excellent"]:
                self.logger.info("✅ Excelente categorização! Menos de 30% em 'Outros'")
            elif outros_percentage < EFFICIENCY_TARGETS["good"]:
                self.logger.info("✅ Boa categorização! Menos de 50% em 'Outros'")
            else:
                self.logger.warning("⚠️  Categorização pode ser melhorada. Muitas transações em 'Outros'")
    
    def test_categorization(self) -> None:
        """Testa o sistema de categorização com exemplos."""
        self.logger.info("=== TESTE DE CATEGORIZAÇÃO ===")
        
        test_cases = [
            ("PIX QRS IFOOD COM A18/06", 45.90, "Alimentação"),
            ("PAY UBER 14/06", 25.50, "Transporte"),
            ("DA DROGASIL 19/06", 15.80, "Saúde"),
            ("DA SABESP 00000118677", 120.00, "Moradia"),
            ("PIX TRANSF Bruna A17/06", 500.00, "Transferências"),
            ("REND PAGO APLIC AUT MAIS", 150.00, "Investimentos"),
            ("PAY CINEMA 20/06", 35.00, "Lazer"),
            ("PAY SHOPPING 22/06", 200.00, "Vestuário"),
            ("PAY ADVOGADO 25/06", 800.00, "Serviços"),
            ("PAY ESCOLA 28/06", 500.00, "Educação"),
            ("PAY DESCONHECIDO 30/06", 50.00, "Outros"),
        ]
        
        correct = 0
        total = len(test_cases)
        
        for description, amount, expected in test_cases:
            result = self.categorizer.categorize_transaction(description, amount)
            status = "✅" if result == expected else "❌"
            self.logger.info(f"{status} '{description}' -> {result} (esperado: {expected})")
            if result == expected:
                correct += 1
        
        accuracy = (correct / total) * 100
        self.logger.info(f"\nPrecisão do teste: {correct}/{total} ({accuracy:.1f}%)")
        
        if accuracy >= 80:
            self.logger.info("✅ Sistema de categorização funcionando bem!")
        else:
            self.logger.warning("⚠️  Sistema pode precisar de ajustes")

def main():
    parser = argparse.ArgumentParser(
        description="Categorização inteligente de arquivos OFX usando palavras-chave",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python categorize_smart.py
  python categorize_smart.py --test
        """
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Executa teste de categorização com exemplos"
    )
    
    args = parser.parse_args()
    
    app = SmartCategorizeOFXApp()
    
    if args.test:
        app.test_categorization()
    else:
        app.run()

if __name__ == '__main__':
    main() 