"""Dashboard totals and workbench steps (munim_web.services.views)."""

from __future__ import annotations

import pytest

from munim_web.services.views import dashboard, progress

pytestmark = pytest.mark.unit


def row(
    owed: int | None, interest: int | None, days: int | None, open_: int = 0
) -> dict[str, object]:
    return {"owed": owed, "interest": interest, "days_late": days, "open": open_}


def test_totals_are_exact_paise_and_skip_cases_without_an_amount() -> None:
    rows = [row(54097671, 4097671, 177, 2), row(None, None, None, 1), row(100, 0, 0)]
    assert dashboard(rows) == {  # type: ignore[arg-type]
        "cases": 3,
        "owed": 54097771,
        "interest": 4097671,
        "late": 1,
        "open": 3,
        "unconfirmed": False,
    }


def test_no_cases_add_up_to_zero() -> None:
    assert dashboard([]) == {
        "cases": 0,
        "owed": 0,
        "interest": 0,
        "late": 0,
        "open": 0,
        "unconfirmed": False,
    }


def test_one_unconfirmed_bank_rate_marks_the_total() -> None:
    rows = [row(100, 0, 0), {**row(200, 50, 3), "unconfirmed_rate": True}]
    assert dashboard(rows)["unconfirmed"] is True  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("flags", "expected"),
    [
        ((False, False, False, False), ["current", "todo", "todo", "todo"]),
        ((True, False, False, False), ["done", "current", "todo", "todo"]),
        ((True, True, False, False), ["done", "done", "current", "todo"]),
        ((True, True, True, False), ["done", "done", "done", "current"]),
        ((True, True, True, True), ["done", "done", "done", "done"]),
        ((True, False, True, False), ["done", "current", "done", "todo"]),
    ],
)
def test_first_step_not_done_is_current(flags: tuple[bool, ...], expected: list[str]) -> None:
    papers, values, terms, confirmed = flags
    steps = progress(papers=papers, values=values, terms=terms, confirmed=confirmed)
    assert [s["state"] for s in steps] == expected
    assert [s["key"] for s in steps] == ["papers", "values", "terms", "confirm"]
