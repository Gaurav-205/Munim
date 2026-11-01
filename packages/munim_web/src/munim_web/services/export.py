"""The case export ZIP (PRD E5): evidence file, claims with provenance, and the photos.

Photos are the originals byte for byte, except where an Aadhaar number was found: then the
redacted working copy goes in instead, and `photo_is_original` is false.

Built in memory and handed to the browser; nothing is written to the data folder
(docs/SECURITY_PRIVACY.md, "Export"). `case.json` carries `schema` so a reader can tell
versions apart; bump it when a field changes meaning or goes away.
"""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import PurePosixPath
from typing import Any

from munim_web.services.case_service import CaseSnapshot, ref_of
from munim_web.services.papers import MASK_MARK, PaperService

__all__ = ["SCHEMA", "build_zip", "claims_by_paper"]

SCHEMA = "munim-export/1"


def claims_by_paper(snap: CaseSnapshot) -> dict[str, list[dict[str, Any]]]:
    """Every claim with its first read, current value, source, box and findings, per paper."""
    out: dict[str, list[dict[str, Any]]] = {}
    for c in snap.claims:
        ref = ref_of(c)
        box = [c["box_y1"], c["box_x1"], c["box_y2"], c["box_x2"]]
        out.setdefault(c["paper_id"], []).append(
            {
                "id": c["id"],
                "field": ref.field,
                "index": ref.index,
                "value_read": c["value_read"],
                "value_current": c["value_current"],
                "source": c["source"],
                "box": None if None in box else box,
                "findings": [
                    {"rule_id": f.rule_id, "status": str(f.status), "message_key": f.message_key}
                    for f in snap.findings_for(ref)
                ],
            }
        )
    return out


def _redacted(snap: CaseSnapshot, paper_id: str) -> bool:
    """An Aadhaar number was masked in this paper's values, so its original shows it."""
    return any(
        c["paper_id"] == paper_id and MASK_MARK in (c["value_read"] or "") for c in snap.claims
    )


def _photo(snap: CaseSnapshot, paper: Any) -> tuple[str, str]:
    """(name in the ZIP, stored path). The redacted working copy replaces an original that
    shows an Aadhaar number (docs/SECURITY_PRIVACY.md section 5)."""
    stem = f"{paper['kind'] or 'paper'}-{paper['id']}"
    if _redacted(snap, paper["id"]):
        return f"photos/{stem}-aadhaar-hidden.jpg", paper["derived_path"]
    suffix = PurePosixPath(paper["original_path"]).suffix
    return f"originals/{stem}{suffix}", paper["original_path"]


def _clock(snap: CaseSnapshot) -> dict[str, Any]:
    outcome = snap.clock.outcome
    result = outcome.result if outcome else None
    return {
        "as_on": snap.clock.as_on.isoformat(),
        "delivered": snap.clock.delivered.isoformat() if snap.clock.delivered else None,
        "delivered_from": snap.clock.delivered_from,
        "principal_paise": snap.clock.principal_paise,
        "missing": list(snap.clock.missing),
        "provisional": snap.clock.provisional,
        "error_key": outcome.error_key if outcome else None,
        "due_date": result.due_date.isoformat() if result else None,
        "days_late": result.days_late if result else None,
        "cap_applied": result.cap_applied if result else None,
        "interest_paise": result.interest_paise if result else None,
        "total_paise": result.total_paise if result else None,
        "bank_rates_used": [
            {
                "effective_from": r.rate.effective_from.isoformat(),
                "percent": str(r.rate.percent),
                "confirmed": r.confirmed,
            }
            for r in (outcome.rates_used if outcome else ())
        ],
    }


def build_zip(
    snap: CaseSnapshot, papers: PaperService, evidence_html: bytes, meta: dict[str, str]
) -> bytes:
    """The ZIP's bytes. `meta` carries the app version and the export time."""
    claims = claims_by_paper(snap)
    document = {
        "schema": SCHEMA,
        **meta,
        "case": dict(snap.case),
        "papers": [
            {
                "id": p["id"],
                "kind": p["kind"],
                "sha256": p["sha256"],
                "photo": _photo(snap, p)[0],
                "photo_is_original": not _redacted(snap, p["id"]),
                "claims": claims.get(p["id"], []),
            }
            for p in snap.papers
        ],
        "acceptances": [dict(a) for a in snap.acceptance_rows],
        "payments": [dict(p) for p in snap.payments],
        "clock": _clock(snap),
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("case.json", json.dumps(document, ensure_ascii=False, indent=2))
        archive.writestr("evidence.html", evidence_html)
        for p in snap.papers:
            name, stored = _photo(snap, p)
            archive.writestr(name, papers.path(stored).read_bytes())
    return buffer.getvalue()
