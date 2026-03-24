from __future__ import annotations

import json

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import MUNICIPAL_SUMMARY_PATH, SUMMARY_PATH, SYNTHETIC_BPC_PATH
from src.pipeline import run_pipeline


st.set_page_config(page_title="Mapa de Judicialização do BPC", layout="wide")

st.markdown(
    """
    <style>
      .stApp { background: #07111f; color: #f7fafc; }
      .block-container { padding-top: 2rem; }
      [data-testid="stMetricValue"] { color: #86efac; }
      h1, h2, h3 { color: #f8fafc; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    if not SUMMARY_PATH.exists():
        run_pipeline()
    bpc_df = pd.read_parquet(SYNTHETIC_BPC_PATH)
    municipal_df = pd.read_parquet(MUNICIPAL_SUMMARY_PATH)
    summary = json.loads(SUMMARY_PATH.read_text())
    return bpc_df, municipal_df, summary


bpc_df, municipal_df, summary = load_data()

st.title("Mapa de Judicialização e Concentração do BPC")
st.caption(
    "Painel analítico com base sintética calibrada para investigar concentração territorial do BPC e participação de benefícios concedidos judicialmente."
)

cols = st.columns(5)
cols[0].metric("Municípios", summary["municipios_cobertos"])
cols[1].metric("Competências", summary["competencias_cobertas"])
cols[2].metric("Linhas", summary["linhas_sinteticas"])
cols[3].metric("Valor total", f"R$ {summary['valor_total_bpc']:,.0f}".replace(",", "."))
cols[4].metric("Judicialização média", f"{summary['taxa_media_judicializacao_pct']:.2f}%")

tab1, tab2, tab3 = st.tabs(["Concentração", "Judicialização", "Municípios críticos"])

with tab1:
    top_concentration = municipal_df.nlargest(15, "valor_total_bpc").copy()
    fig_conc = px.bar(
        top_concentration,
        x="valor_total_bpc",
        y="nome_municipio",
        orientation="h",
        title="Top 15 municípios por valor total do BPC",
        color="participacao_valor_pct",
    )
    fig_conc.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_conc, use_container_width=True)

    treemap = px.treemap(
        top_concentration,
        path=[px.Constant("Alagoas"), "nome_municipio"],
        values="valor_total_bpc",
        color="taxa_judicializacao_pct",
        title="Concentração do BPC nos principais municípios",
    )
    st.plotly_chart(treemap, use_container_width=True)

with tab2:
    top_judicial = municipal_df.nlargest(20, "taxa_judicializacao_pct").copy()
    fig_jud = px.bar(
        top_judicial,
        x="taxa_judicializacao_pct",
        y="nome_municipio",
        orientation="h",
        title="Top 20 municípios por taxa de judicialização",
        color="beneficios_judiciais",
    )
    fig_jud.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_jud, use_container_width=True)

    time_df = (
        bpc_df.assign(ano_mes=pd.to_datetime(bpc_df["ano_mes_competencia"]))
        .groupby(["ano_mes", "beneficio_concedido_judicialmente"], as_index=False)["valor_total"]
        .sum()
    )
    fig_time = px.line(
        time_df,
        x="ano_mes",
        y="valor_total",
        color="beneficio_concedido_judicialmente",
        title="Evolução temporal do valor do BPC por judicialização",
    )
    st.plotly_chart(fig_time, use_container_width=True)

with tab3:
    critical = municipal_df.sort_values(
        ["taxa_judicializacao_pct", "indice_concentracao"], ascending=[False, False]
    ).head(20)
    scatter = px.scatter(
        municipal_df,
        x="taxa_judicializacao_pct",
        y="participacao_valor_pct",
        color="risco_judicializacao",
        hover_name="nome_municipio",
        size="valor_total_bpc",
        title="Concentração territorial vs judicialização",
    )
    st.plotly_chart(scatter, use_container_width=True)
    st.dataframe(
        critical[
            [
                "nome_municipio",
                "valor_total_bpc",
                "quantidade_beneficios",
                "beneficios_judiciais",
                "taxa_judicializacao_pct",
                "participacao_valor_pct",
                "indice_concentracao",
                "risco_judicializacao",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
