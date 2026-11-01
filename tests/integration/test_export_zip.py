"""ZIP export (PRD E5, docs/API.md `GET /cases/{id}/export.zip`, T6.8).

The ZIP holds the evidence file as HTML, every claim with its provenance as versioned JSON, and
the original photos byte for byte. It is built in memory: the app does not keep a copy
(docs/SECURITY_PRIVACY.md, "Export").
"""

from __future__ import annotations

import hashlib
import io
import json
import zipfile

import pytest

from tests.integration.test_web_flow import DEMO, Web, demo_case, web  # noqa: F401

pytestmark = pytest.mark.integration


def _export(web: Web, case_id: str) -> zipfile.ZipFile:  # noqa: F811
    r = web.client.get(f"/cases/{case_id}/export.zip")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/zip"
    assert r.headers["content-disposition"] == f'attachment; filename="munim-{case_id}.zip"'
    assert r.headers["cache-control"] == "no-store"
    return zipfile.ZipFile(io.BytesIO(r.content))


def test_export_holds_evidence_claims_and_originals(web: Web) -> None:  # noqa: F811
    case_id, papers = demo_case(web)
    web.post(
        f"/cases/{case_id}/settings",
        {"agreement": "written", "credit_days": "30", "as_on_date": "13/10/2026"},
    )
    archive = _export(web, case_id)
    names = set(archive.namelist())
    assert names == {
        "case.json",
        "evidence.html",
        *(f"originals/{kind}-{pid}.jpg" for kind, pid in papers.items()),
    }

    for kind, pid in papers.items():
        stored = archive.read(f"originals/{kind}-{pid}.jpg")
        assert stored == (DEMO / f"{kind}.jpg").read_bytes()

    data = json.loads(archive.read("case.json"))
    assert data["schema"] == "munim-export/1"
    assert data["case"]["id"] == case_id
    by_kind = {p["kind"]: p for p in data["papers"]}
    invoice = by_kind["invoice"]
    assert invoice["sha256"] == hashlib.sha256((DEMO / "invoice.jpg").read_bytes()).hexdigest()
    assert invoice["original"] == f"originals/invoice-{papers['invoice']}.jpg"
    gstin = next(c for c in invoice["claims"] if c["field"] == "buyer_gstin")
    assert gstin["source"] == "repair"
    assert gstin["value_read"] != gstin["value_current"]
    assert any(f["rule_id"] == "GSTIN-CHECKSUM" for f in gstin["findings"])
    # Golden: the demo case on the seeded Bank Rate table (docs/DOMAIN_RULES.md).
    assert data["clock"]["interest_paise"] == 4_097_671
    assert data["clock"]["days_late"] == 177

    evidence = archive.read("evidence.html").decode("utf-8")
    assert "₹40,976.71" in evidence


def test_export_keeps_no_copy_and_logs_an_event(web: Web) -> None:  # noqa: F811
    case_id = web.new_case()
    before = sorted(p.name for p in web.app.state.settings.data_dir.rglob("*"))
    archive = _export(web, case_id)
    assert json.loads(archive.read("case.json"))["papers"] == []
    after = sorted(p.name for p in web.app.state.settings.data_dir.rglob("*"))
    assert [n for n in after if n.endswith(".zip")] == []
    assert len(after) - len(before) <= 2  # SQLite journal files only
    events = web.app.state.db.all(
        "SELECT kind FROM events WHERE case_id = ? ORDER BY rowid", (case_id,)
    )
    assert "export.downloaded" in [e["kind"] for e in events]


def test_export_of_an_unknown_case_is_404(web: Web) -> None:  # noqa: F811
    assert web.client.get("/cases/nope/export.zip").status_code == 404


def test_evidence_file_links_to_the_export(web: Web) -> None:  # noqa: F811
    case_id = web.new_case()
    page = web.client.get(f"/cases/{case_id}/dossier").text
    assert f'href="/cases/{case_id}/export.zip"' in page


def test_the_bundled_ifsc_list_reaches_the_rules(web: Web) -> None:  # noqa: F811
    # rules/ifsc.json is razorpay/ifsc v2.0.62; SBIN0001234 is the demo invoice's bank branch.
    known = web.app.state.db.known_ifsc
    assert known is not None and len(known) == 183_214
    case_id, papers = demo_case(web)
    data = json.loads(_export(web, case_id).read("case.json"))
    invoice = next(p for p in data["papers"] if p["kind"] == "invoice")
    ifsc = next(c for c in invoice["claims"] if c["field"] == "bank_ifsc")
    assert ifsc["value_current"] == "SBIN0001234"
    assert [f["status"] for f in ifsc["findings"] if f["rule_id"] == "IFSC-KNOWN"] == ["passed"]
