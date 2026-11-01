"""MCP server exposing Munim's deterministic checks (docs/ARCHITECTURE.md, PRD F4).

Every tool is a thin wrapper over munim_core, so it answers exactly as the app does. There is
no document upload tool, by design (privacy). Run it with `munim-mcp` (stdio).
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Literal

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel, StrictInt

from munim_core.clock import BankRate, ClockInput, Step, compute
from munim_core.ids import check_gstin as core_check_gstin
from munim_core.money import format_inr
from munim_core.verify.catalog import RULES
from munim_core.verify.invoice import total
from munim_core.verify.models import ClaimValue, PaperState

__all__ = ["main", "server"]

server = MCPServer(
    "munim-mcp",
    instructions=(
        "Deterministic Indian invoice checks and the MSMED Act payment clock. A 'passed' "
        "result means the rule's computation succeeded on the values given; it does not prove "
        "the values are true."
    ),
)


class RateRow(BaseModel):
    effective_from: date
    percent: str


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


@server.tool()
def check_gstin(gstin: str) -> str:
    """Check a GSTIN's format, state code, embedded PAN and mod-36 check character."""
    res = core_check_gstin(gstin)
    return _json(
        {
            "ok": res.ok,
            "errors": list(res.errors),
            "normalised": res.normalised,
            "normalisation_applied": res.normalisation_applied,
            "state_code": res.state_code,
            "pan": res.pan,
        }
    )


@server.tool()
def check_invoice_arithmetic(
    *,
    taxable_total: str,
    cgst: str,
    sgst: str,
    igst: str,
    invoice_total: str,
    round_off: str | None = None,
) -> str:
    """Rule INV-TOTAL: taxable total + CGST + SGST + IGST (+ round-off) against the printed total.

    Give amounts in rupees as printed (for example "1,17,999.60"). Leave round_off out when the
    invoice prints no round-off line: then the sum may differ from the total by up to 1.00.
    """
    texts = {
        "taxable_total": taxable_total,
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "invoice_total": invoice_total,
        "round_off": round_off,
    }
    fields = {
        k: ClaimValue(raw=v, text=v, source="user") for k, v in texts.items() if v is not None
    }
    finding = total(PaperState(kind="invoice", fields=fields))
    return _json(
        {
            "rule_id": finding.rule_id,
            "rule_version": finding.rule_version,
            "status": str(finding.status),
            "params": dict(finding.params),
        }
    )


@server.tool()
def compute_msmed_interest(
    *,
    principal_paise: StrictInt,
    acceptance_date: date,
    agreement: Literal["written", "none"],
    as_on: date,
    bank_rates: list[RateRow],
    credit_days: StrictInt | None = None,
) -> str:
    """MSMED Act sections 15 and 16: due date, days late, and compound interest with monthly rests.

    The rate is three times the RBI Bank Rate in force. Munim does not assume one: pass the
    Bank Rate table as rows of effective_from (YYYY-MM-DD) and percent (for example "5.75").
    """
    if not bank_rates:
        raise ToolError("give at least one Bank Rate row; Munim does not assume a rate")
    days = [r.effective_from for r in bank_rates]
    repeated = sorted({d for d in days if days.count(d) > 1})
    if repeated:
        raise ToolError(f"two Bank Rate rows start on {repeated[0].isoformat()}; keep one")
    try:
        percents = [Decimal(r.percent) for r in bank_rates]
    except InvalidOperation as exc:
        raise ToolError("a Bank Rate percent must be a number such as 5.75") from exc
    if not all(p.is_finite() and 0 <= p < 100 for p in percents):
        raise ToolError("a Bank Rate percent must be a number such as 5.75")
    rates = tuple(BankRate(r.effective_from, p) for r, p in zip(bank_rates, percents, strict=True))
    try:
        res = compute(
            ClockInput(
                acceptance_date=acceptance_date,
                agreement=agreement,
                credit_days=credit_days,
                principal_paise=principal_paise,
                as_on=as_on,
                rates=rates,
            )
        )
    except ValueError as exc:  # the clock's own refusals: no rate in force, missing days
        raise ToolError(str(exc)) from exc
    return _json(
        {
            "due_date": res.due_date.isoformat(),
            "as_on": as_on.isoformat(),
            "days_late": res.days_late,
            "cap_applied": res.cap_applied,
            "basis": res.basis_key,
            "principal_paise": principal_paise,
            "interest_paise": res.interest_paise,
            "total_paise": res.total_paise,
            "interest_formatted": format_inr(res.interest_paise),
            "total_formatted": format_inr(res.total_paise),
            "monthly_rests": sum(1 for s in res.steps if s.kind == "month"),
            "bank_rates_used": _rates_used(res.steps),
        }
    )


def _rates_used(steps: Sequence[Step]) -> list[dict[str, str]]:
    """The Bank Rate rows the working used, in order, once each."""
    seen: dict[date, str] = {}
    for s in steps:
        if s.rate_effective_from is not None and s.bank_rate_percent is not None:
            seen.setdefault(s.rate_effective_from, str(s.bank_rate_percent))
    return [{"effective_from": d.isoformat(), "percent": p} for d, p in seen.items()]


@server.tool()
def list_rules() -> str:
    """The rule catalogue: id, version, family and usual severity of every Munim rule."""
    rules = [
        {
            "rule_id": r.rule_id,
            "version": r.version,
            "family": r.family,
            "severity": str(r.severity),
        }
        for r in RULES.values()
    ]
    return _json({"rules": rules})


def main() -> None:
    server.run("stdio")


if __name__ == "__main__":
    main()
