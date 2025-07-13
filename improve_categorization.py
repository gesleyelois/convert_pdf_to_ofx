#!/usr/bin/env python3
"""
Script automatizado para melhorar o sistema de categorização.
Executa todo o processo: categorização → extração de "Outros" → análise → sugestões → atualização.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from services.logger import StructuredLogger

class CategorizationImprover:
    """Classe para automatizar o processo de melhoria da categorização."""
    
    def __init__(self):
        self.logger = StructuredLogger()
        self.csv_dir = Path("csv_reports")
        self.csv_dir.mkdir(exist_ok=True)
    
    def run_full_process(self) -> None:
        """Executa todo o processo de melhoria da categorização."""
        try:
            self.logger.info("🚀 INICIANDO PROCESSO DE MELHORIA DA CATEGORIZAÇÃO")
            self.logger.info("=" * 60)
            
            # Passo 1: Categorização dos arquivos OFX
            self._step1_categorize_ofx()
            
            # Passo 2: Extrair transações "Outros"
            self._step2_extract_outros()
            
            # Passo 3: Analisar e sugerir categorias
            self._step3_suggest_categories()
            
            # Passo 4: Extrair palavras-chave
            self._step4_extract_keywords()
            
            # Passo 5: Mostrar resumo
            self._step5_show_summary()
            
            self.logger.info("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
            self.logger.info("📋 Verifique os arquivos gerados em: csv_reports/")
            self.logger.info("🔧 Atualize o keyword_config.py com as sugestões se necessário")
            
        except Exception as e:
            self.logger.error(f"❌ Erro no processo: {e}")
            raise
    
    def _step1_categorize_ofx(self) -> None:
        """Passo 1: Categorizar arquivos OFX."""
        self.logger.info("\n📊 PASSO 1: CATEGORIZANDO ARQUIVOS OFX")
        self.logger.info("-" * 40)
        
        try:
            # Executa o script de categorização
            result = subprocess.run([sys.executable, "categorize_smart.py"], 
                                 capture_output=True, text=True, check=True)
            
            self.logger.info("✅ Categorização concluída com sucesso!")
            self.logger.info(f"📝 Saída: {result.stdout}")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Erro na categorização: {e}")
            self.logger.error(f"Erro: {e.stderr}")
            raise
        except FileNotFoundError:
            self.logger.error("❌ Arquivo categorize_smart.py não encontrado!")
            raise
    
    def _step2_extract_outros(self) -> None:
        """Passo 2: Extrair transações classificadas como 'Outros'."""
        self.logger.info("\n🔍 PASSO 2: EXTRAINDO TRANSAÇÕES 'OUTROS'")
        self.logger.info("-" * 40)
        
        try:
            # Executa o script de extração
            result = subprocess.run([sys.executable, "extract_outros.py"], 
                                 capture_output=True, text=True, check=True)
            
            self.logger.info("✅ Extração de transações 'Outros' concluída!")
            self.logger.info(f"📝 Saída: {result.stdout}")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Erro na extração: {e}")
            self.logger.error(f"Erro: {e.stderr}")
            raise
        except FileNotFoundError:
            self.logger.error("❌ Arquivo extract_outros.py não encontrado!")
            raise
    
    def _step3_suggest_categories(self) -> None:
        """Passo 3: Analisar e sugerir categorias."""
        self.logger.info("\n💡 PASSO 3: SUGERINDO CATEGORIAS")
        self.logger.info("-" * 40)
        
        try:
            # Executa o script de sugestão
            result = subprocess.run([sys.executable, "suggest_categories.py"], 
                                 capture_output=True, text=True, check=True)
            
            self.logger.info("✅ Sugestões de categorias geradas!")
            self.logger.info(f"📝 Saída: {result.stdout}")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Erro na sugestão: {e}")
            self.logger.error(f"Erro: {e.stderr}")
            raise
        except FileNotFoundError:
            self.logger.error("❌ Arquivo suggest_categories.py não encontrado!")
            raise
    
    def _step4_extract_keywords(self) -> None:
        """Passo 4: Extrair palavras-chave das sugestões."""
        self.logger.info("\n🔧 PASSO 4: EXTRAINDO PALAVRAS-CHAVE")
        self.logger.info("-" * 40)
        
        try:
            # Executa o script de extração de palavras-chave
            result = subprocess.run([sys.executable, "extract_keywords.py"], 
                                 capture_output=True, text=True, check=True)
            
            self.logger.info("✅ Palavras-chave extraídas!")
            self.logger.info(f"📝 Saída: {result.stdout}")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Erro na extração de palavras-chave: {e}")
            self.logger.error(f"Erro: {e.stderr}")
            raise
        except FileNotFoundError:
            self.logger.error("❌ Arquivo extract_keywords.py não encontrado!")
            raise
    
    def _step5_show_summary(self) -> None:
        """Passo 5: Mostrar resumo dos arquivos gerados."""
        self.logger.info("\n📋 PASSO 5: RESUMO DOS ARQUIVOS GERADOS")
        self.logger.info("-" * 40)
        
        # Lista arquivos gerados
        csv_files = list(self.csv_dir.glob("*.csv"))
        
        if csv_files:
            self.logger.info("📁 Arquivos CSV gerados:")
            for csv_file in csv_files:
                size = csv_file.stat().st_size
                self.logger.info(f"  📄 {csv_file.name} ({size} bytes)")
        else:
            self.logger.warning("⚠️  Nenhum arquivo CSV encontrado!")
        
        # Mostra estatísticas se disponível
        outros_file = self.csv_dir / "transacoes_outros.csv"
        if outros_file.exists():
            try:
                import csv
                with open(outros_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    count = sum(1 for _ in reader)
                    self.logger.info(f"📊 Total de transações 'Outros' analisadas: {count}")
            except Exception as e:
                self.logger.warning(f"⚠️  Não foi possível contar transações: {e}")
    
    def run_step(self, step: str) -> None:
        """Executa um passo específico do processo."""
        self.logger.info(f"🎯 EXECUTANDO PASSO: {step}")
        
        if step == "1":
            self._step1_categorize_ofx()
        elif step == "2":
            self._step2_extract_outros()
        elif step == "3":
            self._step3_suggest_categories()
        elif step == "4":
            self._step4_extract_keywords()
        elif step == "5":
            self._step5_show_summary()
        else:
            self.logger.error(f"❌ Passo inválido: {step}")
            self.logger.info("Passos válidos: 1, 2, 3, 4, 5")
    
    def show_help(self) -> None:
        """Mostra ajuda sobre o processo."""
        self.logger.info("📖 AJUDA - PROCESSO DE MELHORIA DA CATEGORIZAÇÃO")
        self.logger.info("=" * 60)
        self.logger.info("""
