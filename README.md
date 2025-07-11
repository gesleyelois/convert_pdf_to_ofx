# convert_pdf_to_ofx

Conversor de extratos bancários em PDF para formato OFX.

## 🚀 Características

- ✅ **Suporte a múltiplos bancos**: Itaú, Mercado Pago e outros
- ✅ **Conversão automática**: Detecta o banco automaticamente
- ✅ **Formato OFX**: Compatível com softwares de gestão financeira
- ✅ **Configurável**: Fácil personalização para novos bancos
- ✅ **Logs detalhados**: Acompanhe todo o processo de conversão

## 🛠️ Instalação

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd convert_pdf_to_ofx
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## 💡 Usando ambiente virtual (opcional, mas recomendado)

Para evitar conflitos de dependências com outros projetos Python, recomenda-se usar um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # No Linux/Mac
# ou
.venv\Scripts\activate   # No Windows
pip install -r requirements.txt
```

Depois, rode normalmente:

```bash
python main.py
```

## 🚀 Como Usar

### 1. Prepare seus PDFs
Coloque os extratos bancários em PDF na pasta `pdfs/`:
```
pdfs/
├── extrato_itau.pdf
├── extrato_mercadopago.pdf
└── outros_extratos.pdf
```

### 2. Execute o conversor
```bash
python main.py
```

### 3. Acesse os arquivos OFX gerados
Os arquivos convertidos estarão na pasta `ofxs_gerados/`:
```
ofxs_gerados/
├── extrato_itau.ofx
├── extrato_mercadopago.ofx
└── outros_extratos.ofx
```

## 📝 Logs de Execução

Durante a conversão, você verá logs como:
```
[INFO] Diretórios configurados com sucesso
[INFO] Iniciando conversão de PDFs em OFX...
[INFO] Encontrados 3 arquivos PDF para processar
[INFO] Processando extrato_itau.pdf (itau)...
[INFO] extrato_itau.pdf convertido com sucesso! Total de transações: 15
[INFO] Processamento concluído: 3 sucessos, 0 falhas
[INFO] Conversão concluída. Arquivos OFX gerados em: ofxs_gerados
```

## 🔧 Configuração

### Adicionando um Novo Banco

1. **Crie um novo parser:**
```python
# parsers/novo_banco.py
from parsers.base_parser import BaseParser
from interfaces import Transaction, AccountData

class NovoBancoParser(BaseParser):
    def __init__(self):
        super().__init__('novo_banco')
    
    def parse(self, file_path: str) -> tuple[List[Transaction], AccountData]:
        # Implementação específica do banco
        pass
```

2. **Registre o parser:**
```python
# services/bank_identifier.py
from parsers.novo_banco import NovoBancoParser

class BankIdentifier:
    def __init__(self):
        self._parsers = {
            # ... parsers existentes
            'novo_banco': NovoBancoParser,
        }
```

3. **Adicione a configuração:**
```python
# config.py
BANK_CONFIGS = {
    # ... configurações existentes
    'novo_banco': {
        'name': 'Novo Banco',
        'agency': '1234',
        'account': '56789-0',
        'bank_id': '0123',
        'org': 'NOVO BANCO S.A.',
        'fid': '123'
    }
}
```

## 📁 Estrutura do Projeto

```
convert_pdf_to_ofx/
├── config.py                 # Configurações centralizadas
├── interfaces.py             # Interfaces e tipos
├── main.py                  # Aplicação principal
├── requirements.txt          # Dependências
├── services/                 # Serviços especializados
├── parsers/                  # Parsers de bancos
├── writers/                  # Escritores de formato
├── pdfs/                     # PDFs de entrada
├── ofxs_gerados/            # OFXs de saída
└── temp/                    # Arquivos temporários
```

## 🧪 Testes

### Executar Testes (quando implementados)
```bash
pytest tests/
```

## 🤝 Contribuindo

1. **Fork o projeto**
2. **Crie uma branch para sua feature**
3. **Adicione testes**
4. **Faça commit das mudanças**
5. **Abra um Pull Request**

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para dúvidas ou problemas:
1. Consulte este README
2. Abra uma issue no repositório
3. Consulte os logs para diagnóstico 