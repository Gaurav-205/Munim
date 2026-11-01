"""Aadhaar pixel blur (docs/SECURITY_PRIVACY.md section 5, T6.8).

When a read masks an Aadhaar number, the box it came from is pixelated in the derived image,
the one the app shows and crops. The original upload is kept byte for byte as evidence.
"""

from __future__ import annotations

import io
import json
from typing import Any

import pytest
from PIL import Image

from munim_ai.extract import ExtractOutcome
from munim_ai.normalize import ClaimDraft
from tests.integration.test_web_flow import DEMO, Web, web  # noqa: F401

pytestmark = pytest.mark.integration

BOX = (100, 100, 200, 600)  # y1, x1, y2, x2 on the 0-1000 grid


def _outcome(masked: bool) -> ExtractOutcome:
    draft = ClaimDraft(
        field="supplier_name",
        index=None,
        value_read="Aadhaar XXXX XXXX 0124" if masked else "Sample Fabricators",
        value="Aadhaar XXXX XXXX 0124" if masked else "Sample Fabricators",
        box=BOX,
        masked=masked,
    )
    return ExtractOutcome(
        claims=(draft,), ok=True, partial=False, attempts=1, invalid_attempts=0, result=None
    )


def _read_with(web: Web, monkeypatch: pytest.MonkeyPatch, masked: bool) -> Any:  # noqa: F811
    async def fake_extract(*_: object, **__: object) -> ExtractOutcome:
        return _outcome(masked)

    monkeypatch.setattr("munim_web.services.papers.extract_paper", fake_extract)
    case_id = web.new_case()
    paper_id = web.upload(case_id, "invoice")
    papers = web.app.state.papers
    paper = web.app.state.db.paper(paper_id)
    derived_before = papers.path(paper["derived_path"]).read_bytes()
    web.read(paper_id)
    return case_id, paper, derived_before


def _pixels(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data)).convert("L")


def test_masked_aadhaar_box_is_pixelated_in_the_derived_image_only(
    web: Web,  # noqa: F811
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case_id, paper, derived_before = _read_with(web, monkeypatch, masked=True)
    papers = web.app.state.papers
    assert papers.path(paper["original_path"]).read_bytes() == (DEMO / "invoice.jpg").read_bytes()
    derived_after = papers.path(paper["derived_path"]).read_bytes()
    assert derived_after != derived_before
    before, after = _pixels(derived_before), _pixels(derived_after)
    w, h = after.size
    inside = (int(0.15 * w), int(0.12 * h), int(0.55 * w), int(0.18 * h))
    # Pixelated: within the box there are far fewer distinct grey levels than before.
    assert (
        len(set(after.crop(inside).get_flattened_data()))
        < len(set(before.crop(inside).get_flattened_data())) / 3
    )

    events = web.app.state.db.all(
        "SELECT kind, detail_json FROM events WHERE case_id = ? AND kind = ?",
        (case_id, "paper.aadhaar_blurred"),
    )
    assert [json.loads(e["detail_json"]) for e in events] == [
        {"paper": paper["id"], "boxes": 1, "without_box": 0}
    ]
    assert "0124" not in events[0]["detail_json"]  # ids and counts only, never the value


def test_a_read_with_no_aadhaar_leaves_the_derived_image_alone(
    web: Web,  # noqa: F811
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, paper, derived_before = _read_with(web, monkeypatch, masked=False)
    papers = web.app.state.papers
    assert papers.path(paper["derived_path"]).read_bytes() == derived_before


def test_startup_sweep_masks_numbers_stored_before_the_wider_pattern(
    web: Web,  # noqa: F811
) -> None:
    case_id = web.new_case()
    paper_id = web.upload(case_id, "invoice")
    db = web.app.state.db
    db.replace_claims(
        paper_id,
        [{"field": "supplier_name", "line_index": -1, "value_read": None, "value": None}],
    )
    old = "Aadhaar 2345  6789  0124"  # synthetic test number, double spaces: missed before
    db.run(
        "UPDATE claims SET value_read = ?, value_current = ? WHERE paper_id = ?",
        (old, old, paper_id),
    )
    assert db.remask_aadhaar() == 1
    row = db.one("SELECT value_read, value_current FROM claims WHERE paper_id = ?", (paper_id,))
    assert row["value_read"] == row["value_current"] == "Aadhaar XXXX XXXX 0124"
    assert db.remask_aadhaar() == 0  # idempotent


def test_rotating_a_paper_keeps_the_aadhaar_box_pixelated(
    web: Web,  # noqa: F811
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from munim_ai import imageprep

    _, paper, _ = _read_with(web, monkeypatch, masked=True)
    r = web.post(f"/papers/{paper['id']}/rotate?deg=90")
    assert r.status_code == 303
    papers = web.app.state.papers
    plain = imageprep.prepare(papers.path(paper["original_path"]).read_bytes(), 90).jpeg
    after = _pixels(papers.path(paper["derived_path"]).read_bytes())
    fresh = _pixels(plain)
    y1, x1, y2, x2 = imageprep.rotate_box(BOX, 90)
    w, h = after.size
    inside = (x1 * w // 1000, y1 * h // 1000, x2 * w // 1000, y2 * h // 1000)
    assert len(set(after.crop(inside).get_flattened_data())) < (
        len(set(fresh.crop(inside).get_flattened_data())) / 3
    )


def test_export_ships_the_redacted_photo_when_an_aadhaar_was_found(
    web: Web,  # noqa: F811
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import zipfile

    case_id, paper, _ = _read_with(web, monkeypatch, masked=True)
    r = web.client.get(f"/cases/{case_id}/export.zip")
    archive = zipfile.ZipFile(io.BytesIO(r.content))
    name = f"photos/invoice-{paper['id']}-aadhaar-hidden.jpg"
    assert name in archive.namelist()
    assert not [n for n in archive.namelist() if n.startswith("originals/")]
    papers = web.app.state.papers
    assert archive.read(name) == papers.path(paper["derived_path"]).read_bytes()
    entry = json.loads(archive.read("case.json"))["papers"][0]
    assert (entry["photo"], entry["photo_is_original"]) == (name, False)
