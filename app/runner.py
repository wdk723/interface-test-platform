import json
import os
import pytest

def run_test_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    os.makedirs("generated", exist_ok=True)
    test_file = os.path.join("generated", "test_cases.py")

    with open(test_file, "w", encoding="utf-8") as f:
        f.write("import requests\n\n")
        for i, case in enumerate(cases):
            f.write(f"def test_case_{i}():\n")
            f.write(f"    resp = requests.{case['method'].lower()}('{case['url']}')\n")
            f.write(f"    assert resp.status_code == {case['expected_status']}\n\n")

    os.makedirs("reports", exist_ok=True)
    pytest.main([
        test_file,
        "--html=reports/report.html",
        "--self-contained-html"
    ])
