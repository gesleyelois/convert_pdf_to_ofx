# convert_pdf_to_ofx

Conversor de extratos bancários em PDF para OFX com categorização inteligente.

## Instalação

```bash
git clone <repository-url>
cd convert_pdf_to_ofx
pip install -r requirements.txt
```

> Recomenda-se usar ambiente virtual:  
> `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`

## Como Usar

### 1. Converter PDFs para OFX

- Coloque seus PDFs em `pdfs/`
- Execute:
  ```bash
  python main.py
  ```
- Os arquivos `.ofx` serão gerados em `ofxs_gerados/`

### 2. Categorizar OFXs

- Execute:
  ```bash
  python categorize_smart.py
  ```
- Os arquivos categorizados estarão em `ofxs_categorizados/`

### 3. Melhorar a Categorização

1. Extraia transações não categorizadas:
   ```bash
   python extract_outros.py
   ```
2. Sugira novas categorias:
   ```bash
   python suggest_categories.py
   ```
3. Extraia e atualize palavras-chave automaticamente:
   ```bash
   python extract_keywords.py
   ```
   > O arquivo `keywords.json` será atualizado.

4. Re-categorize:
   ```bash
   python categorize_smart.py
   ```

### 4. Personalização

- Edite manualmente o arquivo `keywords.json` para ajustar ou criar categorias e palavras-chave.
- Para ajustar prioridades, edite `CATEGORY_PRIORITIES` em `keyword_config.py`.

## Dicas

- Sempre execute `python extract_keywords.py` após sugerir novas categorias para atualizar o arquivo de palavras-chave.
- O sistema funciona para extratos Itaú, Mercado Pago, Nubank, PagSeguro e pode ser adaptado para outros bancos. 