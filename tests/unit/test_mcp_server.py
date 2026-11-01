"""The MCP server, driven through the official MCP SDK client (docs/TASKS.md T6.6).

Each tool must give the same answer as the munim_core rule it wraps, so the expected values
below are the golden numbers of docs/DOMAIN_RULES.md, not new ones.
"""

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

import pytest
from mcp import Client, StdioServerParameters

from munim_mcp.server import server
from tests.ref_gstin import check_character

pytestmark = pytest.mark.unit

DEMO_RATE = [{"effective_from": "2000-01-01", "percent": "5.75"}]


async def _call(name: str, arguments: dict[str, Any]) -> tuple[bool, Any]:
    async with Client(server) as client:
        result = await client.call_tool(name, arguments)
    text = result.content[0].text  # type: ignore[union-attr]
    if result.is_error:
        return True, text
    return False, json.loads(text)


def call(name: str, arguments: dict[str, Any]) -> Any:
    is_error, value = asyncio.run(_call(name, arguments))
    assert not is_error, value
    return value


def call_error(name: str, arguments: dict[str, Any]) -> str:
    is_error, value = asyncio.run(_call(name, arguments))
    assert is_error, value
    return str(value)


def test_lists_the_four_tools_from_the_architecture() -> None:
    async def names() -> set[str]:
        async with Client(server) as client:
            return {t.name for t in (await client.list_tools()).tools}

    assert asyncio.run(names()) == {
        "check_gstin",
        "check_invoice_arithmetic",
        "compute_msmed_interest",
        "list_rules",
    }


def test_gstin_passes_and_fails_like_the_core() -> None:
    body = "27AAPFU0939F1Z"  # synthetic
    good = body + check_character(body)
    out = call("check_gstin", {"gstin": good})
    assert out["ok"] is True
    assert out["state_code"] == "27"
    bad = good[:-1] + ("0" if good[-1] != "0" else "1")
    out = call("check_gstin", {"gstin": bad})
    assert out["ok"] is False
    assert "GSTIN-CHECKSUM" in out["errors"]


def test_invoice_total_with_round_off_passes() -> None:
    out = call(
        "check_invoice_arithmetic",
        {
            "taxable_total": "1,00,000.00",
            "cgst": "9,000.00",
            "sgst": "9,000.00",
            "igst": "0",
            "round_off": "-0.40",
            "invoice_total": "1,17,999.60",
        },
    )
    assert out["rule_id"] == "INV-TOTAL"
    assert out["status"] == "passed"


def test_invoice_total_without_round_off_allows_one_rupee() -> None:
    # DOMAIN_RULES INV-TOTAL: no round-off line printed, the sum may differ by up to 1.00.
    args = {"taxable_total": "1000.00", "cgst": "90.00", "sgst": "90.00", "igst": "0"}
    assert call("check_invoice_arithmetic", {**args, "invoice_total": "1181.00"})["status"] == (
        "passed"
    )
    out = call("check_invoice_arithmetic", {**args, "invoice_total": "1181.01"})
    assert out["status"] == "failed"
    assert out["params"] == {"computed_paise": "118000", "printed_paise": "118101"}


def test_invoice_total_refuses_a_round_off_of_a_rupee_or_more() -> None:
    out = call(
        "check_invoice_arithmetic",
        {
            "taxable_total": "1000.00",
            "cgst": "0",
            "sgst": "0",
            "igst": "180.00",
            "round_off": "1.00",
            "invoice_total": "1181.00",
        },
    )
    assert out["status"] == "failed"


def test_unreadable_amount_is_skipped_not_guessed() -> None:
    out = call(
        "check_invoice_arithmetic",
        {"taxable_total": "abc", "cgst": "0", "sgst": "0", "igst": "0", "invoice_total": "1"},
    )
    assert out["status"] == "skipped"


def test_interest_matches_the_golden_demo_case() -> None:
    out = call(
        "compute_msmed_interest",
        {
            "principal_paise": 50_000_000,
            "acceptance_date": "2026-03-20",
            "agreement": "written",
            "credit_days": 30,
            "as_on": "2026-10-13",
            "bank_rates": DEMO_RATE,
        },
    )
    assert out["due_date"] == "2026-04-19"
    assert out["days_late"] == 177
    assert out["interest_paise"] == 4_290_370
    assert out["total_paise"] == 54_290_370
    assert out["interest_formatted"] == "₹42,903.70"
    assert out["cap_applied"] is False


