# Convert PDF to OFX

Sistema completo para conversão de extratos bancários em PDF para OFX com categorização inteligente e análise de transações.

## 🚀 Funcionalidades

- **Conversão PDF → OFX**: Suporte para múltiplos bancos (Itaú, Mercado Pago, Nubank, PagSeguro)
- **Categorização Inteligente**: Sistema baseado em palavras-chave com aprendizado automático
- **Análise de Transações**: Extração e análise de transações não categorizadas
- **Sugestão de Categorias**: IA para sugerir categorias para transações "Outros"
- **Geração de Relatórios**: CSVs detalhados com estatísticas e análises
- **Formato Padronizado**: FITIDs únicos no formato `trans_XXX_YYYYMMDD`

## 📋 Pré-requisitos

- Python 3.8+
- pip
- Git

## 🛠️ Instalação

```bash
# Clone o repositório
git clone <repository-url>
cd convert_pdf_to_ofx

# Crie um ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto

```
convert_pdf_to_ofx/
├── pdfs/                    # PDFs de entrada
├── ofxs_gerados/           # OFXs convertidos
├── ofxs_categorizados/     # OFXs com categorias
├── csv_reports/            # Relatórios CSV
├── temp/                   # Arquivos temporários
├── parsers/                # Parsers específicos por banco
├── writers/                # Writers para diferentes formatos
├── services/               # Serviços de categorização
└── keywords.json           # Configuração de palavras-chave
```

## 🎯 Como Usar

### 1. Conversão de PDFs para OFX

```bash
# Coloque seus PDFs em pdfs/
python main.py
```

**Resultado**: Arquivos `.ofx` gerados em `ofxs_gerados/`

### 2. Categorização Inteligente

```bash
# Categoriza automaticamente todas as transações
python categorize_smart.py
```

**Resultado**: Arquivos OFX categorizados em `ofxs_categorizados/`

### 3. Análise de Transações "Outros"

```bash
# Extrai transações não categorizadas
python extract_outros.py
```

**Resultado**: `csv_reports/transacoes_outros.csv`

### 4. Sugestão de Categorias

```bash
# Analisa e sugere categorias para transações "Outros"
python suggest_categories.py
```

**Resultado**: `csv_reports/transacoes_outros_sugeridas.csv`

### 5. Melhoria da Categorização

```bash
# Extrai palavras-chave automaticamente
python extract_keywords.py

# Testa a categorização
python test_categorization.py

# Melhora categorização existente
python improve_categorization.py
```

## 📊 Relatórios Gerados

### CSV de Transações "Outros"
- **Arquivo**: `csv_reports/transacoes_outros.csv`
- **Colunas**: `fitid`, `description`, `category`, `amount`, `date`, `file`
- **Formato FITID**: `trans_001_20250117`

### CSV com Sugestões de Categorias
- **Arquivo**: `csv_reports/transacoes_outros_sugeridas.csv`
- **Colunas**: `fitid`, `description`, `category`, `amount`, `date`, `file`, `suggested_category`

## 🔧 Configuração

### Palavras-chave Personalizadas

Edite `keywords.json` para adicionar novas categorias e palavras-chave:

```json
{
  "Alimentação": [
    "restaurante",
    "ifood",
    "rappi",
    "uber eats"
  ],
  "Transporte": [
    "uber",
    "99",
    "combustível",
    "estacionamento"
  ]
}
```

### Prioridades de Categorias

Ajuste `CATEGORY_PRIORITIES` em `keyword_config.py` para definir a ordem de prioridade das categorias.

## 🏦 Bancos Suportados

- **Itaú**: Extratos completos com todas as transações
- **Mercado Pago**: Transações de pagamento e transferências
- **Nubank**: Extratos detalhados com categorização
- **PagSeguro**: Transações de pagamento digital

## 📈 Estatísticas e Análises

O sistema gera estatísticas detalhadas incluindo:

- Total de transações por categoria
- Percentual de transações categorizadas vs "Outros"
- Valor total e médio por categoria
- Distribuição temporal das transações
- Eficácia da categorização

## 🔍 Debugging e Testes

```bash
# Testa a categorização
python test_categorization.py

# Verifica logs detalhados
tail -f logs/app.log
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para dúvidas ou problemas:

1. Verifique os logs em `logs/`
2. Execute `python test_categorization.py` para diagnosticar problemas
3. Abra uma issue no GitHub

## 🔄 Atualizações Recentes

- ✅ Formato FITID padronizado: `trans_XXX_YYYYMMDD`
- ✅ Criação automática de diretórios
- ✅ Melhor tratamento de erros
- ✅ Logs estruturados
- ✅ Relatórios CSV aprimorados
- ✅ Sugestão inteligente de categorias 