from __future__ import annotations

import json

import numpy as np
import pandas as pd

from .config import MUNICIPAL_SUMMARY_PATH, PROCESSED_DIR, RAW_SOURCE_PATH, SUMMARY_PATH, SYNTHETIC_BPC_PATH


def _load_municipalities() -> pd.DataFrame:
    raw_df = pd.read_csv(RAW_SOURCE_PATH)
    municipalities = raw_df[["co_mun", "no_mun"]].drop_duplicates().rename(
        columns={"co_mun": "codigo_municipio_siafi", "no_mun": "nome_municipio"}
    )
    municipalities["codigo_municipio_siafi"] = municipalities["codigo_municipio_siafi"].astype(str)
    municipalities["uf"] = "AL"
    return municipalities.sort_values("nome_municipio").reset_index(drop=True)


def build_synthetic_bpc_dataset(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    municipalities = _load_municipalities()
    months = pd.period_range("2023-01", "2025-12", freq="M")
    min_wage = {2023: 1320.0, 2024: 1412.0, 2025: 1518.0}

    records: list[dict[str, object]] = []
    for idx, row in municipalities.iterrows():
        municipal_factor = 0.65 + (idx / len(municipalities)) * 1.7
        judicial_base = 0.05 + ((idx % 9) / 100)
        if row["nome_municipio"] in {"Maceió", "Arapiraca", "Palmeira dos Índios"}:
            judicial_base += 0.08

        for period in months:
            year = period.year
            month = period.month
            seasonal = 1.02 if month in (1, 2) else 1.0 if month in (3, 4, 5, 6, 7, 8, 9, 10) else 1.04
            base_benefits = int(max(55, rng.normal(loc=260 * municipal_factor * seasonal, scale=18)))
            judicial_share = min(0.30, max(0.03, rng.normal(loc=judicial_base, scale=0.015)))

            judicial_count = max(1, int(round(base_benefits * judicial_share)))
            non_judicial_count = max(1, base_benefits - judicial_count)

            for judicial_flag, count in (("SIM", judicial_count), ("NÃO", non_judicial_count)):
                value = min_wage[year]
                if judicial_flag == "SIM":
                    value *= 1.0

                records.append(
                    {
                        "ano_mes_competencia": f"{year}-{month:02d}",
                        "ano_mes_referencia": f"{year}-{month:02d}",
                        "uf": row["uf"],
                        "codigo_municipio_siafi": row["codigo_municipio_siafi"],
                        "nome_municipio": row["nome_municipio"],
                        "beneficio_concedido_judicialmente": judicial_flag,
                        "valor_parcela": float(value),
                        "quantidade_beneficios": int(count),
                        "valor_total": float(round(count * value, 2)),
                    }
                )

    return pd.DataFrame(records)


def build_municipal_summary(bpc_df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        bpc_df.groupby(["codigo_municipio_siafi", "nome_municipio"], as_index=False)
        .agg(
            valor_total_bpc=("valor_total", "sum"),
            quantidade_beneficios=("quantidade_beneficios", "sum"),
        )
    )

    judicial = (
        bpc_df[bpc_df["beneficio_concedido_judicialmente"] == "SIM"]
        .groupby(["codigo_municipio_siafi", "nome_municipio"], as_index=False)
        .agg(
            valor_judicial=("valor_total", "sum"),
            beneficios_judiciais=("quantidade_beneficios", "sum"),
        )
    )
    summary = summary.merge(judicial, on=["codigo_municipio_siafi", "nome_municipio"], how="left").fillna(0)
    summary["taxa_judicializacao_pct"] = (
        (summary["beneficios_judiciais"] / summary["quantidade_beneficios"]) * 100
    ).round(2)

    total_value = summary["valor_total_bpc"].sum()
    summary["participacao_valor_pct"] = ((summary["valor_total_bpc"] / total_value) * 100).round(4)
    summary["indice_concentracao"] = (
        (summary["participacao_valor_pct"] / summary["participacao_valor_pct"].mean()) * 100
    ).round(2)
    summary["risco_judicializacao"] = summary["taxa_judicializacao_pct"].map(
        lambda value: "alto" if value >= 14 else "moderado" if value >= 9 else "baixo"
    )
    return summary.sort_values(["taxa_judicializacao_pct", "valor_total_bpc"], ascending=[False, False])


def build_summary_dict(bpc_df: pd.DataFrame, municipal_df: pd.DataFrame) -> dict[str, object]:
    top_city = municipal_df.sort_values("valor_total_bpc", ascending=False).iloc[0]
    top_judicial = municipal_df.sort_values("taxa_judicializacao_pct", ascending=False).iloc[0]
    return {
        "municipios_cobertos": int(municipal_df["nome_municipio"].nunique()),
        "competencias_cobertas": int(bpc_df["ano_mes_competencia"].nunique()),
        "linhas_sinteticas": int(len(bpc_df)),
        "valor_total_bpc": float(round(municipal_df["valor_total_bpc"].sum(), 2)),
        "taxa_media_judicializacao_pct": float(round(municipal_df["taxa_judicializacao_pct"].mean(), 2)),
        "municipio_maior_concentracao": str(top_city["nome_municipio"]),
        "municipio_maior_judicializacao": str(top_judicial["nome_municipio"]),
    }


def run_pipeline() -> dict[str, object]:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    bpc_df = build_synthetic_bpc_dataset()
    municipal_df = build_municipal_summary(bpc_df)
    summary = build_summary_dict(bpc_df, municipal_df)

    bpc_df.to_parquet(SYNTHETIC_BPC_PATH, index=False)
    municipal_df.to_parquet(MUNICIPAL_SUMMARY_PATH, index=False)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary
