# Mapa de Judicialização e Concentração do BPC

Projeto em `Python + Streamlit` para analisar concentração territorial e judicialização do Benefício de Prestação Continuada (BPC) com base em uma camada sintética calibrada segundo o schema oficial do Portal da Transparência.

O foco do projeto é reproduzir uma análise territorial e de controle social que seria útil para monitorar:

- concentração do gasto assistencial;
- distribuição municipal do benefício;
- participação de benefícios concedidos judicialmente;
- municípios que merecem priorização em análise gerencial ou auditoria.

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

### Current outputs

- `102` municipalities
- `36` monthly competencies
- `7,344` synthetic rows
- average municipal judicialization rate above `5%`
