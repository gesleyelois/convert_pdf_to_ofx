"""
Serviço de limpeza de arquivos temporários.
Seguindo o princípio de Single Responsibility.
"""

import os
import shutil
from pathlib import Path
from typing import List
from services.logger import StructuredLogger
from config import TEMP_DIR, PROCESSING_CONFIG

class CleanupService:
    """Serviço responsável pela limpeza de arquivos temporários."""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.temp_dir = TEMP_DIR
        self.cleanup_enabled = PROCESSING_CONFIG['temp_cleanup_enabled']
    
    def cleanup_temp_directory(self) -> None:
        """Limpa o diretório temporário."""
        if not self.cleanup_enabled:
            self.logger.debug("Limpeza de arquivos temporários desabilitada")
            return
        
        if not self.temp_dir.exists():
            self.logger.debug(f"Diretório temporário não existe: {self.temp_dir}")
            return
        
        try:
            cleaned_files = 0
            for item in self.temp_dir.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                        cleaned_files += 1
                    elif item.is_dir():
                        shutil.rmtree(item)
                        cleaned_files += 1
                except Exception as e:
                    self.logger.warning(f"Não foi possível remover {item}: {e}")
            
            if cleaned_files > 0:
                self.logger.info(f"Limpeza concluída. {cleaned_files} itens removidos de '{self.temp_dir}'")
            else:
                self.logger.debug("Diretório temporário já estava limpo")
                
        except Exception as e:
            self.logger.error(f"Erro durante limpeza do diretório temporário: {e}")
    
    def cleanup_specific_files(self, file_paths: List[str]) -> None:
        """
        Remove arquivos específicos.
        
        Args:
            file_paths: Lista de caminhos de arquivos para remover
        """
        if not self.cleanup_enabled:
            return
        
        for file_path in file_paths:
            try:
                path = Path(file_path)
                if path.exists():
                    path.unlink()
                    self.logger.debug(f"Arquivo removido: {file_path}")
            except Exception as e:
                self.logger.warning(f"Não foi possível remover {file_path}: {e}")
    
    def ensure_temp_directory_exists(self) -> None:
        """Garante que o diretório temporário existe."""
        self.temp_dir.mkdir(exist_ok=True)
        self.logger.debug(f"Diretório temporário garantido: {self.temp_dir}") 