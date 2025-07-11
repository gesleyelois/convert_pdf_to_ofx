"""
Parser para extratos do Itaú.
"""

import re
from parsers.base_parser import BaseParser
from interfaces import Transaction, AccountData

class ItauParser(BaseParser):
    def __init__(self):
        super().__init__('itau')
    
    def parse(self, file_path: str):
        text = self._extract_text_from_pdf(file_path)
        transactions = self._parse_transactions(text)
        account_data = self._create_account_data()
        return transactions, account_data
    
    def _parse_transactions(self, text: str):
        transactions = []
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines:
            transaction = self._parse_transaction_line(line)
            if transaction:
                transactions.append(transaction)
        return transactions
    
    def _parse_transaction_line(self, line: str):
        match = re.search(
            r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+(-?[\d.,]+)$', 
            line
        )
        if not match:
            return None
        date_str, description, value_str = match.groups()
        description = description.strip()
        if 'saldo do dia' in description.lower():
            return None
        try:
            amount = self._parse_amount(value_str)
            transaction_type = 'saída' if amount < 0 else 'entrada'
            amount = self._normalize_amount(amount, transaction_type)
            date_iso = self._convert_date_to_iso(date_str)
            trntype = self._determine_trntype(transaction_type)
            return Transaction(
                date=date_iso,
                amount=amount,
                description=description,
                transaction_type=transaction_type,
                trntype=trntype
            )
        except (ValueError, TypeError):
            return None
    
    def _parse_amount(self, amount_str: str) -> float:
        clean_amount = amount_str.replace('.', '').replace(',', '.')
        return float(clean_amount) 