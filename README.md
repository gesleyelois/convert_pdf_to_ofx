# convert_pdf_to_ofx

Conversor de extratos bancários em PDF para formato OFX com **categorização inteligente por palavras-chave**.

## 🚀 Características

- ✅ **Suporte a múltiplos bancos**: Itaú, Mercado Pago e outros
- ✅ **Conversão automática**: Detecta o banco automaticamente
- ✅ **Formato OFX**: Compatível com softwares de gestão financeira
- ✅ **Categorização inteligente**: Sistema de palavras-chave otimizado para o contexto brasileiro
- ✅ **Configurável**: Fácil personalização de categorias e palavras-chave
- ✅ **Logs detalhados**: Acompanhe todo o processo de conversão

## 🏦 Bancos Suportados

- **Itaú**: Extratos em PDF
- **Mercado Pago**: Extratos em PDF
- **Nubank**: Extratos em PDF
- **PagSeguro**: Extratos em PDF
- **Outros**: Estrutura extensível para novos bancos

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

## 🚀 Como Usar

### 1. Conversão de PDF para OFX

#### Prepare seus PDFs
Coloque os extratos bancários em PDF na pasta `pdfs/`:
```
pdfs/
├── extrato_itau.pdf
├── extrato_mercadopago.pdf
└── outros_extratos.pdf
```

#### Execute o conversor
```bash
python main.py
```

#### Acesse os arquivos OFX gerados
Os arquivos convertidos estarão na pasta `ofxs_gerados/`:
```
ofxs_gerados/
├── extrato_itau.ofx
├── extrato_mercadopago.ofx
└── outros_extratos.ofx
```

### 2. Categorização Inteligente de OFX

#### Execute a categorização
```bash
python categorize_smart.py
```

#### Teste o sistema de categorização
```bash
python categorize_smart.py --test
```

#### Acesse os arquivos OFX categorizados
Os arquivos categorizados estarão na pasta `ofxs_categorizados/`:
```
ofxs_categorizados/
├── categorizado_extrato_itau.ofx
├── categorizado_extrato_mercadopago.ofx
└── categorizado_outros_extratos.ofx
```

## 📊 Exemplos de Uso

### Exemplo 1: Processamento Completo
```bash
# 1. Converta PDFs para OFX
python main.py

# 2. Categorize os OFXs gerados
python categorize_smart.py

# 3. Verifique os resultados
ls ofxs_categorizados/
```

### Exemplo 2: Teste do Sistema
```bash
# Teste a precisão do categorizador
python categorize_smart.py --test
```

### Exemplo 3: Personalização
```bash
# 1. Edite as palavras-chave
nano keyword_config.py

# 2. Execute novamente
python categorize_smart.py
```

## 🧠 Sistema de Categorização Inteligente

### Como Funciona

O sistema usa um **categorizador inteligente baseado em palavras-chave** otimizado para o contexto bancário brasileiro:

1. **Leitura dos OFXs**: O sistema lê todos os arquivos OFX da pasta `ofxs_gerados/`
2. **Análise das transações**: Extrai descrições e valores das transações
3. **Categorização por palavras-chave**: Usa regras hierárquicas e contexto para categorizar
4. **Geração de relatórios**: Cria arquivos com estatísticas detalhadas por categoria

### 🔄 Processo de Melhoria da Categorização

O sistema inclui um **processo automatizado de melhoria** que permite identificar e corrigir transações não categorizadas:

#### Processo Completo (Recomendado)
```bash
# Executa todo o processo de melhoria automaticamente
python improve_categorization.py
```

#### Processo Passo a Passo
```bash
# 1. Categorizar arquivos OFX
python categorize_smart.py

# 2. Extrair transações classificadas como "Outros"
python extract_outros.py

# 3. Analisar e sugerir categorias
python suggest_categories.py

# 4. Extrair palavras-chave das sugestões
python extract_keywords.py
```

#### Executar Passo Específico
```bash
# Apenas extrair transações "Outros"
python improve_categorization.py --step 2

# Apenas sugerir categorias
python improve_categorization.py --step 3
```

#### Arquivos Gerados
- `csv_reports/transacoes_outros.csv` - Transações não categorizadas
- `csv_reports/transacoes_outros_sugeridas.csv` - Transações com categorias sugeridas

#### Próximos Passos Após a Análise
1. **Analise o arquivo** `csv_reports/transacoes_outros_sugeridas.csv`
2. **Atualize** `keyword_config.py` com as sugestões apropriadas
3. **Teste as melhorias** com `python test_new_categories.py`
4. **Reexecute o processo** se necessário

### Categorias Disponíveis

