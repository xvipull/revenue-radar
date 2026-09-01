import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PipelineTests(__import__('unittest').TestCase):
 def setUp(self):
  subprocess.run([sys.executable,'src/generate_data.py'],cwd=ROOT,check=True); subprocess.run([sys.executable,'src/pipeline.py'],cwd=ROOT,check=True)
 def test_quality_controls_pass(self):
  r=json.loads((ROOT/'reports/data_quality_report.json').read_text()); self.assertEqual(r['status'],'PASS'); self.assertEqual(r['referential_failures'],0)
 def test_dashboard_has_scored_exceptions(self):
  d=json.loads((ROOT/'web/dashboard-data.json').read_text()); self.assertGreater(len(d['orders']),100); self.assertTrue(any(int(x['leakage_score'])>=70 for x in d['orders']))
