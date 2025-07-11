"""
Interfaces e tipos para o projeto.
Seguindo o princípio de Dependency Inversion.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Protocol
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    """Representa uma transação bancária."""
    date: str  # Formato ISO: YYYYMMDD
    amount: float
    description: str
    transaction_type: str  # 'entrada' ou 'saída'
    trntype: str  # 'CREDIT' ou 'DEBIT'

@dataclass
class AccountData:
    """Representa dados da conta bancária."""
    bank_name: str
    agency: str
    account: str
    bank_id: str
    org: str
    fid: str

@dataclass
class ProcessingResult:
    """Resultado do processamento de um arquivo."""
    success: bool
    file_name: str
    bank_name: str
    transactions_count: int
    error_message: str = ""

class BankParser(ABC):
    """Interface para parsers de bancos."""
    
    @abstractmethod
    def can_parse(self, file_name: str) -> bool:
        """Verifica se o parser pode processar o arquivo."""
        pass
    
    @abstractmethod
    def parse(self, file_path: str) -> tuple[List[Transaction], AccountData]:
        """Processa o arquivo PDF e retorna transações e dados da conta."""
        pass

class OFXWriter(ABC):
    """Interface para escritores OFX."""
    
    @abstractmethod
    def write(self, transactions: List[Transaction], account_data: AccountData, output_path: str) -> None:
        """Escreve as transações em formato OFX."""
        pass

class FileProcessor(ABC):
    """Interface para processadores de arquivo."""
    
    @abstractmethod
    def process_file(self, file_path: str) -> ProcessingResult:
        """Processa um arquivo individual."""
        pass

class Logger(ABC):
    """Interface para logging."""
    
    @abstractmethod
    def info(self, message: str) -> None:
        """Log de informação."""
        pass
    
    @abstractmethod
    def error(self, message: str) -> None:
        """Log de erro."""
        pass
    
    @abstractmethod
    def warning(self, message: str) -> None:
        """Log de aviso."""
        pass

class FileValidator(ABC):
    """Interface para validação de arquivos."""
    
    @abstractmethod
    def is_valid_file(self, file_path: str) -> bool:
        """Verifica se o arquivo é válido para processamento."""
        pass 