Este script automatiza o processo de melhoria do sistema de categorização:

🔧 PROCESSO COMPLETO:
1. Categoriza arquivos OFX usando categorize_smart.py
2. Extrai transações classificadas como "Outros"
3. Analisa e sugere categorias para transações "Outros"
4. Extrai palavras-chave das sugestões
5. Mostra resumo dos arquivos gerados

📁 ARQUIVOS GERADOS:
- csv_reports/transacoes_outros.csv
- csv_reports/transacoes_outros_sugeridas.csv

🎯 USO:
- Processo completo: python improve_categorization.py
- Passo específico: python improve_categorization.py --step 2
- Ajuda: python improve_categorization.py --help

📋 PRÓXIMOS PASSOS:
1. Analise o arquivo transacoes_outros_sugeridas.csv
2. Atualize keyword_config.py com as sugestões
3. Teste as melhorias com test_new_categories.py
4. Reexecute o processo se necessário
        """)

def main():
    parser = argparse.ArgumentParser(
        description="Script automatizado para melhorar o sistema de categorização",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python improve_categorization.py                    # Processo completo
  python improve_categorization.py --step 2          # Apenas extrair "Outros"
  python improve_categorization.py --help            # Mostrar ajuda
        """
    )
    
    parser.add_argument(
        "--step",
        type=str,
        choices=["1", "2", "3", "4", "5"],
        help="Executar apenas um passo específico"
    )
    
    parser.add_argument(
        "--help-process",
        action="store_true",
        help="Mostrar ajuda detalhada sobre o processo"
    )
    
    args = parser.parse_args()
    
    improver = CategorizationImprover()
    
    if args.help_process:
        improver.show_help()
    elif args.step:
        improver.run_step(args.step)
    else:
        improver.run_full_process()

if __name__ == '__main__':
    main() 