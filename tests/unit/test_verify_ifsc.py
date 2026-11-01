"""IFSC-KNOWN (docs/DOMAIN_RULES.md 3.1, PRD C8): pass, fail, boundary and skipped.

The bank list is the razorpay/ifsc dataset, loaded by the web layer and handed to the core as
a set, so the core stays pure. These tests use a small synthetic list.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from munim_core.ids import check_ifsc_format, ifsc_codes
from munim_core.verify import run_all
from munim_core.verify.models import FieldRef, Severity, Status
from tests.unit.verify_helpers import TODAY, case, invoice, only

pytestmark = pytest.mark.unit

KNOWN = frozenset({"SBIN0000001", "ABCD0123456"})  # synthetic list


def ifsc_findings(value: str | None, known: frozenset[str] | None = KNOWN):
    state = replace(case(inv=invoice(bank_ifsc=value)), known_ifsc=known)
    return only(run_all(state, TODAY), "IFSC-KNOWN")


def test_ifsc_in_the_list_passes() -> None:
    [f] = ifsc_findings("SBIN0000001")
    assert f.status is Status.PASSED
    assert f.fields == (FieldRef("invoice", "bank_ifsc"),)


def test_ifsc_is_tidied_like_the_paper_prints_it() -> None:
    [f] = ifsc_findings(" abcd 0123456 ")
    assert f.status is Status.PASSED


def test_well_formed_ifsc_missing_from_the_list_needs_a_look() -> None:
    [f] = ifsc_findings("SBIN0999999")
    assert f.status is Status.NEEDS_REVIEW
    assert f.severity is Severity.WARNING
    assert f.message_key == "rule.IFSC-KNOWN"
    assert f.params == {"printed": "SBIN0999999"}


@pytest.mark.parametrize(
    "value",
    [
        "SBIN1000001",  # fifth character must be zero
        "SBI00000001",  # four letters first
        "SBIN000001",  # 10 characters
        "SBIN00000012",  # 12 characters
        "SBIN0-00001",
    ],
)
def test_badly_formed_ifsc_fails(value: str) -> None:
    [f] = ifsc_findings(value)
    assert f.status is Status.FAILED
    assert f.severity is Severity.WARNING
    assert f.message_key == "rule.IFSC-KNOWN.format"


def test_no_value_or_no_list_is_skipped() -> None:
    assert [f.status for f in ifsc_findings(None)] == [Status.SKIPPED]
    assert [f.status for f in ifsc_findings("SBIN0000001", known=None)] == [Status.SKIPPED]


def test_bad_format_fails_even_without_the_list() -> None:
    assert [f.status for f in ifsc_findings("SBIN1000001", known=None)] == [Status.FAILED]


def test_no_finding_when_the_invoice_has_no_ifsc_field() -> None:
    assert only(run_all(case(inv=invoice()), TODAY), "IFSC-KNOWN") == []


def test_format_boundary_accepts_letters_in_the_branch_part() -> None:
    assert check_ifsc_format("HDFC0CAGSBK")
    assert not check_ifsc_format("HDFC0CAGSB")


def test_razorpay_layout_expands_to_codes() -> None:
    # IFSC.json maps a bank code to branch suffixes; numbers are zero-padded to six.
    codes = ifsc_codes({"ABCD": [1, 123456, "NEFT02"], "WXYZ": []})
    assert codes == frozenset({"ABCD0000001", "ABCD0123456", "ABCD0NEFT02"})
