"""
Escritor de arquivos OFX categorizados (XML).
Seguindo o princípio de Single Responsibility.
"""

from typing import List
from datetime import datetime
from interfaces import CategorizedOFXWriter, CategorizedTransaction, AccountData
from config import OFX_CONFIG

class CategorizedOFXWriterImpl(CategorizedOFXWriter):
    """Implementação do escritor de OFX categorizado (XML)."""
    
    def write(self, transactions: List[CategorizedTransaction], account_data: AccountData, output_path: str) -> None:
        """
        Escreve as transações categorizadas em formato OFX XML.
        """
        ofx_content = self._generate_ofx_header()
        ofx_content += self._generate_sign_on_message()
        ofx_content += self._generate_bank_message(transactions, account_data)
        ofx_content += "</OFX>\n"
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(ofx_content)

    def _generate_ofx_header(self) -> str:
        """Gera o cabeçalho OFX XML."""
        return f'''<?xml version="1.0" encoding="UTF-8"?>\n<OFX>\n'''

    def _generate_sign_on_message(self) -> str:
        """Gera a mensagem de sign-on."""
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        return f'''  <SIGNONMSGSRSV1>\n    <SONRS>\n      <STATUS>\n        <CODE>0</CODE>\n        <SEVERITY>INFO</SEVERITY>\n      </STATUS>\n      <DTSERVER>{current_time}[0:GMT]</DTSERVER>\n      <LANGUAGE>{OFX_CONFIG['language']}</LANGUAGE>\n      <FI>\n        <ORG>CATEGORIZED OFX</ORG>\n        <FID>CAT</FID>\n      </FI>\n    </SONRS>\n  </SIGNONMSGSRSV1>\n'''

    def _generate_bank_message(self, transactions: List[CategorizedTransaction], account_data: AccountData) -> str:
        if not transactions:
            return ""
        dates = [t.date for t in transactions]
        start_date = min(dates)
        end_date = max(dates)
        start_date_formatted = f"{start_date}000000[-3:BRT]"
        end_date_formatted = f"{end_date}000000[-3:BRT]"
        transactions_xml = ""
        for i, transaction in enumerate(transactions):
            transactions_xml += self._generate_transaction_xml(transaction, i + 1)
        return f'''  <BANKMSGSRSV1>\n    <STMTTRNRS>\n      <TRNUID>1</TRNUID>\n      <STATUS>\n        <CODE>0</CODE>\n        <SEVERITY>INFO</SEVERITY>\n      </STATUS>\n      <STMTRS>\n        <CURDEF>{OFX_CONFIG['currency']}</CURDEF>\n        <BANKACCTFROM>\n          <BANKID>{account_data.bank_id}</BANKID>\n          <BRANCHID>{account_data.agency}</BRANCHID>\n          <ACCTID>{account_data.account}</ACCTID>\n          <ACCTTYPE>{OFX_CONFIG['account_type']}</ACCTTYPE>\n        </BANKACCTFROM>\n        <BANKTRANLIST>\n          <DTSTART>{start_date_formatted}</DTSTART>\n          <DTEND>{end_date_formatted}</DTEND>\n{transactions_xml}        </BANKTRANLIST>\n      </STMTRS>\n    </STMTTRNRS>\n  </BANKMSGSRSV1>\n'''

    def _generate_transaction_xml(self, transaction: CategorizedTransaction, index: int) -> str:
        date_formatted = f"{transaction.date}000000[-3:BRT]"
        amount_formatted = f"{transaction.amount:.2f}"
        date_obj = datetime.strptime(transaction.date, "%Y%m%d")
        date_str = date_obj.strftime('%Y%m%d')
        fitid = f"trans_{index:03d}_{date_str}"
        memo_with_category = f"{transaction.description} [CATEGORIA: {transaction.category}]"
        return f'''            <STMTTRN>\n              <TRNTYPE>{transaction.trntype}</TRNTYPE>\n              <DTPOSTED>{date_formatted}</DTPOSTED>\n              <TRNAMT>{amount_formatted}</TRNAMT>\n              <FITID>{fitid}</FITID>\n              <MEMO>{memo_with_category}</MEMO>\n            </STMTTRN>\n''' 