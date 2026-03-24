from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline import run_pipeline


class PipelineTest(unittest.TestCase):
    def test_pipeline_outputs_expected_summary(self):
        summary = run_pipeline()
        self.assertEqual(summary["municipios_cobertos"], 102)
        self.assertEqual(summary["competencias_cobertas"], 36)
        self.assertEqual(summary["linhas_sinteticas"], 7344)
        self.assertGreater(summary["taxa_media_judicializacao_pct"], 5)


if __name__ == "__main__":
    unittest.main()
