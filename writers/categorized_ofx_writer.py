"""
Escritor de arquivos OFX categorizados.
Seguindo o princípio de Single Responsibility.
"""

from typing import List
from datetime import datetime
from interfaces import CategorizedOFXWriter, CategorizedTransaction, AccountData
from config import OFX_CONFIG

class CategorizedOFXWriterImpl(CategorizedOFXWriter):
    """Implementação do escritor de OFX categorizado."""
    
    def write(self, transactions: List[CategorizedTransaction], account_data: AccountData, output_path: str) -> None:
        """
        Escreve as transações categorizadas em formato OFX.
        
        Args:
            transactions: Lista de transações categorizadas
            account_data: Dados da conta bancária
            output_path: Caminho do arquivo de saída
        """
        ofx_content = self._generate_ofx_header()
        ofx_content += self._generate_sign_on_message()
        ofx_content += self._generate_bank_message(transactions, account_data)
        ofx_content += "</OFX>"
        
        # Escrever arquivo
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(ofx_content)
    
    def _generate_ofx_header(self) -> str:
        """Gera o cabeçalho OFX."""
        return f"""OFXHEADER:100
DATA:OFXSGML
VERSION:{OFX_CONFIG['version']}
SECURITY:{OFX_CONFIG['security']}
ENCODING:{OFX_CONFIG['encoding']}
CHARSET:{OFX_CONFIG['charset']}
COMPRESSION:{OFX_CONFIG['compression']}
OLDFILEUID:NONE
NEWFILEUID:NONE
<OFX>
"""
    
    def _generate_sign_on_message(self) -> str:
        """Gera a mensagem de sign-on."""
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"""<SIGNONMSGSRSV1>
<SONRS>
<STATUS>
<CODE>0</CODE>
<SEVERITY>INFO</SEVERITY>
</STATUS>
<DTSERVER>{current_time}[0:GMT]</DTSERVER>
<LANGUAGE>{OFX_CONFIG['language']}
<FI>
<ORG>CATEGORIZED OFX</ORG>
<FID>CAT</FID>
</FI>
</SONRS>
</SIGNONMSGSRSV1>
"""
    
    def _generate_bank_message(self, transactions: List[CategorizedTransaction], account_data: AccountData) -> str:
        """Gera a mensagem bancária com transações categorizadas."""
        if not transactions:
            return ""
        
        # Encontrar datas de início e fim
        dates = [t.date for t in transactions]
        start_date = min(dates)
        end_date = max(dates)
        
        # Formatar datas para OFX
        start_date_formatted = f"{start_date}000000[-3:BRT]"
        end_date_formatted = f"{end_date}000000[-3:BRT]"
        
        # Gerar transações
        transactions_xml = ""
        for i, transaction in enumerate(transactions):
            transactions_xml += self._generate_transaction_xml(transaction, i + 1)
        
        return f"""<BANKMSGSRSV1>
<STMTTRNRS>
<TRNUID>1</TRNUID>
<STATUS>
<CODE>0</CODE>
<SEVERITY>INFO</SEVERITY>
</STATUS>
<STMTRS>
<CURDEF>{OFX_CONFIG['currency']}
<BANKACCTFROM>
<BANKID>{account_data.bank_id}
<BRANCHID>{account_data.agency}
<ACCTID>{account_data.account}
<ACCTTYPE>{OFX_CONFIG['account_type']}
</BANKACCTFROM>
<BANKTRANLIST>
<DTSTART>{start_date_formatted}
<DTEND>{end_date_formatted}
{transactions_xml}</BANKTRANLIST>
</STMTRS>
</STMTTRNRS>
</BANKMSGSRSV1>
"""
    
    def _generate_transaction_xml(self, transaction: CategorizedTransaction, index: int) -> str:
        """Gera XML para uma transação individual."""
        # Formatar data para OFX
        date_formatted = f"{transaction.date}000000[-3:BRT]"
        
        # Formatar valor
        amount_formatted = f"{transaction.amount:.2f}"
        
        # Criar ID único
        fitid = f"cat_trans_{index:03d}_{transaction.date}"
        
        # Adicionar categoria ao memo
        memo_with_category = f"{transaction.description} [CATEGORIA: {transaction.category}]"
        
        return f"""<STMTTRN>
<TRNTYPE>{transaction.trntype}
<DTPOSTED>{date_formatted}
<TRNAMT>{amount_formatted}
<FITID>{fitid}
<MEMO>{memo_with_category}
</STMTTRN>
""" 