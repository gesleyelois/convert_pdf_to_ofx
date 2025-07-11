"""
Serviço de validação de arquivos.
Seguindo o princípio de Single Responsibility.
"""

import os
from pathlib import Path
from typing import List
from interfaces import FileValidator
from config import PROCESSING_CONFIG

class PDFFileValidator(FileValidator):
    """Validador de arquivos PDF."""
    
    def __init__(self):
        self.supported_extensions = PROCESSING_CONFIG['supported_extensions']
        self.max_file_size_mb = PROCESSING_CONFIG['max_file_size_mb']
    
    def is_valid_file(self, file_path: str) -> bool:
        """Verifica se o arquivo é válido para processamento."""
        try:
            path = Path(file_path)
            
            # Verificar se o arquivo existe
            if not path.exists():
                return False
            
            # Verificar extensão
            if path.suffix.lower() not in self.supported_extensions:
                return False
            
            # Verificar tamanho do arquivo
            file_size_mb = path.stat().st_size / (1024 * 1024)
            if file_size_mb > self.max_file_size_mb:
                return False
            
            # Verificar se é um arquivo (não diretório)
            if not path.is_file():
                return False
            
            return True
            
        except (OSError, ValueError):
            return False
    
    def get_file_extension(self, file_path: str) -> str:
        """Retorna a extensão do arquivo."""
        return Path(file_path).suffix.lower()
    
    def get_file_size_mb(self, file_path: str) -> float:
        """Retorna o tamanho do arquivo em MB."""
        return Path(file_path).stat().st_size / (1024 * 1024) 