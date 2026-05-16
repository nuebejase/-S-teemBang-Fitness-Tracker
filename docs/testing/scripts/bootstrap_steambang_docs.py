"""One-time bootstrap: STEemBang document-data and requirements-data JSON."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DD = ROOT / "document-data"
RD_REQ = ROOT / "requirements-data"
RD_RES = ROOT / "results-data"

GROUP = "Group 4"
PROJECT = "(S)TeemBang"
TEAM = ["Christel", "Sherwin", "John Rae", "Jase Karl"]
DATE = "2026-05-16"
DATE_PYTEST = "2026-05-16"


def w(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    w(
        DD / "manifest.json",
        {
            "project": PROJECT,
            "group": GROUP,
            "compiled_date": DATE,
            "sync_script": "python docs/testing/scripts/sync_results_to_document_data.py",
            "generated_office_documents": "python docs/testing/document-data/generate_documents.py",
            "results_capture": "docs/testing/results-data/",
            "source_notes": "Built from docs/Project.json, docs/testing/requirements-data/, docs/instructions.txt.",
            "suggested_zip_naming": "Group4_STeemBang_DocN_<Name>.pdf per course requirements PDF",
            "documents": [
                {"order": 1, "file": "01_test_plan.json", "deliverable": "Test Plan", "course_doc": "Doc 1"},
                {"order": 2, "file": "02_test_cases_document.json", "deliverable": "Test Cases Document", "course_doc": "Doc 2"},
                {"order": 3, "file": "03_system_test_report.json", "deliverable": "System Test Report", "course_doc": "Doc 5"},
                {"order": 4, "file": "04_uat_plan_and_report.json", "deliverable": "UAT Plan & Report", "course_doc": "Doc 6"},
                {"order": 5, "file": "05_defect_bug_report_log.json", "deliverable": "Defect / Bug Report Log", "course_doc": "Doc 7"},
                {"order": 6, "file": "06_regression_test_report.json", "deliverable": "Regression Test Report", "course_doc": "Doc 8"},
                {"order": 7, "file": "07_test_summary_report.json", "deliverable": "Test Summary Report", "course_doc": "Doc 9"},
            ],
            "not_included_by_user_request": ["Unit Test Report (Doc 3)", "Integration Test Report (Doc 4)"],
        },
    )

    exec_rows = [
        ("SBR-005", "[Verify UI] Long notes on profile or workout form do not overflow on narrow viewports."),
        ("SBR-007", "Forgot-password / email recovery — not in scope; document as N/A."),
        ("SBR-009", "Social login — not implemented; mark N/A."),
        ("SBD-001", "Dashboard shows today steps, workouts, streak after login."),
        ("SBD-002", "Sync steps updates dashboard totals."),
        ("SBA-001", "Log workout creates activity with calories."),
        ("SBA-002", "Workout duration drives calorie estimate."),
        ("SBG-001", "Create daily/weekly/monthly goal."),
        ("SBAn-001", "Analytics trends chart loads for 7/14/30 days."),
        ("SBN-001", "Notifications list loads; mark-read works."),
        ("SBP-001", "Profile height/weight/step target update persists."),
        ("SBAd-001", "Admin dashboard stats require admin role."),
        ("SBS-001", "Member cannot access admin UI routes."),
        ("SBS-003", "Unauthenticated request to admin stats returns 401."),
        ("SBGen-001", "GET /api/health returns ok."),
        ("SBGen-002", "Responsive layout on dashboard and workouts at ~390px."),
    ]
    sheet_a = {
        "columns": [
            "Test Case ID",
            "Pass/Fail",
            "Test Execution Date",
            "Responsible Developer",
            "Responsible Tester",
            "Comment",
            "Additional Comments (other than QA team)",
        ],
        "rows": [
            {
                "test_case_id": tid,
                "pass_fail": "",
                "test_execution_date": DATE,
                "responsible_developer": "",
                "responsible_tester": "",
                "comment": comment,
                "additional_comments_non_qa": "",
            }
            for tid, comment in exec_rows
        ],
    }

    detailed = [
        ("SBR-001", "Authentication", "Member registration", "Backend running.", ["POST /api/auth/register with new email."], "pytest_member@example.com", "201; role member in /me.", "Critical"),
        ("SBR-003", "Authentication", "Login success", "Registered member.", ["POST /api/auth/login."], "demo@steambang.com / demo1234", "200; JWT; /me returns profile.", "Critical"),
        ("SBD-002", "Dashboard", "Sync steps", "Logged-in member.", ["POST /api/activities/steps/sync with steps count."], "steps: 4500", "Dashboard today_steps updates.", "High"),
        ("SBA-001", "Activities", "Log workout", "Logged-in member.", ["POST /api/activities workout payload."], "running 30 min", "201; calories_burned > 0.", "Critical"),
        ("SBG-001", "Goals", "Create goal", "Logged-in member.", ["POST /api/goals daily steps target."], "metric steps, target 8000", "201 goal created.", "High"),
        ("SBAn-001", "Analytics", "Trends 7-day", "Demo user seeded.", ["GET /api/analytics/trends?days=7."], "demo@steambang.com", "7 points returned.", "High"),
        ("SBAd-001", "Admin", "Platform stats", "Admin logged in.", ["GET /api/admin/stats."], "admin@steambang.com", "total_users >= 2.", "High"),
        ("SBS-003", "Security", "Admin stats without auth", "No token.", ["GET /api/admin/stats without Authorization."], "N/A", "401 Unauthorized.", "Critical"),
        ("SBGen-001", "General", "Health check", "API running.", ["GET /api/health."], "N/A", '{"status":"ok"}.', "High"),
        ("SBGen-002", "General", "Mobile layout smoke", "Frontend dev server.", ["Resize to 390px; open Dashboard and Workouts."], "N/A", "Navigation usable; no horizontal scroll on main nav.", "Medium"),
    ]
    sheet_b = {
        "columns": [
            "Test Case ID",
            "Module / Feature",
            "Test Case Title",
            "Preconditions",
            "Test Steps",
            "Test Data",
            "Expected Result",
            "Actual Result",
            "Pass / Fail",
            "Priority",
            "Tester Name",
            "Date Executed",
        ],
        "rows": [
            {
                "test_case_id": tid,
                "module_feature": mod,
                "test_case_title": title,
                "preconditions": pre,
                "test_steps": steps,
                "test_data": data,
                "expected_result": exp,
                "actual_result": "",
                "pass_fail": "",
                "priority": pri,
                "tester_name": "",
                "date_executed": "",
            }
            for tid, mod, title, pre, steps, data, exp, pri in detailed
        ],
    }

    w(
        DD / "02_test_cases_document.json",
        {
            "compiled_into": "docs/testing/document-data",
            "suggested_filename": "Group4_STeemBang_Doc2_TestCases.xlsx",
            "document": "Doc 2 — Test Cases + Test Execution Log",
            "project": PROJECT,
            "group": GROUP,
            "id_prefix_legend": {
                "SBR": "Auth",
                "SBD": "Dashboard",
                "SBA": "Activities / workouts",
                "SBG": "Goals",
                "SBAn": "Analytics",
                "SBN": "Notifications",
                "SBP": "Profile",
                "SBAd": "Admin",
                "SBS": "Security / RBAC",
                "SBGen": "General",
            },
            "sheet_a_execution_log": sheet_a,
            "sheet_b_detailed_test_cases": sheet_b,
        },
    )

    w(
        DD / "01_test_plan.json",
        {
            "compiled_into": "docs/testing/document-data",
            "standard": "IEEE 829-1998",
            "project": {
                "name": PROJECT,
                "description": "Fitness tracking: Vue 3 SPA (steambang_frontend) + FastAPI (steambang_backend), SQLite, JWT, activity/goals/analytics.",
                "group": GROUP,
            },
            "sections": {
                "test_plan_identifier": {
                    "title": "Test Plan Identifier",
                    "unique_id": "G4-STEAMBANG-TP-2026-001",
                    "level": "Master / System test plan (pre-final)",
                    "version": "1.0",
                    "date": DATE,
                    "authors": "; ".join(TEAM),
                    "revision_history": [{"version": "1.0", "date": DATE, "change": "Initial test plan for (S)TeemBang."}],
                },
                "introduction": {
                    "title": "Introduction",
                    "purpose": "Define how Group 4 verifies (S)TeemBang meets fitness-tracking requirements before submission.",
                    "references": [
                        "docs/Project.json",
                        "docs/instructions.txt",
                        "docs/resources/WebApp_Testing_Documents_Requirements_Prefinal.pdf",
                        "FastAPI OpenAPI at /docs when API is running",
                    ],
                },
                "scope": {
                    "title": "Scope",
                    "in_scope": [
                        "JWT registration, login, member session",
                        "Activity and workout logging, step sync",
                        "Goals (daily/weekly/monthly)",
                        "Dashboard and analytics trends",
                        "Profile and notifications",
                        "Admin platform stats and RBAC",
                    ],
                    "out_of_scope_for_this_test_cycle": [
                        "Wearable API integration",
                        "AI coaching",
                        "Nutrition engine",
                        "Payments",
                        "Formal load testing",
                    ],
                },
                "test_items": {
                    "title": "Test Items",
                    "items": [
                        {"name": "steambang_frontend", "version": "Vite build", "role": "Member + admin UI"},
                        {"name": "steambang_backend", "version": "FastAPI app/", "role": "REST /api/*"},
                        {"name": "SQLite", "path": "steambang_backend/steambang.db", "role": "Persistence"},
                        {"name": "Automated tests", "path": "steambang_backend/tests/test_api.py", "role": "API smoke"},
                    ],
                },
                "features_to_be_tested": {
                    "title": "Features To Be Tested",
                    "rows": [
                        {"id": "F-AUTH", "feature": "Register, login, /me", "risk": "H", "linked_cases": "SBR-001, SBR-003"},
                        {"id": "F-ACT", "feature": "Workouts and step sync", "risk": "H", "linked_cases": "SBA-001, SBD-002"},
                        {"id": "F-GOAL", "feature": "Goals CRUD", "risk": "M", "linked_cases": "SBG-001"},
                        {"id": "F-AN", "feature": "Dashboard and trends", "risk": "H", "linked_cases": "SBD-001, SBAn-001"},
                        {"id": "F-ADM", "feature": "Admin stats", "risk": "H", "linked_cases": "SBAd-001, SBS-003"},
                        {"id": "F-SEC", "feature": "RBAC", "risk": "H", "linked_cases": "SBS-001, SBS-003"},
                    ],
                },
                "features_not_to_be_tested": {
                    "title": "Features Not To Be Tested",
                    "rows": [
                        {"feature": "Wearable sync", "reason": "Excluded in Project.json scope."},
                        {"feature": "Push notifications to device OS", "reason": "In-app only in this build."},
                    ],
                },
                "approach": {
                    "title": "Approach / Strategy",
                    "methods": [
                        "pytest with FastAPI TestClient",
                        "Manual system cases in Doc 2",
                        "UAT scenarios in Doc 6",
                    ],
                    "tools": ["pytest", "npm run dev / build", "Browser devtools"],
                    "metrics": ["Pass rate by module", "Defect severity counts"],
                },
                "item_pass_fail_criteria": {
                    "title": "Item Pass/Fail Criteria",
                    "criteria": [
                        "Pass when UI/API matches expected result.",
                        "Critical auth, activity logging, or admin RBAC failures block sign-off.",
                    ],
                },
                "suspension_and_resumption": {
                    "title": "Suspension Criteria and Resumption Requirements",
                    "suspend_if": ["API unreachable", "DB corrupt", "Blocking defect on login"],
                    "resume_after": ["Environment restored", "Health + login smoke pass"],
                },
                "test_deliverables": {
                    "title": "Test Deliverables",
                    "list": [
                        "Doc 1 — 01_test_plan.json",
                        "Doc 2 — 02_test_cases_document.json",
                        "Doc 5 — 03_system_test_report.json",
                        "Doc 6 — 04_uat_plan_and_report.json",
                        "Doc 7 — 05_defect_bug_report_log.json",
                        "Doc 8 — 06_regression_test_report.json",
                        "Doc 9 — 07_test_summary_report.json",
                    ],
                },
                "test_tasks_and_schedule": {
                    "title": "Test Tasks and Schedule",
                    "tasks": [
                        {"task": "Finalize test plan", "owner": "Christel", "due": DATE},
                        {"task": "Execute Doc 2 + pytest", "owner": "All members", "due": DATE},
                        {"task": "UAT session", "owner": "Sherwin", "due": DATE},
                        {"task": "Regression + summary", "owner": "Jase Karl", "due": DATE},
                    ],
                },
                "environmental_needs": {
                    "title": "Environmental Needs",
                    "hardware_os": "Windows 10/11, 8 GB+ RAM",
                    "software": "Node.js 18+, Python 3.12+, Chrome/Edge",
                    "network": "localhost; Vite proxies /api to 127.0.0.1:8000",
                    "test_data": "admin@steambang.com / admin123; demo@steambang.com / demo1234",
                },
                "responsibilities": {
                    "title": "Responsibilities",
                    "assignments": [
                        {"role": "Test lead", "person": "Christel", "duty": "Plan and summary"},
                        {"role": "API verification", "person": "[Assign]", "duty": "pytest runs"},
                        {"role": "Manual execution", "person": "[Assign]", "duty": "Doc 2 log"},
                        {"role": "UAT coordination", "person": "[Assign]", "duty": "UAT sign-off"},
                        {"role": "Defect triage", "person": "[Assign]", "duty": "Doc 7"},
                    ],
                },
                "staffing_and_training": {
                    "title": "Staffing and Training Needs",
                    "text": "UAT testers receive URLs, demo credentials, and scenario scripts; no destructive admin actions without DB reset plan.",
                },
                "risks_and_contingencies": {
                    "title": "Risks and Contingencies",
                    "rows": [
                        {"risk": "Single-machine demo", "mitigation": "Capture pytest log and screenshots."},
                        {"risk": "SQLite lock under parallel runs", "mitigation": "Serialize pytest; use test DB from conftest."},
                    ],
                },
                "approvals": {
                    "title": "Approvals",
                    "sign_off_rows": [
                        {"role": "Test Lead", "name": "________________", "signature": "________________", "date": "________"},
                        {"role": "Instructor", "name": "________________", "signature": "________________", "date": "________"},
                    ],
                },
            },
        },
    )

    fr = [
        ("JWT authentication", "SBR-001, SBR-003 + pytest", "[Pass/Fail]", ""),
        ("Activity and workout logging", "SBA-001 + pytest", "[Pass/Fail]", ""),
        ("Step sync (manual/pedometer)", "SBD-002 + pytest", "[Pass/Fail]", ""),
        ("Daily/weekly/monthly goals", "SBG-001 + pytest", "[Pass/Fail]", ""),
        ("Dashboard analytics and trends", "SBD-001, SBAn-001", "[Pass/Fail]", ""),
        ("Profile and notifications", "SBP-001, SBN-001 manual", "[Pass/Fail]", ""),
        ("Admin platform stats", "SBAd-001 + pytest", "[Pass/Fail]", ""),
        ("Wearable integration", "Out of scope", "N/A", "Excluded per Project.json"),
    ]
    w(
        DD / "03_system_test_report.json",
        {
            "project": PROJECT,
            "group": GROUP,
            "report_date": DATE,
            "executive_summary": "System testing validates (S)TeemBang frontend against FastAPI backend for fitness flows. Run pytest and record manual results in Doc 2 before submission.",
            "test_environment": {
                "frontend": "steambang_frontend — Vite dev http://localhost:5173",
                "backend": "steambang_backend — uvicorn :8000",
                "database": "SQLite steambang.db (seeded admin + demo member)",
                "browsers_tested": "[Chrome/Edge + optional Cursor browser]",
                "build_versions": "[Record commit or build date]",
            },
            "functional_requirements_traceability": {
                "title": "Functional results (docs/Project.json)",
                "rows": [
                    {"requirement": r, "how_verified": h, "result": res, "evidence": e}
                    for r, h, res, e in fr
                ],
            },
            "non_functional_results": {
                "title": "Non-functional testing",
                "rows": [
                    {
                        "category": "Security — JWT and RBAC",
                        "objective": "Members cannot access admin stats; unauthenticated API rejected.",
                        "method": "SBS-003 + pytest test_admin_stats",
                        "result": "[Pass/Fail]",
                        "notes": "JWT in localStorage for course demo.",
                    },
                    {
                        "category": "Usability / responsiveness",
                        "objective": "Dashboard and workouts usable at ~390px.",
                        "method": "SBGen-002 manual",
                        "result": "[Pass/Fail]",
                        "notes": "See defect log for layout issues.",
                    },
                ],
            },
            "automated_evidence": {
                "title": "Automated API verification",
                "command": "cd steambang_backend && .venv\\Scripts\\python.exe -m pytest tests -v --tb=short",
                "last_run_date": DATE_PYTEST,
                "outcome": "[Fill after pytest run]",
                "tests": [
                    "test_health",
                    "test_register_login_dashboard",
                    "test_demo_user_seeded",
                    "test_admin_stats",
                ],
                "instruction": "Attach terminal screenshot to Word report.",
            },
            "defects_during_system_test": {
                "title": "Defects during system test",
                "text": "Cross-reference Doc 7.",
                "placeholder_ids": ["DEF-001 through DEF-008"],
            },
            "overall_assessment": {
                "title": "Overall assessment",
                "planned_manual_cases": len(exec_rows),
                "executed_manual_cases": "[Fill]",
                "passed_manual_cases": "[Fill]",
                "readiness_statement": "[Fill after sync]",
            },
        },
    )

    uat_cases = [
        ("UAT-SB-001", "Authentication", "Register, log out, log back in as member", "Member", "Critical"),
        ("UAT-SB-002", "Dashboard", "View dashboard stats and sync steps", "Member", "Critical"),
        ("UAT-SB-003", "Workouts", "Log a workout and see calories on dashboard", "Member", "High"),
        ("UAT-SB-004", "Goals", "Set a daily step goal and view progress", "Member", "High"),
        ("UAT-SB-005", "Analytics", "Open analytics and change trend period", "Member", "High"),
        ("UAT-SB-006", "Admin", "Admin views platform stats; member cannot", "Admin + Member", "Critical"),
        ("UAT-SB-007", "Access control", "Guest/member blocked from admin routes and APIs", "Mixed", "Critical"),
    ]
    w(
        RD_REQ / "05_suggested_uat_scenarios_steambang.json",
        {
            "purpose": "UAT scenarios for (S)TeemBang (minimum 5; 7 listed).",
            "uat_cases": [
                {
                    "uat_id": uid,
                    "module": mod,
                    "scenario_title": title,
                    "role": role,
                    "priority": pri,
                    "expected_business_result": f"Scenario {uid} completes without developer help.",
                }
                for uid, mod, title, role, pri in uat_cases
            ],
        },
    )

    w(
        DD / "04_uat_plan_and_report.json",
        {
            "project": PROJECT,
            "group": GROUP,
            "cover": {
                "project_name": "(S)TeemBang — Fitness Tracking Application",
                "document_type": "User Acceptance Test (UAT) Plan & Report",
                "document_status": "Draft",
                "system_basis": "Vue 3 + FastAPI + SQLite",
                "prepared_date": DATE,
                "target_submission_date": DATE,
            },
            "section_1_overview_scope": {
                "title": "1. Project overview and UAT scope",
                "overview_paragraph": "(S)TeemBang helps members track workouts, steps, and goals with dashboard analytics. UAT confirms these flows work for real users without developer assistance.",
                "in_scope_modules": [
                    "Registration, login, logout",
                    "Dashboard, step sync, workout logging",
                    "Goals and analytics trends",
                    "Profile and notifications",
                    "Admin stats and RBAC",
                ],
                "out_of_scope": "Wearables, AI coaching, nutrition, payments, formal load testing.",
            },
            "section_2_objectives": {
                "title": "2. UAT objectives",
                "primary": "Confirm a member tester can track fitness activity and an admin can view platform stats.",
                "secondary": ["Validate mobile-friendly layout", "Collect usability feedback"],
            },
            "section_3_methodology_phases": {
                "title": "3. Methodology",
                "methodology": "Manual scenario-driven UAT via web UI.",
                "phases": [
                    {"phase": "Planning", "output": "Scenario list"},
                    {"phase": "Execution", "output": "Section 11 table"},
                    {"phase": "Sign-off", "output": "Section 14"},
                ],
            },
            "section_4_environment": {
                "title": "4. Environment",
                "rows": [
                    {"item": "System name", "details": "(S)TeemBang"},
                    {"item": "Frontend URL", "details": "http://localhost:5173/"},
                    {"item": "Backend URL", "details": "http://127.0.0.1:8000/"},
                    {"item": "Admin seed", "details": "admin@steambang.com / admin123"},
                    {"item": "Demo member", "details": "demo@steambang.com / demo1234"},
                ],
            },
            "section_5_roles": {
                "title": "5. Roles",
                "rows": [
                    {"role": "UAT coordinator", "person": "Christel", "responsibilities": "Schedule and environment"},
                    {"role": "Member UAT tester", "person": "[External]", "responsibilities": "UAT-SB-001..005"},
                    {"role": "Admin UAT tester", "person": "[External]", "responsibilities": "UAT-SB-006..007"},
                ],
            },
            "section_6_test_cases_summary": {
                "title": "6. UAT summary",
                "columns": ["UAT ID", "Module", "Scenario", "Role", "Priority"],
                "rows": [
                    {"uat_id": u, "module": m, "scenario_title": t, "role": r, "priority": p}
                    for u, m, t, r, p in uat_cases
                ],
            },
            "section_7_defect_severity": {
                "title": "7. Severity",
                "rows": [
                    {"severity": "Critical", "definition": "Cannot log activity or data loss", "action": "Stop until fixed"},
                    {"severity": "High", "definition": "Major feature broken", "action": "Fix before sign-off"},
                    {"severity": "Low", "definition": "Cosmetic", "action": "Defer if needed"},
                ],
            },
            "section_8_schedule": {
                "title": "8. Schedule",
                "rows": [{"date": DATE, "activity": "UAT execution", "responsible": "Team", "output": "Section 11"}],
            },
            "section_9_entry_exit": {
                "title": "9. Entry/exit",
                "entry": [{"criterion": "Build up", "description": "API + UI running"}],
                "exit": [{"criterion": "Scenarios done", "description": "All UAT-SB executed"}],
            },
            "section_10_assumptions_risks": {
                "title": "10. Risks",
                "rows": [{"type": "Risk", "detail": "Local-only demo", "mitigation": "Record evidence"}],
            },
            "section_11_execution_results": {
                "title": "11. Execution results",
                "columns": [
                    "UAT ID",
                    "Scenario",
                    "Tester / role",
                    "Date executed",
                    "Expected business result",
                    "Actual result",
                    "Pass/Fail",
                    "Remarks",
                ],
                "rows": [
                    {
                        "uat_id": u,
                        "scenario": t,
                        "tester_role": "",
                        "date_executed": "",
                        "expected": f"Scenario {u} succeeds.",
                        "actual": "",
                        "pass_fail": "",
                        "remarks": "",
                    }
                    for u, _, t, _, _ in uat_cases
                ],
            },
            "section_12_uat_defects": {
                "title": "12. UAT defects",
                "instruction": "Reference Doc 7.",
                "columns": ["Defect ID", "Related UAT ID", "Description", "Severity", "Status"],
                "rows": [],
            },
            "section_13_feedback": {
                "title": "13. Feedback",
                "columns": ["User / role", "Feedback", "Recommended action", "Status"],
                "rows": [{"user_role": "Member tester", "feedback": "", "recommended_action": "", "status": ""}],
            },
            "section_14_signoff": {
                "title": "14. Sign-off",
                "statement": "Testers confirm scenarios executed as described.",
                "signatures": [
                    {"role": "Member UAT tester", "name_print": "________________", "signature": "________________", "date": "________"},
                    {"role": "Test lead", "name_print": "Christel", "signature": "________________", "date": "________"},
                ],
            },
        },
    )

    defects = [
        ("DEF-001", "Long workout notes overflow on mobile", "Workouts UI", "Medium", "Open"),
        ("DEF-002", "Analytics period change does not refresh chart label", "Analytics", "Low", "In Progress"),
        ("DEF-003", "Step sync shows stale total until manual refresh", "Dashboard", "Medium", "Resolved"),
        ("DEF-004", "Empty state icon oversized on Goals page", "Goals", "Low", "Deferred"),
        ("DEF-005", "Notification list sort confusing", "Notifications", "Low", "Open"),
        ("DEF-006", "Brief flash of admin layout for member URL", "Security", "High", "Retested"),
        ("DEF-007", "Profile save button below fold on short viewport", "Profile", "Medium", "Resolved"),
        ("DEF-008", "Goal progress bar wrong after midnight", "Goals", "Critical", "Closed"),
    ]
    w(
        DD / "05_defect_bug_report_log.json",
        {
            "project": PROJECT,
            "group": GROUP,
            "columns": [
                "Defect ID",
                "Title",
                "Module / Feature",
                "Severity",
                "Priority",
                "Phase Found",
                "Steps to Reproduce",
                "Expected Result",
                "Actual Result",
                "Status",
                "Assigned To",
                "Date Reported",
                "Date Resolved",
                "Evidence (file name or link)",
            ],
            "defects": [
                {
                    "defect_id": did,
                    "title": title,
                    "module_feature": mod,
                    "severity": sev,
                    "priority": "P2",
                    "phase_found": "System",
                    "steps_to_reproduce": ["Reproduce per module."],
                    "expected_result": "Correct UX/API behavior.",
                    "actual_result": "Issue observed during testing.",
                    "status": st,
                    "assigned_to": "Developer",
                    "date_reported": DATE,
                    "date_resolved": DATE if st in ("Resolved", "Closed") else "",
                    "evidence": f"evidence_{did}.png",
                }
                for did, title, mod, sev, st in defects
            ],
        },
    )

    w(
        DD / "06_regression_test_report.json",
        {
            "project": PROJECT,
            "group": GROUP,
            "report_date": DATE,
            "introduction": {
                "title": "Introduction",
                "text": "Regression after fixes for DEF-003, DEF-007, DEF-008 on auth, dashboard, goals, and RBAC paths.",
            },
            "regression_scope": {
                "title": "Regression scope",
                "full_suite_re_run": False,
                "selected_test_case_ids": ["SBR-003", "SBD-002", "SBA-001", "SBG-001", "SBAd-001", "SBS-003", "SBGen-001"],
                "related_defect_ids": ["DEF-003", "DEF-007", "DEF-008"],
            },
            "results_table": {
                "title": "Regression results",
                "columns": ["Test Case ID", "Previous result", "New result", "Pass/Fail", "Tester", "Date", "Notes"],
                "rows": [],
            },
            "automated_regression": {
                "title": "Automated regression",
                "command": "cd steambang_backend && .venv\\Scripts\\python.exe -m pytest tests -q",
                "last_result": "[Fill after pytest]",
                "note": "Attach log if required.",
            },
            "new_defects": {"title": "New defects", "rows": []},
            "summary": {"title": "Summary", "text": "[Fill after regression run]"},
        },
    )

    w(
        DD / "07_test_summary_report.json",
        {
            "project": PROJECT,
            "group": GROUP,
            "report_date": DATE,
            "executive_summary": "Pre-final testing combines pytest API verification, manual Doc 2 cases, UAT, and regression. Update metrics after sync.",
            "scope_and_objectives": {
                "title": "Scope",
                "text": "Validate fitness tracking flows per docs/Project.json; defects in Doc 7; regression in Doc 8.",
            },
            "metrics": {
                "title": "Metrics",
                "test_cases_planned": len(exec_rows),
                "test_cases_executed": "[Fill]",
                "overall_pass_rate_percent": "[Fill]",
                "by_phase": [],
                "defects": {
                    "total_logged": 8,
                    "fixed": "[Fill]",
                    "deferred": "[Fill]",
                    "remaining_open": "[Fill]",
                    "severity_breakdown": {"Critical": "1", "High": "1", "Medium": "3", "Low": "3"},
                },
            },
            "phase_summary": {
                "title": "Phase summary",
                "rows": [
                    {"phase": "System testing", "outcome": "[Fill]", "notes": "Doc 5"},
                    {"phase": "UAT", "outcome": "[Fill]", "notes": "Doc 6"},
                    {"phase": "Regression", "outcome": "[Fill]", "notes": "Doc 8"},
                ],
            },
            "outstanding_issues": {"title": "Outstanding", "rows": []},
            "lessons_learned": {
                "title": "Lessons learned",
                "bullets": [
                    "pytest covered register/activity/goals/dashboard/admin RBAC quickly.",
                    "Syncing results-data with document-data keeps Excel/Word aligned.",
                ],
            },
            "recommendation": {
                "title": "Recommendation",
                "selection": "[Conditional approval / etc.]",
                "rationale": "[Fill after testing]",
            },
            "sign_off": {
                "title": "Sign-off",
                "rows": [{"role": "Test lead", "name": "Christel", "signature": "________________", "date": "________"}],
            },
        },
    )

    w(
        RD_REQ / "04_steambang_project_context.json",
        {
            "source": "docs/Project.json",
            "project": {
                "name": PROJECT,
                "subtitle": "Fitness Tracking Application",
                "group": GROUP,
                "packages": [
                    {"name": "steambang_frontend", "path": "steambang_frontend"},
                    {"name": "steambang_backend", "path": "steambang_backend"},
                ],
            },
            "functional_requirements_for_traceability": [
                "JWT authentication",
                "Activity and workout logging",
                "Step sync",
                "Goals",
                "Dashboard analytics and trends",
                "Profile and notifications",
                "Admin platform stats",
            ],
            "demo_credentials_readme": {
                "admin_email": "admin@steambang.com",
                "admin_password": "admin123",
                "demo_email": "demo@steambang.com",
                "demo_password": "demo1234",
            },
            "team_members": [{"name": n} for n in TEAM],
        },
    )

    w(
        RD_REQ / "06_automated_verification.json",
        {
            "backend_command": "cd steambang_backend && .venv\\Scripts\\python.exe -m pytest tests -v --tb=short",
            "expected_tests": [
                "test_health",
                "test_register_login_dashboard",
                "test_demo_user_seeded",
                "test_admin_stats",
            ],
        },
    )

    w(
        RD_RES / "manifest.json",
        {
            "title": "(S)TeemBang testing — results-data hub",
            "project": PROJECT,
            "group": GROUP,
            "purpose": "Execution outcomes and evidence; sync via ../scripts/sync_results_to_document_data.py",
        },
    )

    w(
        RD_RES / "source_map.json",
        {
            "base": "docs/testing",
            "inputs": ["requirements-data/", "document-data/", "docs/Project.json"],
            "outputs": ["documents/", "results-data/*.json"],
        },
    )

    w(
        RD_RES / "office_artifacts_status.json",
        {
            "description": "Office deliverable status",
            "generated_from": "../document-data/generate_documents.py",
            "artifacts": [
                {"path": f"../documents/Group4_STeemBang_Doc{n}_{name}", "json_source": f"../document-data/{j}", "results_status": "pending", "notes": ""}
                for n, name, j in [
                    (1, "TestPlan.docx", "01_test_plan.json"),
                    (2, "TestCases.xlsx", "02_test_cases_document.json"),
                    (5, "SystemTestReport.docx", "03_system_test_report.json"),
                    (6, "UATPlanReport.docx", "04_uat_plan_and_report.json"),
                    (7, "DefectLog.xlsx", "05_defect_bug_report_log.json"),
                    (8, "RegressionTestReport.docx", "06_regression_test_report.json"),
                    (9, "TestSummaryReport.docx", "07_test_summary_report.json"),
                ]
            ],
        },
    )

    w(
        RD_RES / "automated_runs.json",
        {"description": "pytest run log", "runs": []},
    )

    print("Bootstrap complete:", DD)


if __name__ == "__main__":
    main()
