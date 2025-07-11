"""
Serviço de identificação de bancos.
Seguindo o princípio de Single Responsibility.
"""

from typing import Optional, Dict, Type
from interfaces import BankParser
from parsers.itau import ItauParser
from parsers.mercadopago import MercadoPagoParser

class BankIdentifier:
    """Identifica qual parser usar baseado no nome do arquivo."""
    
    def __init__(self):
        self._parsers: Dict[str, Type[BankParser]] = {
            'itau': ItauParser,
            'mercadopago': MercadoPagoParser,
        }
    
    def identify_bank(self, file_name: str) -> Optional[str]:
        """
        Identifica o banco baseado no nome do arquivo.
        
        Args:
            file_name: Nome do arquivo PDF
            
        Returns:
            Nome do banco identificado ou None se não encontrado
        """
        file_name_lower = file_name.lower()
        
        for bank_name in self._parsers.keys():
            if bank_name in file_name_lower:
                return bank_name
        
        return None
    
    def get_parser(self, bank_name: str) -> Optional[BankParser]:
        """
        Retorna a instância do parser para o banco especificado.
        
        Args:
            bank_name: Nome do banco
            
        Returns:
            Instância do parser ou None se não encontrado
        """
        parser_class = self._parsers.get(bank_name)
        if parser_class:
            return parser_class()
        return None
    
    def get_available_banks(self) -> list[str]:
        """Retorna lista de bancos disponíveis."""
        return list(self._parsers.keys())
    
    def register_parser(self, bank_name: str, parser_class: Type[BankParser]) -> None:
        """
        Registra um novo parser.
        
        Args:
            bank_name: Nome do banco
            parser_class: Classe do parser
        """
        self._parsers[bank_name] = parser_class 