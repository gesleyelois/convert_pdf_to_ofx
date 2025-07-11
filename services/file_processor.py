"""
Serviço de processamento de arquivos.
Seguindo o princípio de Single Responsibility.
"""

import os
from pathlib import Path
from typing import List
from interfaces import FileProcessor, ProcessingResult, OFXWriter
from services.bank_identifier import BankIdentifier
from services.file_validator import PDFFileValidator
from services.logger import StructuredLogger

class PDFFileProcessor(FileProcessor):
    """Processador de arquivos PDF."""
    
    def __init__(self, ofx_writer: OFXWriter, logger: StructuredLogger):
        self.ofx_writer = ofx_writer
        self.logger = logger
        self.bank_identifier = BankIdentifier()
        self.file_validator = PDFFileValidator()
    
    def process_file(self, file_path: str) -> ProcessingResult:
        """
        Processa um arquivo PDF individual.
        
        Args:
            file_path: Caminho para o arquivo PDF
            
        Returns:
            Resultado do processamento
        """
        file_name = Path(file_path).name
        
        # Validar arquivo
        if not self.file_validator.is_valid_file(file_path):
            error_msg = f"Arquivo inválido: {file_name}"
            self.logger.error(error_msg)
            return ProcessingResult(
                success=False,
                file_name=file_name,
                bank_name="",
                transactions_count=0,
                error_message=error_msg
            )
        
        # Identificar banco
        bank_name = self.bank_identifier.identify_bank(file_name)
        if not bank_name:
            error_msg = f"Banco não identificado para: {file_name}"
            self.logger.error(error_msg)
            return ProcessingResult(
                success=False,
                file_name=file_name,
                bank_name="",
                transactions_count=0,
                error_message=error_msg
            )
        
        # Obter parser
        parser = self.bank_identifier.get_parser(bank_name)
        if not parser:
            error_msg = f"Parser não encontrado para banco: {bank_name}"
            self.logger.error(error_msg)
            return ProcessingResult(
                success=False,
                file_name=file_name,
                bank_name=bank_name,
                transactions_count=0,
                error_message=error_msg
            )
        
        try:
            # Processar arquivo
            self.logger.info(f"Processando {file_name} ({bank_name})...")
            
            transactions, account_data = parser.parse(file_path)
            
            # Gerar arquivo OFX
            output_path = self._generate_output_path(file_path)
            self.ofx_writer.write(transactions, account_data, output_path)
            
            self.logger.info(
                f"{file_name} convertido com sucesso! "
                f"Total de transações: {len(transactions)}"
            )
            
            return ProcessingResult(
                success=True,
                file_name=file_name,
                bank_name=bank_name,
                transactions_count=len(transactions)
            )
            
        except Exception as e:
            error_msg = f"Falha ao processar {file_name}: {str(e)}"
            self.logger.error(error_msg)
            return ProcessingResult(
                success=False,
                file_name=file_name,
                bank_name=bank_name,
                transactions_count=0,
                error_message=error_msg
            )
    
    def _generate_output_path(self, input_path: str) -> str:
        """Gera o caminho de saída para o arquivo OFX."""
        from config import OFXS_DIR
        
        input_path_obj = Path(input_path)
        output_filename = input_path_obj.stem + '.ofx'
        return str(OFXS_DIR / output_filename) 