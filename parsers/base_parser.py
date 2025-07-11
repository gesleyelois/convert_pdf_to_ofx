"""
Parser base com funcionalidades comuns.
"""

from abc import ABC
from datetime import datetime
from interfaces import BankParser, Transaction, AccountData
from config import BANK_CONFIGS

class BaseParser(BankParser, ABC):
    def __init__(self, bank_name: str):
        self.bank_name = bank_name
        self.bank_config = BANK_CONFIGS.get(bank_name, {})
    
    def can_parse(self, file_name: str) -> bool:
        return self.bank_name.lower() in file_name.lower()
    
    def _create_account_data(self) -> AccountData:
        return AccountData(
            bank_name=self.bank_config.get('name', self.bank_name.title()),
            agency=self.bank_config.get('agency', ''),
            account=self.bank_config.get('account', ''),
            bank_id=self.bank_config.get('bank_id', ''),
            org=self.bank_config.get('org', ''),
            fid=self.bank_config.get('fid', '')
        )
    
    def _convert_date_to_iso(self, date_str: str) -> str:
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj.strftime('%Y%m%d')
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, '%d-%m-%Y')
                return date_obj.strftime('%Y%m%d')
            except ValueError:
                raise ValueError(f"Formato de data não reconhecido: {date_str}")
    
    def _normalize_amount(self, amount: float, transaction_type: str) -> float:
        if transaction_type == 'entrada':
            return abs(amount)
        else:
            return -abs(amount)
    
    def _determine_trntype(self, transaction_type: str) -> str:
        return 'CREDIT' if transaction_type == 'entrada' else 'DEBIT'
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text 