"""Ensure testing JSON and generated Office artifacts stay aligned."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
DD = REPO / "docs" / "testing" / "document-data"
DOCS = REPO / "docs" / "testing" / "documents"
RD = REPO / "docs" / "testing" / "results-data"

OFFICE_FILES = [
    "Group4_STeemBang_Doc1_TestPlan.docx",
    "Group4_STeemBang_Doc2_TestCases.xlsx",
    "Group4_STeemBang_Doc5_SystemTestReport.docx",
    "Group4_STeemBang_Doc6_UATPlanReport.docx",
    "Group4_STeemBang_Doc7_DefectLog.xlsx",
    "Group4_STeemBang_Doc8_RegressionTestReport.docx",
    "Group4_STeemBang_Doc9_TestSummaryReport.docx",
]

JSON_SOURCES = [
    "01_test_plan.json",
    "02_test_cases_document.json",
    "03_system_test_report.json",
    "04_uat_plan_and_report.json",
    "05_defect_bug_report_log.json",
    "06_regression_test_report.json",
    "07_test_summary_report.json",
]


@pytest.mark.parametrize("name", JSON_SOURCES)
def test_document_data_json_exists(name: str) -> None:
    assert (DD / name).is_file()


@pytest.mark.parametrize("name", OFFICE_FILES)
def test_generated_office_artifact_exists(name: str) -> None:
    path = DOCS / name
    assert path.is_file(), f"Missing {name}; run generate_documents.py"
    assert path.stat().st_size > 500


def test_manifest_lists_seven_documents() -> None:
    manifest = json.loads((DD / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["project"] == "(S)TeemBang"
    assert manifest["group"] == "Group 4"
    assert len(manifest["documents"]) == 7


def test_doc2_execution_log_matches_results_data() -> None:
    doc2 = json.loads((DD / "02_test_cases_document.json").read_text(encoding="utf-8"))
    rd = json.loads((RD / "doc2_execution_log_results.json").read_text(encoding="utf-8"))
    assert doc2["sheet_a_execution_log"]["rows"] == rd["rows"]


def test_uat_section_11_matches_results_data() -> None:
    uat_doc = json.loads((DD / "04_uat_plan_and_report.json").read_text(encoding="utf-8"))
    uat_rd = json.loads((RD / "uat_execution_results.json").read_text(encoding="utf-8"))
    doc_rows = uat_doc["section_11_execution_results"]["rows"]
    assert len(doc_rows) == 7
    for doc_row, rd_row in zip(doc_rows, uat_rd["rows"], strict=True):
        assert doc_row["uat_id"] == rd_row["uat_id"]
        assert doc_row["pass_fail"] == rd_row["pass_fail"]


def test_system_report_automated_evidence_lists_pytest_tests() -> None:
    sys_doc = json.loads((DD / "03_system_test_report.json").read_text(encoding="utf-8"))
    tests = sys_doc["automated_evidence"]["tests"]
    assert "test_health" in tests
    assert "passed" in sys_doc["automated_evidence"]["outcome"].lower()


def test_summary_metrics_align_with_doc7_defect_count() -> None:
    summary = json.loads((DD / "07_test_summary_report.json").read_text(encoding="utf-8"))
    defects = json.loads((DD / "05_defect_bug_report_log.json").read_text(encoding="utf-8"))
    assert summary["metrics"]["defects"]["total_logged"] == len(defects["defects"])
