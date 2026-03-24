# Mapa de Judicialização e Concentração do BPC

Projeto em `Python + Streamlit` para analisar concentração territorial e judicialização do Benefício de Prestação Continuada (BPC) com base em uma camada sintética calibrada segundo o schema oficial do Portal da Transparência.

O foco do projeto é reproduzir uma análise territorial e de controle social que seria útil para monitorar:

- concentração do gasto assistencial;
- distribuição municipal do benefício;
- participação de benefícios concedidos judicialmente;
- municípios que merecem priorização em análise gerencial ou auditoria.

## Por que esse tipo de análise importa

O BPC é um benefício assistencial de alta relevância social e orçamentária. Em contextos de análise pública, olhar apenas o valor total pago não é suficiente. Também importa entender:

- como o benefício se distribui territorialmente;
- quais municípios concentram maior parcela do valor total;
- onde a judicialização parece mais elevada;
- e como combinar concentração e judicialização para priorizar investigação, acompanhamento e ação gerencial.

Esse projeto foi pensado justamente para reproduzir esse tipo de leitura analítica.

## O que é o BPC

O Benefício de Prestação Continuada é um benefício assistencial previsto na LOAS. Ele garante um salário mínimo mensal à pessoa idosa com 65 anos ou mais e à pessoa com deficiência que comprovem não possuir meios de se manter nem de ser mantidas pela família. Diferentemente da aposentadoria, o BPC não exige contribuição prévia ao INSS.  
Fonte: [GOV.BR - BPC](https://www.gov.br/pt-br/servicos/solicitar-beneficio-assistencial-a-pessoa-com-deficiencia-bpc-loas), [GOV.BR - BPC Idoso](https://www.gov.br/pt-br/servicos/solicitar-beneficio-assistencial-ao-idoso-bpc-loas)

## Para que serve

Este projeto serve para simular uma análise territorial de gestão social e controle:

- medir onde o BPC está mais concentrado;
- identificar municípios com maior participação relativa no valor total;
- analisar a proporção de benefícios concedidos judicialmente;
- destacar municípios críticos pela combinação de alta judicialização e alta concentração.

## Fonte e desenho dos dados

Como o download transacional oficial do BPC não estava acessível automaticamente neste ambiente, o projeto usa uma **base sintética calibrada**, construída a partir:

- do **dicionário oficial de dados do BPC** do Portal da Transparência;
- de uma base pública aberta de municípios de Alagoas usada como suporte territorial.

O dicionário oficial do BPC inclui campos como:

- `Ano/Mês Competência`
- `Ano/Mês Referência`
- `UF`
- `Código Município SIAFI`
- `Nome Município`
- `Benefício Concedido Judicialmente`
- `Valor Parcela`

Fonte oficial do schema: [Dicionário de Dados - BPC](https://portaldatransparencia.gov.br/dicionario-de-dados/bpc)

Base territorial auxiliar usada na simulação:

- [al_municipios_base.csv](data/raw/al_municipios_base.csv)

## O que os dados representam

O projeto não usa registros individuais de beneficiários. Em vez disso, ele trabalha com uma camada sintética agregada por:

- município;
- competência mensal;
- status de judicialização.

Cada linha da base representa um recorte analítico com:

- `ano_mes_competencia`
  Mês de competência do benefício.
- `ano_mes_referencia`
  Mês de referência do registro.
- `uf`
  Unidade federativa.
- `codigo_municipio_siafi`
  Código do município.
- `nome_municipio`
  Nome do município.
- `beneficio_concedido_judicialmente`
  Indica se o bloco agregado representa benefícios concedidos judicialmente.
- `valor_parcela`
  Valor unitário da parcela.
- `quantidade_beneficios`
  Quantidade agregada de benefícios naquele recorte.
- `valor_total`
  Valor total agregado daquele grupo.

Essa estrutura permite derivar indicadores que são muito úteis em gestão social:

- volume total do benefício por município;
- peso relativo de cada município no total da base;
- taxa de judicialização municipal;
- e um índice sintético de concentração.

### Cobertura da base sintética

- `102` municípios de Alagoas
- `36` competências mensais (`2023-01` a `2025-12`)
- `7.344` linhas agregadas mensais por município e status judicial

## Técnicas usadas

- `pandas`
  Para geração e agregação da base sintética.
- `Streamlit`
  Para o dashboard interativo.
- `Plotly`
  Para visualizações de concentração e judicialização.
- regras analíticas de concentração
  Para calcular participação relativa e índice de concentração municipal.

## Como cada técnica foi utilizada

### 1. Geração sintética calibrada

Como a base transacional pública do BPC não estava acessível de forma automatizada neste ambiente, a solução adotada foi criar uma base sintética com comportamento plausível, mantendo aderência ao schema oficial.

O pipeline faz isso assim:

- usa uma base territorial pública de municípios de Alagoas;
- cria competências mensais entre `2023-01` e `2025-12`;
- define o valor da parcela com base no salário mínimo de cada ano;
- gera volumes de benefícios por município com fatores territoriais e sazonais;
- cria uma parcela judicial calibrada por município, com reforço em municípios maiores.

Essa abordagem não substitui o dado oficial, mas é útil para reproduzir o raciocínio analítico e a lógica de produto.

### 2. Agregação territorial

Depois da geração sintética, o projeto agrega os dados por município para calcular:

- `valor_total_bpc`
- `quantidade_beneficios`
- `valor_judicial`
- `beneficios_judiciais`
- `taxa_judicializacao_pct`

Essa é a camada central para responder perguntas como:

- onde o BPC está mais concentrado?
- onde a judicialização é maior?
- quais municípios combinam maior volume e maior sensibilidade jurídica?

### 3. Índice de concentração

O projeto calcula também:

- `participacao_valor_pct`
  Quanto do valor total da base cada município representa.
- `indice_concentracao`
  Um índice relativo comparando a participação do município com a média geral.

Isso ajuda a transformar o valor bruto em leitura comparativa.

### 4. Classificação analítica de risco

O campo `risco_judicializacao` é derivado por regra:

- `alto`
- `moderado`
- `baixo`

Ele não é um modelo supervisionado; é uma classificação operacional baseada em faixas da taxa de judicialização. Isso é útil para deixar o painel mais acionável.

## Bibliotecas e frameworks

### `pandas`

Foi usada para:

- leitura da base territorial auxiliar;
- geração da base sintética;
- agregações por município;
- cálculo dos indicadores finais;
- export dos datasets em `parquet`.

Escolha:

- ideal para prototipação analítica rápida;
- muito eficiente para esse volume de dados;
- simples de explicar em portfólio e entrevista.

### `Streamlit`

Foi usado para construir a interface final do usuário.

Escolha:

- facilita transformar a análise em produto explorável;
- permite navegação rápida por abas;
- é muito bom para demos e portfólio.

### `Plotly`

Foi usado para as visualizações interativas:

- barras para concentração;
- linha temporal por judicialização;
- treemap territorial;
- scatter para relação entre concentração e judicialização.

Escolha:

- bom suporte a interatividade;
- visual mais forte para GitHub e entrevistas;
- fácil integração com Streamlit.

## Pipeline

1. Carregar municípios de Alagoas.
2. Gerar base sintética do BPC com:
   - competências mensais
   - valor de parcela
   - quantidade de benefícios
   - status de judicialização
3. Agregar os dados por município.
4. Calcular:
   - valor total do BPC
   - benefícios totais
   - benefícios judiciais
   - taxa de judicialização
   - participação no valor total
   - índice de concentração
5. Exibir o painel analítico.

## Como interpretar os resultados

- `valor_total_bpc`
  Mostra os municípios com maior concentração absoluta do benefício.
- `taxa_judicializacao_pct`
  Mostra o peso relativo da judicialização na composição do benefício local.
- `participacao_valor_pct`
  Mede a participação de cada município no valor total da base.
- `indice_concentracao`
  Ajuda a identificar municípios cuja presença no gasto total está acima da média da distribuição.
- `risco_judicializacao`
  Traduz a taxa em uma categoria mais fácil de consumir por gestão e controle.

## Resultados atuais

- `102` municípios cobertos
- `36` competências mensais
- `7.344` linhas sintéticas
- taxa média de judicialização municipal acima de `5%`
- município com maior concentração do valor total: `Viçosa`
- município com maior taxa de judicialização simulada: `Palmeira dos Índios`

## Como executar

```bash
cd "/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/mapa-de-judicializacao-e-concentracao-do-BPC"
source .venv/bin/activate
python main.py
streamlit run app.py
```

## Testes

```bash
source .venv/bin/activate
python -m unittest discover -s tests -v
```

## English

### What this project is for

This project simulates a territorial analytics workflow for BPC, focused on:

- concentration of benefit value across municipalities;
- judicialization rate by municipality;
- identification of critical municipalities with both high concentration and high judicial share.

### Data design

The project uses a **synthetic but schema-aligned** BPC dataset, inspired by the official Portal da Transparência data dictionary and calibrated with a public municipal territorial base from Alagoas.

### Techniques and tools

- `pandas` for synthetic data generation and aggregation
- `Streamlit` for the dashboard
- `Plotly` for interactive visual analytics
- rule-based territorial indicators for concentration and judicialization risk

### Current outputs

- `102` municipalities
- `36` monthly competencies
- `7,344` synthetic rows
- average municipal judicialization rate above `5%`
