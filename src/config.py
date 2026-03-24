from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_SOURCE_PATH = BASE_DIR / "data" / "raw" / "al_municipios_base.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SYNTHETIC_BPC_PATH = PROCESSED_DIR / "bpc_synthetic_monthly.parquet"
MUNICIPAL_SUMMARY_PATH = PROCESSED_DIR / "municipal_summary.parquet"
SUMMARY_PATH = PROCESSED_DIR / "summary.json"
