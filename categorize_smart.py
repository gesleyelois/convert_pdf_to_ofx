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
import unicodedata
import re # Added for regex processing
from keyword_config import CATEGORY_KEYWORDS

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
                        # Se for erro de ledger balance, tenta processar mesmo assim
                        if 'Empty ledger balance' in str(e):
                            self.logger.warning(f"Saldo não pode ser lido em {ofx_file.name}, mas continuando processamento...")
                            # Tenta processar o arquivo mesmo com erro de saldo
                            try:
                                with open(ofx_file, 'r', encoding=encoding, errors='ignore') as file:
                                    ofx = OfxParser()
                                    parsed_ofx = ofx.parse(file)
                                break
                            except Exception as parse_error:
                                # Se ainda falhar, tenta processar o arquivo diretamente
                                self.logger.warning(f"Tentando processamento alternativo para {ofx_file.name}")
                                return self._process_ofx_alternative(ofx_file)
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
    
    def _process_ofx_alternative(self, ofx_file: Path) -> Dict[str, int]:
        """Processa arquivo OFX usando método alternativo quando ofxparse falha."""
        try:
            # Lê o arquivo diretamente e extrai transações usando regex
            with open(ofx_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extrai transações usando regex
            transactions = self._extract_transactions_with_regex(content)
            
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
            self._save_categorized_ofx_file(ofx_file, categorized_transactions, None)
            
            self.logger.info(f"Arquivo processado (método alternativo): {categorized_count}/{len(transactions)} transações categorizadas")
            
            return {'total': len(transactions), 'categorized': categorized_count}
            
        except Exception as e:
            self.logger.error(f"Erro no processamento alternativo de {ofx_file.name}: {e}")
            return {'total': 0, 'categorized': 0}
    
    def _extract_transactions_from_ofx(self, parsed_ofx) -> List[Dict]:
        """Extrai todas as transações do arquivo OFX usando ofxparse."""
        transactions = []
        
        # Tenta extrair de diferentes tipos de conta
        for account in parsed_ofx.accounts:
            if hasattr(account, 'statement') and account.statement:
                for transaction in account.statement.transactions:
                    # Formatar data como YYYYMMDD
                    date_str = transaction.date.strftime('%Y%m%d') if transaction.date else ''
                    
                    transaction_dict = {
                        'description': transaction.memo or transaction.type or '',
                        'amount': float(transaction.amount) if transaction.amount else 0.0,
                        'date': date_str,
                        'type': transaction.type,
                        'id': transaction.id if hasattr(transaction, 'id') else None
                    }
                    transactions.append(transaction_dict)
        
        return transactions
    
    def _extract_transactions_with_regex(self, content: str) -> List[Dict]:
        """Extrai transações do conteúdo OFX usando regex."""
        transactions = []
        
        # Padrão para encontrar blocos de transação
        transaction_pattern = r'<STMTTRN>.*?</STMTTRN>'
        transaction_blocks = re.findall(transaction_pattern, content, re.DOTALL)
        
        for i, block in enumerate(transaction_blocks):
            try:
                # Padrões para extrair dados da transação
                trntype_pattern = r'<TRNTYPE>([^<\n]+)'
                dtposted_pattern = r'<DTPOSTED>([^<\n]+)'
                trnamt_pattern = r'<TRNAMT>([^<\n]+)'
                memo_pattern = r'<MEMO>([^<\n]+)'
                fitid_pattern = r'<FITID>([^<\n]+)'
                
                # Extrair valores
                trntype = re.search(trntype_pattern, block)
                dtposted = re.search(dtposted_pattern, block)
                trnamt = re.search(trnamt_pattern, block)
                memo = re.search(memo_pattern, block)
                fitid = re.search(fitid_pattern, block)
                
                if all([trntype, dtposted, trnamt]):
                    # Processar tipo de transação
                    transaction_type = "entrada" if trntype.group(1).strip() == "CREDIT" else "saída"
                    
                    # Processar data (formato OFX: YYYYMMDDHHMMSS)
                    date_str = dtposted.group(1).strip()[:8]  # Pegar apenas YYYYMMDD
                    
                    # Processar valor
                    amount = float(trnamt.group(1).strip())
                    
                    # Processar descrição
                    description = memo.group(1).strip() if memo else f"Transação {i + 1}"
                    
                    # Processar FITID
                    fitid_str = fitid.group(1).strip() if fitid else f"trans_{i + 1}_{date_str}"
                    
                    transaction_dict = {
                        'description': description,
                        'amount': amount,
                        'date': date_str,  # Usar formato YYYYMMDD
                        'type': trntype.group(1).strip(),
                        'fitid': fitid_str
                    }
                    transactions.append(transaction_dict)
                    
            except Exception as e:
                self.logger.warning(f"Erro ao processar transação {i + 1}: {e}")
                continue
        
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
        """Salva o arquivo OFX categorizado mantendo o formato original."""
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
                raise Exception("Não foi possível ler o arquivo original")
            
            # Cria um mapeamento de transações por FITID
            transaction_map = {}
            for transaction in categorized_transactions:
                fitid = transaction.get('fitid', '')
                if fitid:
                    transaction_map[fitid] = transaction.get('category', 'Outros')
            
            # Modifica o conteúdo OFX original adicionando categorias
            modified_content = self._add_categories_to_ofx(original_content, transaction_map)
            
            # Salva o arquivo com o mesmo nome do original (sem prefixo)
            output_file = self.output_dir / original_file.name
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            self.logger.info(f"Arquivo OFX categorizado salvo: {output_file.name}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar arquivo: {e}")

    def _normalize_text(self, text: str) -> str:
        """Normaliza texto para comparação flexível (sem acento, caixa baixa, sem espaços extras)."""
        text = text.lower().strip()
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        text = ' '.join(text.split())
        return text

    def _add_categories_to_ofx(self, ofx_content: str, transaction_map: Dict[str, str]) -> str:
        """Adiciona categorias ao conteúdo OFX original usando FITID quando possível."""
        lines = ofx_content.split('\n')
        modified_lines = []
        last_fitid = None
        
        for line in lines:
            if '<FITID>' in line:
                # Captura o FITID da transação
                last_fitid = line.replace('<FITID>', '').replace('</FITID>', '').strip()
                modified_lines.append(line)
            elif '<MEMO>' in line:
                # Extrai o conteúdo do MEMO
                if '</MEMO>' in line:
                    memo_content = line.replace('<MEMO>', '').replace('</MEMO>', '').strip()
                else:
                    memo_content = line.replace('<MEMO>', '').strip()
                
                # Busca categoria pelo FITID ou categoriza pela descrição
                category = None
                if last_fitid and last_fitid in transaction_map:
                    category = transaction_map[last_fitid]
                else:
                    category = self.categorizer.categorize_transaction(memo_content, 0)
                
                # Adiciona categoria se não existir
                if '[CATEGORIA:' not in memo_content:
                    if '</MEMO>' in line:
                        modified_memo = f"<MEMO>{memo_content} [CATEGORIA: {category}]</MEMO>"
                    else:
                        modified_memo = f"<MEMO>{memo_content} [CATEGORIA: {category}]"
                else:
                    if '</MEMO>' in line:
                        modified_memo = f"<MEMO>{memo_content}</MEMO>"
                    else:
                        modified_memo = f"<MEMO>{memo_content}"
                
                modified_lines.append(modified_memo)
            else:
                modified_lines.append(line)
        
        return '\n'.join(modified_lines)
    
    def _show_statistics(self) -> None:
        """Mostra estatísticas da categorização."""
        self.logger.info("=== ESTATÍSTICAS DE CATEGORIZAÇÃO ===")
        
        # Conta transações por categoria nos arquivos processados
        category_stats = {}
        total_files = 0
        total_transactions = 0
        
        for output_file in self.output_dir.glob("*.ofx"):
            # Pula arquivos que não são do diretório de saída (arquivos originais)
            if output_file.parent.name != "ofxs_categorizados":
                continue
                
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Conta categorias no arquivo OFX
                lines = content.split('\n')
                for line in lines:
                    if '[CATEGORIA:' in line and ']' in line:
                        # Extrai a categoria da linha
                        start_idx = line.find('[CATEGORIA:') + 11
                        end_idx = line.find(']', start_idx)
                        if start_idx > 10 and end_idx > start_idx:
                            category = line[start_idx:end_idx].strip()
                            category_stats[category] = category_stats.get(category, 0) + 1
                            total_transactions += 1
                
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

def main():
    parser = argparse.ArgumentParser(
        description="Categorização inteligente de arquivos OFX usando palavras-chave",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python categorize_smart.py
        """
    )
    
    args = parser.parse_args()
    
    app = SmartCategorizeOFXApp()
    app.run()

if __name__ == '__main__':
    main() 