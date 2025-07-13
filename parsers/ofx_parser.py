"""
Parser para arquivos OFX.
Seguindo o princípio de Single Responsibility.
"""

import re
from typing import List
from pathlib import Path
from interfaces import Transaction, AccountData

class OFXParserImpl:
    """Implementação do parser de arquivos OFX."""
    
    def parse(self, file_path: str) -> tuple[List[Transaction], AccountData]:
        """
        Processa o arquivo OFX e retorna transações e dados da conta.
        
        Args:
            file_path: Caminho para o arquivo OFX
            
        Returns:
            Tupla com lista de transações e dados da conta
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extrair dados da conta
        account_data = self._extract_account_data(content)
        
        # Extrair transações
        transactions = self._extract_transactions(content)
        
        return transactions, account_data
    
    def _extract_account_data(self, content: str) -> AccountData:
        """Extrai dados da conta do conteúdo OFX."""
        # Padrões para extrair dados da conta
        org_pattern = r'<ORG>([^<]+)</ORG>'
        fid_pattern = r'<FID>([^<]+)</FID>'
        bankid_pattern = r'<BANKID>([^<]+)</BANKID>'
        branchid_pattern = r'<BRANCHID>([^<]+)</BRANCHID>'
        acctid_pattern = r'<ACCTID>([^<]+)</ACCTID>'
        
        # Extrair valores
        org = re.search(org_pattern, content)
        fid = re.search(fid_pattern, content)
        bankid = re.search(bankid_pattern, content)
        branchid = re.search(branchid_pattern, content)
        acctid = re.search(acctid_pattern, content)
        
        return AccountData(
            bank_name=org.group(1) if org else "Banco",
            agency=branchid.group(1) if branchid else "",
            account=acctid.group(1) if acctid else "",
            bank_id=bankid.group(1) if bankid else "",
            org=org.group(1) if org else "",
            fid=fid.group(1) if fid else ""
        )
    
    def _extract_transactions(self, content: str) -> List[Transaction]:
        """Extrai transações do conteúdo OFX."""
        transactions = []
        
        # Padrão para encontrar blocos de transação - mais flexível
        transaction_pattern = r'<STMTTRN>.*?</STMTTRN>'
        transaction_blocks = re.findall(transaction_pattern, content, re.DOTALL)
        
        if not transaction_blocks:
            # Tentar padrão alternativo
            transaction_pattern = r'<STMTTRN>.*?<TRNTYPE>.*?</STMTTRN>'
            transaction_blocks = re.findall(transaction_pattern, content, re.DOTALL)
        
        for i, block in enumerate(transaction_blocks):
            try:
                transaction = self._parse_transaction_block(block, i + 1)
                if transaction:
                    transactions.append(transaction)
            except Exception as e:
                # Log error but continue processing other transactions
                print(f"Erro ao processar transação {i + 1}: {e}")
                continue
        
        return transactions
    
    def _parse_transaction_block(self, block: str, index: int) -> Transaction:
        """Processa um bloco de transação individual."""
        # Padrões para extrair dados da transação - mais flexíveis
        trntype_pattern = r'<TRNTYPE>([^<\n]+)'
        dtposted_pattern = r'<DTPOSTED>([^<\n]+)'
        trnamt_pattern = r'<TRNAMT>([^<\n]+)'
        memo_pattern = r'<MEMO>([^<\n]+)'
        fitid_pattern = r'<FITID>([^<\n]+)'
        
        # Extrair valores
        trntype = re.search(trntype_pattern, block)
        dtposted = re.search(dtposted_pattern, block)
        trnamt = re.search(trnamt_pattern, block)
        memo = re.search(memo_pattern, block)
        fitid = re.search(fitid_pattern, block)
        
        if not all([trntype, dtposted, trnamt]):
            raise ValueError(f"Dados obrigatórios não encontrados na transação {index}")
        
        # Processar tipo de transação
        transaction_type = "entrada" if trntype.group(1).strip() == "CREDIT" else "saída"
        
        # Processar data (formato OFX: YYYYMMDDHHMMSS)
        date_str = dtposted.group(1).strip()[:8]  # Pegar apenas YYYYMMDD
        
        # Processar valor
        amount = float(trnamt.group(1).strip())
        
        # Processar descrição
        description = memo.group(1).strip() if memo else f"Transação {index}"
        
        # Processar FITID
        fitid_str = fitid.group(1).strip() if fitid else ""
        
        return Transaction(
            date=date_str,
            amount=amount,
            description=description,
            transaction_type=transaction_type,
            trntype=trntype.group(1).strip(),
            fitid=fitid_str
        ) 