def test_interest_needs_a_bank_rate_from_the_caller() -> None:
    args = {
        "principal_paise": 100,
        "acceptance_date": "2026-03-20",
        "agreement": "none",
        "as_on": "2026-10-13",
    }
    call_error("compute_msmed_interest", args)
    assert "Bank Rate" in call_error("compute_msmed_interest", {**args, "bank_rates": []})


def test_interest_refuses_a_written_agreement_without_days() -> None:
    call_error(
        "compute_msmed_interest",
        {
            "principal_paise": 100,
            "acceptance_date": "2026-03-20",
            "agreement": "written",
            "as_on": "2026-10-13",
            "bank_rates": DEMO_RATE,
        },
    )


def test_interest_refuses_float_money() -> None:
    call_error(
        "compute_msmed_interest",
        {
            "principal_paise": 100.5,
            "acceptance_date": "2026-03-20",
            "agreement": "none",
            "as_on": "2026-10-13",
            "bank_rates": DEMO_RATE,
        },
    )


def test_list_rules_is_the_core_catalogue() -> None:
    from munim_core.verify.catalog import RULES

    rules = call("list_rules", {})["rules"]
    assert [r["rule_id"] for r in rules] == list(RULES)
    assert {"rule_id": "INV-TOTAL", "version": "1.0", "family": "invoice"}.items() <= next(
        r for r in rules if r["rule_id"] == "INV-TOTAL"
    ).items()


def test_stdio_subprocess_round_trip() -> None:
    """The installed entry point speaks MCP over stdio to a real SDK client."""

    async def run() -> Any:
        params = StdioServerParameters(command=sys.executable, args=["-m", "munim_mcp.server"])
        async with Client(params) as client:
            result = await client.call_tool("check_gstin", {"gstin": "not a gstin"})
            return json.loads(result.content[0].text)  # type: ignore[union-attr]

    assert asyncio.run(run())["ok"] is False


@pytest.mark.parametrize("percent", ["abc", "NaN", "-1", "Infinity"])
def test_interest_refuses_a_rate_that_is_not_a_percent(percent: str) -> None:
    message = call_error(
        "compute_msmed_interest",
        {
            "principal_paise": 100,
            "acceptance_date": "2026-03-20",
            "agreement": "none",
            "as_on": "2026-10-13",
            "bank_rates": [{"effective_from": "2000-01-01", "percent": percent}],
        },
    )
    assert "Bank Rate percent" in message


def test_interest_refuses_two_rates_on_the_same_day() -> None:
    # Otherwise the answer would depend on the order of the rows (domain review).
    message = call_error(
        "compute_msmed_interest",
        {
            "principal_paise": 50_000_000,
            "acceptance_date": "2026-03-20",
            "agreement": "written",
            "credit_days": 30,
            "as_on": "2026-10-13",
            "bank_rates": [
                {"effective_from": "2025-06-06", "percent": "5.75"},
                {"effective_from": "2025-06-06", "percent": "9"},
            ],
        },
    )
    assert "2025-06-06" in message


def test_interest_says_which_bank_rates_it_used() -> None:
    out = call(
        "compute_msmed_interest",
        {
            "principal_paise": 50_000_000,
            "acceptance_date": "2026-03-20",
            "agreement": "written",
            "credit_days": 30,
            "as_on": "2026-10-13",
            "bank_rates": [
                {"effective_from": "2025-06-06", "percent": "5.75"},
                {"effective_from": "2025-12-05", "percent": "5.50"},
                {"effective_from": "2026-10-07", "percent": "5.75"},
            ],
        },
    )
    # docs/DOMAIN_RULES.md 5.4: every demo period starts before 7 Oct 2026, so 5.50% applies.
    assert out["interest_paise"] == 4_097_671
    assert out["bank_rates_used"] == [{"effective_from": "2025-12-05", "percent": "5.50"}]
