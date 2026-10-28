# Trabalhos do CONBRATRI 2026: análise e dashboard

Organização, classificação e dashboard dos 44 trabalhos publicados no CONBRATRI 2026 (sessões 1 a 4 e sessão de pôster).

Abra [`dashboard/index.html`](dashboard/index.html) no navegador. O arquivo funciona offline; só a fonte Source Sans vem do Google Fonts.

## Conteúdo do repositório

| Caminho | O que é |
|---|---|
| `01_Sessao_1_…` a `05_Sessao_de_Poster/` | Trabalhos originais, baixados pelo `baixar_trabalhos.py` |
| `lista_trabalhos_e_links.csv` | Lista de trabalhos, sessões e links de origem |
| `baixar_trabalhos.py` | Baixa os arquivos listados no CSV para as pastas das sessões |
| `analise/` | Scripts, textos extraídos e classificação (ver abaixo) |
| `dashboard/index.html` | Dashboard final |
| `dashboard/downloads/` | Cópias dos originais e classificação (CSV e JSON) |

## Passos da análise

### 1. Catalogação e deduplicação
`analise/01_catalogar.py`

- Lê as 44 linhas de `lista_trabalhos_e_links.csv`.
- Para cada linha, procura nas pastas o arquivo correspondente. O nome do arquivo tem o título normalizado (sem acentos, sem pontuação) e truncado em 90 caracteres, então a comparação é feita pelo prefixo.
- Remove cópias idênticas (mesmo md5). Havia cópias de arquivos porque o `baixar_trabalhos.py` foi executado mais de uma vez com numeração diferente.
- Grava `analise/catalogo.json`: um trabalho por entrada, com `id` (T01 a T44), título, sessão e arquivo de origem.

### 2. Extração do texto
`analise/02_extrair_texto.py` e `analise/leitor_doc.py`

- **PDF:** `pdftotext -layout`.
- **DOCX:** leitura direta do `word/document.xml` do pacote, sem dependências extras.
- **DOC (Word 97-2003):** o LibreOffice não conseguiu abrir os arquivos neste ambiente, então `leitor_doc.py` lê o contêiner OLE e a tabela de peças do Word (formato MS-DOC). Biblioteca padrão do Python, sem dependências.
- Saída: `analise/textos/T01.txt` a `T44.txt`. Todos os textos foram gerados; nenhum ficou vazio ou muito curto. A conversão de símbolos matemáticos de PDFs pode perder caracteres (caso visível em T09).

### 3. Leitura e registro dos campos
`analise/03_classificacao.py`

Para cada trabalho foram lidos o resumo e a conclusão, e registrados cinco campos:

- **Objetivo**
- **Técnica utilizada**
- **Dados utilizados**
- **Resultados**
- **Conclusões**

Os campos foram escritos a partir do texto, sem automação. Quando o resumo não traz um dado (valores numéricos, resultados de trabalhos em andamento, conclusão truncada), o registro diz isso explicitamente em vez de completar a informação.

### 4. Definição dos temas
`analise/03_classificacao.py` (dicionário `CLUSTERS` e `ATRIBUICAO`)

- Os 44 trabalhos foram agrupados em 8 temas a partir dos resumos. Cada trabalho entra em um único tema.
- A divisão é um julgamento de leitura, não o resultado de um algoritmo de agrupamento. Não houve modelagem de tópicos nem medida de similaridade.

| Tema | Trabalhos |
|---|---|
| IA na elaboração e revisão de itens | 5 |
| Predição e pré-testagem com IA | 8 |
| IA na análise e gestão de dados educacionais | 7 |
| Modelos TRI e estimação de proficiência | 5 |
| Equalização, escalas e interpretação | 3 |
| Padrões de desempenho e standard setting | 3 |
| Fidedignidade, qualidade de instrumentos e correção | 7 |
| Funcionamento de itens, equidade e uso de resultados | 6 |

Grava `analise/trabalhos.json`, com os campos de cada trabalho e a definição dos temas.

### 5. Geração do dashboard e dos downloads
`analise/04_gerar_dashboard.py` e `analise/dashboard_template.html`

- Copia os arquivos originais para `dashboard/downloads/originais/`, com nomes no padrão `T01 - título`.
- Grava `classificacao.csv` e `classificacao.json`.
- Preenche o template HTML com os dados. O dashboard não usa servidor nem bibliotecas externas além da fonte.

### 6. Verificação
- Contagem: 44 trabalhos, 8 temas, 5 sessões e pôster (29 trabalhos de pôster), 44 downloads.
- O JavaScript do dashboard foi checado com `node --check`.
- A página foi renderizada no Chromium headless: contadores, cartões e blocos de tema aparecem como esperado.
- Os filtros e a busca não foram testados em navegador real.

## Reproduzir

Requisitos: Python 3, `pdftotext` (pacote poppler-utils). Não há dependências Python externas.

```bash
python3 analise/01_catalogar.py
python3 analise/02_extrair_texto.py
python3 analise/03_classificacao.py
python3 analise/04_gerar_dashboard.py
```

Os passos 1 e 2 dependem dos arquivos baixados. O passo 3 contém os textos da classificação, então qualquer alteração de campo ou de tema deve ser feita nele.

## Limitações

- A classificação é manual e reflete a leitura dos resumos. Outro leitor poderia alocar alguns trabalhos a outro tema.
- Os campos vêm principalmente dos resumos. As seções de resultados e conclusões dos textos completos não foram registradas uma a uma.
- Os autores e as instituições não foram extraídos.
- Alguns trabalhos são propostas ou estudos em andamento; os campos desses trabalhos dizem isso.
