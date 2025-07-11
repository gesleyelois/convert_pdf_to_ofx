"""
Serviço de logging estruturado.
Seguindo o princípio de Single Responsibility.
"""

import logging
from typing import Optional
from interfaces import Logger
from config import LOG_CONFIG

class StructuredLogger(Logger):
    """Implementação de logger estruturado."""
    
    def __init__(self, name: str = "extrato2ofx"):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Configura o logger com as configurações definidas."""
        self.logger.setLevel(getattr(logging, LOG_CONFIG['level']))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                LOG_CONFIG['format'],
                datefmt=LOG_CONFIG['date_format']
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def info(self, message: str) -> None:
        """Log de informação."""
        self.logger.info(message)
    
    def error(self, message: str) -> None:
        """Log de erro."""
        self.logger.error(message)
    
    def warning(self, message: str) -> None:
        """Log de aviso."""
        self.logger.warning(message)
    
    def debug(self, message: str) -> None:
        """Log de debug."""
        self.logger.debug(message) 