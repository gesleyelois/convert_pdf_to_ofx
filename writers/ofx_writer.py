"""
Escritor OFX.
"""

import datetime
from interfaces import OFXWriter, Transaction, AccountData
from config import OFX_CONFIG

class OFXWriterRefactored(OFXWriter):
    def write(self, transactions, account_data, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            self._write_header(f)
            self._write_sign_on(f)
            self._write_bank_message(f, transactions, account_data)
            f.write("</OFX>")
    
    def _write_header(self, file):
        file.write("OFXHEADER:100\n")
        file.write("DATA:OFXSGML\n")
        file.write(f"VERSION:{OFX_CONFIG['version']}\n")
        file.write(f"SECURITY:{OFX_CONFIG['security']}\n")
        file.write(f"ENCODING:{OFX_CONFIG['encoding']}\n")
        file.write(f"CHARSET:{OFX_CONFIG['charset']}\n")
        file.write(f"COMPRESSION:{OFX_CONFIG['compression']}\n")
        file.write("OLDFILEUID:NONE\n")
        file.write("NEWFILEUID:NONE\n")
        file.write("<OFX>\n")
    
    def _write_sign_on(self, file):
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file.write("<SIGNONMSGSRSV1>\n")
        file.write("<SONRS>\n")
        file.write("<STATUS>\n")
        file.write("<CODE>0</CODE>\n")
        file.write("<SEVERITY>INFO</SEVERITY>\n")
        file.write("</STATUS>\n")
        file.write(f"<DTSERVER>{current_time}{OFX_CONFIG['gmt_timezone']}</DTSERVER>\n")
        file.write(f"<LANGUAGE>{OFX_CONFIG['language']}\n")
        file.write("<FI>\n")
        file.write("<ORG>NU PAGAMENTOS S.A.</ORG>\n")
        file.write("<FID>260</FID>\n")
        file.write("</FI>\n")
        file.write("</SONRS>\n")
        file.write("</SIGNONMSGSRSV1>\n")
    
    def _write_bank_message(self, file, transactions, account_data):
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        dt_start, dt_end = self._calculate_date_range(transactions)
        file.write("<BANKMSGSRSV1>\n")
        file.write("<STMTTRNRS>\n")
        file.write("<TRNUID>1</TRNUID>\n")
        file.write("<STATUS>\n")
        file.write("<CODE>0</CODE>\n")
        file.write("<SEVERITY>INFO</SEVERITY>\n")
        file.write("</STATUS>\n")
        file.write("<STMTRS>\n")
        file.write(f"<CURDEF>{OFX_CONFIG['currency']}\n")
        self._write_bank_account_from(file, account_data)
        self._write_bank_transaction_list(file, transactions, dt_start, dt_end)
        self._write_ledger_balance(file, current_time)
        self._write_balance_list(file, current_time)
        file.write("</STMTRS>\n")
        file.write("</STMTTRNRS>\n")
        file.write("</BANKMSGSRSV1>\n")
    
    def _write_bank_account_from(self, file, account_data):
        file.write("<BANKACCTFROM>\n")
        file.write(f"<BANKID>{account_data.bank_id}\n")
        file.write(f"<BRANCHID>{account_data.agency}\n")
        file.write(f"<ACCTID>{account_data.account}\n")
        file.write(f"<ACCTTYPE>{OFX_CONFIG['account_type']}\n")
        file.write("</BANKACCTFROM>\n")
    
    def _write_bank_transaction_list(self, file, transactions, dt_start, dt_end):
        file.write("<BANKTRANLIST>\n")
        file.write(f"<DTSTART>{dt_start}\n")
        file.write(f"<DTEND>{dt_end}\n")
        for i, transaction in enumerate(transactions, 1):
            self._write_transaction(file, transaction, i)
        file.write("</BANKTRANLIST>\n")
    
    def _write_transaction(self, file, transaction, index):
        file.write("<STMTTRN>\n")
        file.write(f"<TRNTYPE>{transaction.trntype}\n")
        file.write(f"<DTPOSTED>{transaction.date}000000{OFX_CONFIG['timezone']}\n")
        file.write(f"<TRNAMT>{transaction.amount:.2f}\n")
        file.write(f"<FITID>trans_{index:03d}_{transaction.date}\n")
        file.write(f"<MEMO>{transaction.description}\n")
        file.write("</STMTTRN>\n")
    
    def _write_ledger_balance(self, file, current_time):
        file.write("<LEDGERBAL>\n")
        file.write("<BALAMT>0.37\n")
        file.write(f"<DTASOF>{current_time}{OFX_CONFIG['gmt_timezone']}\n")
        file.write("</LEDGERBAL>\n")
    
    def _write_balance_list(self, file, current_time):
        file.write("<BALLIST>\n")
        file.write("<BAL>\n")
        file.write("<BALTYPE>AVAIL\n")
        file.write("<BALAMT>0.37\n")
        file.write(f"<DTASOF>{current_time}{OFX_CONFIG['gmt_timezone']}\n")
        file.write("</BAL>\n")
        file.write("</BALLIST>\n")
    
    def _calculate_date_range(self, transactions):
        if not transactions:
            return "20250101000000[-3:BRT]", "20250101000000[-3:BRT]"
        dates = [t.date for t in transactions]
        dt_start = min(dates) + "000000[-3:BRT]"
        dt_end = max(dates) + "000000[-3:BRT]"
        return dt_start, dt_end 