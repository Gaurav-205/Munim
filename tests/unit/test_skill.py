"""skills/munim-checks/SKILL.md (T6.7): the Agent Skills frontmatter rules, and the tool list.

CI also runs the reference validator (`skills-ref validate`); this test keeps the same rules
in the local suite and keeps the skill's tool table in step with the MCP server.
"""

from __future__ import annotations

import asyncio
import re
from pathlib import Path

import pytest
import yaml
from mcp import Client

from munim_mcp.server import server

pytestmark = pytest.mark.unit

SKILL_DIR = Path(__file__).resolve().parents[2] / "skills" / "munim-checks"
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def _frontmatter() -> tuple[dict[str, object], str]:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    assert match, "SKILL.md must start with YAML frontmatter between --- lines"
    return yaml.safe_load(match.group(1)), match.group(2)


def test_frontmatter_follows_the_agent_skills_spec() -> None:
    meta, body = _frontmatter()
    assert set(meta) <= ALLOWED_KEYS
    name = str(meta["name"])
    assert name == SKILL_DIR.name
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64
    description = str(meta["description"])
    assert 0 < len(description) <= 1024
    assert len(str(meta.get("compatibility", ""))) <= 500
    assert body.strip()


def test_skill_names_exactly_the_server_tools() -> None:
    async def tools() -> set[str]:
        async with Client(server) as client:
            return {t.name for t in (await client.list_tools()).tools}

    _, body = _frontmatter()
    table = set(re.findall(r"^\| `([a-z_]+)` \|", body, re.MULTILINE))
    assert table == asyncio.run(tools())


def test_skill_says_passed_never_verified_as_a_result() -> None:
    _, body = _frontmatter()
    assert 'never "verified"' in body
    assert not re.search(r"\bis verified\b|\bwas verified\b", body, re.IGNORECASE)
