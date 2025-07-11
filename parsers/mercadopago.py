"""
Parser para extratos do Mercado Pago.
"""

import re
from typing import List
from parsers.base_parser import BaseParser
from interfaces import Transaction, AccountData

class MercadoPagoParser(BaseParser):
    def __init__(self):
        super().__init__('mercadopago')
    
    def parse(self, file_path: str):
        text = self._extract_text_from_pdf(file_path)
        transactions = self._parse_transactions(text)
        account_data = self._create_account_data()
        return transactions, account_data
    
    def _parse_transactions(self, text: str):
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        transaction_lines = self._extract_transaction_lines(lines)
        transactions = []
        for line in transaction_lines:
            transaction = self._parse_transaction_line(line)
            if transaction:
                transactions.append(transaction)
        return transactions
    
    def _extract_transaction_lines(self, lines: List[str]) -> List[str]:
        transaction_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if self._is_header_line(line):
                i += 1
                continue
            if re.search(r'\d{2}-\d{2}-\d{4}.*R\$\s*-?[\d.,]+', line):
                transaction_lines.append(line)
                i += 1
            elif re.search(r'R\$\s*-?[\d.,]+', line) and not re.match(r'\d{2}-\d{2}-\d{4}', line):
                if transaction_lines:
                    transaction_lines[-1] += ' ' + line
                i += 1
            elif (not re.match(r'\d{2}-\d{2}-\d{4}', line) and 
                  not re.search(r'R\$\s*-?[\d.,]+', line) and
                  not line.startswith('1/') and
                  not line.startswith('Data Descrição')):
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if (re.search(r'\d{2}-\d{2}-\d{4}.*R\$\s*-?[\d.,]+', next_line) or
                        re.search(r'\d{2}-\d{2}-\d{4}.*\d+.*R\$\s*-?[\d.,]+', next_line)):
                        transaction_lines.append(line + ' ' + next_line)
                        i += 2
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        return transaction_lines
    
    def _is_header_line(self, line: str) -> bool:
        header_patterns = [
            'Data Descrição',
            '1/',
            'EXTRATO DE CONTA',
            'CPF/CNPJ:',
            'Periodo:',
            'Entradas:',
            'Saldo inicial:',
            'Saidas:',
            'DETALHE DOS MOVIMENTOS'
        ]
        return any(line.startswith(pattern) for pattern in header_patterns)
    
    def _parse_transaction_line(self, line: str):
        match = re.search(
            r'(\d{2}-\d{2}-\d{4})\s+(.+?)\s+(\d+)\s+R\$\s*(-?[\d.,]+)', 
            line
        )
        if not match:
            return None
        date_str, description, id_str, value_str = match.groups()
        description = description.strip()
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