- **Alimentação**: Restaurantes, lanches, supermercados, delivery
- **Transporte**: Uber, combustível, estacionamento, transporte público
- **Saúde**: Farmácias, consultas médicas, exames, planos de saúde
- **Educação**: Escolas, cursos, material escolar, universidades
- **Lazer**: Cinema, shows, streaming, esportes, viagens
- **Moradia**: Aluguel, contas de casa, energia, água, internet
- **Vestuário**: Roupas, calçados, acessórios, higiene pessoal
- **Serviços**: Bancos, seguros, impostos, serviços profissionais
- **Investimentos**: Aplicações, rendimentos, corretoras
- **Transferências**: PIX, TED, DOC, transferências bancárias
- **Reservas**: Reservas automáticas do MercadoPago e outros sistemas
- **Impostos**: IPVA, licenciamento, taxas governamentais
- **Salário**: Remunerações, benefícios, comissões
- **Compras Variadas**: Compras online e gerais
- **Outros**: Transações não categorizadas

### Configuração Personalizada

O sistema é totalmente configurável através do arquivo `keyword_config.py`:

#### Adicionar novas palavras-chave:
```python
CATEGORY_KEYWORDS = {
    "Alimentação": [
        "ifood", "rappi", "uber eats", "mcdonalds", "padaria",
        # Adicione suas palavras-chave aqui
    ],
    # Adicione novas categorias aqui
}
```

#### Ajustar prioridades:
```python
CATEGORY_PRIORITIES = {
    "Alimentação": 10,  # Alta prioridade
    "Transporte": 10,
    "Outros": 0,        # Baixa prioridade
}
```

#### Configurar regras baseadas em valores:
```python
VALUE_BASED_RULES = {
    "high_value_threshold": 1000,  # Valores acima de R$ 1000
    "low_value_threshold": 50,      # Valores abaixo de R$ 50
    "investment_threshold": 5000,   # Valores acima de R$ 5000 são investimentos
}
```

### Eficácia da Categorização

O sistema mostra estatísticas detalhadas incluindo:
- **Total de transações processadas**
- **Distribuição por categoria**
- **Porcentagem de transações em "Outros"**
- **Avaliação da eficácia** (Excelente: <30% em Outros, Bom: <50% em Outros)

## 🧪 Testes

### Teste do Sistema de Categorização
```bash
# Teste básico do categorizador
python test_categorization.py

# Teste das novas categorias adicionadas
python test_new_categories.py
```

### Teste da Categorização por Tipo
```bash
# Testa se o sistema respeita o tipo de transação (débito/crédito)
python categorize_smart.py --test
```

## 📁 Estrutura do Projeto

```
convert_pdf_to_ofx/
├── pdfs/                    # PDFs dos extratos bancários
├── ofxs_gerados/           # OFXs convertidos
├── ofxs_categorizados/     # OFXs categorizados
├── csv_reports/            # Relatórios CSV de análise
│   ├── transacoes_outros.csv
│   └── transacoes_outros_sugeridas.csv
├── services/               # Serviços do sistema
│   ├── smart_keyword_categorizer.py  # Categorizador inteligente
│   ├── logger.py           # Sistema de logs
│   └── ...
├── parsers/                # Parsers para diferentes bancos
├── writers/                # Writers para diferentes formatos
├── keyword_config.py       # Configuração de palavras-chave
├── categorize_smart.py     # Script principal de categorização
├── improve_categorization.py # Processo automatizado de melhoria
├── extract_outros.py       # Extração de transações "Outros"
├── suggest_categories.py   # Sugestões de categorias
├── extract_keywords.py     # Extração de palavras-chave
├── test_categorization.py  # Teste básico do categorizador
├── test_new_categories.py  # Teste das novas categorias
├── main.py                 # Script principal de conversão
└── requirements.txt        # Dependências do projeto
```

## 🔧 Troubleshooting

### Problemas Comuns

#### Erro: "Nenhum arquivo PDF válido encontrado"
- **Solução**: Verifique se os PDFs estão na pasta `pdfs/`
- **Verificação**: `ls pdfs/`

#### Erro: "Nenhum arquivo OFX encontrado"
- **Solução**: Execute primeiro `python main.py` para gerar os OFXs
- **Verificação**: `ls ofxs_gerados/`

#### Erro de encoding nos arquivos OFX
- **Solução**: O sistema tenta automaticamente diferentes encodings
- **Verificação**: Verifique se o arquivo OFX não está corrompido

#### Baixa precisão na categorização
- **Solução**: Adicione palavras-chave específicas no `keyword_config.py`
- **Verificação**: Execute `python categorize_smart.py --test`

### Logs e Diagnóstico

O sistema gera logs detalhados. Para ver mais informações:
```bash
# Ver logs em tempo real
python main.py 2>&1 | tee log.txt

# Ver logs de categorização
python categorize_smart.py 2>&1 | tee categorization_log.txt
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para dúvidas ou problemas:
1. Consulte este README
2. Abra uma issue no repositório
3. Consulte os logs para diagnóstico 