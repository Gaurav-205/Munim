"""The hosted demo entry point (api/index.py): own hosts only, reader pinned to replay."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]

pytestmark = pytest.mark.integration


def _load_entry(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, **env: str) -> ModuleType:
    monkeypatch.setenv("MUNIM_DATA_DIR", str(tmp_path))
    for name in (
        "MUNIM_PUBLIC_HOST",
        "VERCEL_URL",
        "VERCEL_BRANCH_URL",
        "VERCEL_PROJECT_PRODUCTION_URL",
        "MUNIM_PROVIDER",
    ):
        monkeypatch.delenv(name, raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    spec = importlib.util.spec_from_file_location("munim_vercel_entry", ROOT / "api" / "index.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_default_host_is_the_demo_domain(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    entry = _load_entry(monkeypatch, tmp_path)
    assert entry.deploy_hosts({}) == ("munim-demo.vercel.app",)


def test_vercel_and_override_hosts_are_added(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    entry = _load_entry(monkeypatch, tmp_path)
    hosts = entry.deploy_hosts(
        {
            "MUNIM_PUBLIC_HOST": "Munim.example.in, www.munim.example.in",
            "VERCEL_URL": "munim-demo-abc123.vercel.app",
            "VERCEL_PROJECT_PRODUCTION_URL": "munim-demo.vercel.app",
            "VERCEL_BRANCH_URL": "",
        }
    )
    assert hosts == (
        "munim-demo-abc123.vercel.app",
        "munim-demo.vercel.app",
        "munim.example.in",
        "www.munim.example.in",
    )
    assert "*" not in hosts


def test_wildcard_is_never_accepted(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    entry = _load_entry(monkeypatch, tmp_path)
    assert entry.deploy_hosts({"MUNIM_PUBLIC_HOST": "*"}) == ("munim-demo.vercel.app",)


def test_foreign_host_is_refused_and_reader_is_replay(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    entry = _load_entry(monkeypatch, tmp_path, VERCEL_URL="munim-demo-abc123.vercel.app")
    assert entry.settings.provider == "replay"
    with TestClient(entry.app, base_url="https://munim-demo.vercel.app") as client:
        health = client.get("/healthz")
        assert health.status_code == 200
        assert health.json()["provider"] == "replay"
        own = client.get("/healthz", headers={"host": "munim-demo-abc123.vercel.app"})
        assert own.status_code == 200
        refused = client.get("/healthz", headers={"host": "evil.example"})
        assert refused.status_code == 400
        assert refused.content == b"Bad Host header"


def test_provider_env_cannot_unpin_replay(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    entry = _load_entry(monkeypatch, tmp_path, MUNIM_PROVIDER="gemini")
    assert entry.settings.provider == "replay"


def test_upload_limit_fits_vercel_body_cap(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # Vercel refuses request bodies over 4.5 MB with its own page, before the app sees them.
    entry = _load_entry(monkeypatch, tmp_path)
    limit = entry.settings.max_upload_bytes
    assert limit + 64 * 1024 < 4_500_000
    with TestClient(entry.app, base_url="https://munim-demo.vercel.app") as client:
        client.get("/")
        token = client.cookies.get("munim_csrf_8765")
        fields = {"title": "t", "supplier_name": "s", "buyer_name": "b", "csrf_token": token}
        case = client.post("/cases", data=fields, follow_redirects=False)
        page = client.get(case.headers["location"] + "?error=paper.err.size")
    assert f"larger than {limit // (1024 * 1024)} MB" in page.text


def _demo_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> tuple[ModuleType, TestClient]:
    entry = _load_entry(monkeypatch, tmp_path)
    return entry, TestClient(entry.app, base_url="https://munim-demo.vercel.app")


def _new_case(client: TestClient) -> tuple[str, str]:
    client.get("/")
    token = str(client.cookies.get("munim_csrf_8765"))
    fields = {"title": "t", "supplier_name": "s", "buyer_name": "b", "csrf_token": token}
    case = client.post("/cases", data=fields, follow_redirects=False)
    return case.headers["location"].split("/cases/")[1].split("?")[0], token


def test_demo_refuses_visitor_uploads(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # Visitors share one database on the hosted demo, so their own photos must never land there.
    entry, client = _demo_client(monkeypatch, tmp_path)
    with client:
        case_id, token = _new_case(client)
        photo = (ROOT / "eval/fixtures/demo/invoice.jpg").read_bytes()
        r = client.post(
            f"/cases/{case_id}/papers",
            data={"kind": "invoice", "csrf_token": token},
            files={"file": ("x.jpg", photo, "image/jpeg")},
            follow_redirects=False,
        )
        assert r.status_code == 303
        assert "error=paper.err.demo" in r.headers["location"]
        assert entry.app.app.state.db.papers(case_id) == []
        page = client.get(f"/cases/{case_id}").text
        assert 'type="file"' not in page
        assert f'action="/cases/{case_id}/samples"' in page


def test_demo_adds_the_sample_papers_and_exports_under_the_vercel_cap(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    import hashlib

    entry, client = _demo_client(monkeypatch, tmp_path)
    with client:
        case_id, token = _new_case(client)
        r = client.post(
            f"/cases/{case_id}/samples", data={"csrf_token": token}, follow_redirects=False
        )
        assert r.status_code == 303
        papers = entry.app.app.state.db.papers(case_id)
        assert {p["kind"]: p["sha256"] for p in papers} == {
            kind: hashlib.sha256((ROOT / f"eval/fixtures/demo/{kind}.jpg").read_bytes()).hexdigest()
            for kind in ("invoice", "challan", "po")
        }
        export = client.get(f"/cases/{case_id}/export.zip")
        assert export.status_code == 200
        assert len(export.content) < 4_500_000


def test_samples_route_is_off_outside_the_demo(tmp_path: Path) -> None:
    from munim_web.main import create_app
    from munim_web.settings import Settings

    app = create_app(Settings(data_dir=tmp_path, provider="replay"))
    with TestClient(app, base_url="http://127.0.0.1:8765") as client:
        case_id, token = _new_case(client)
        r = client.post(
            f"/cases/{case_id}/samples", data={"csrf_token": token}, follow_redirects=False
        )
        assert r.status_code == 404
