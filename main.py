from __future__ import annotations

from src.pipeline import run_pipeline


if __name__ == "__main__":
    summary = run_pipeline()
    print("Mapa de Judicialização e Concentração do BPC")
    print("-" * 46)
    for key, value in summary.items():
        print(f"{key}: {value}")

