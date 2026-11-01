---
name: munim-checks
description: Deterministic checks for Indian tax invoices and the MSMED Act payment clock. Use when asked whether a GSTIN is well formed, whether an invoice's taxable value, CGST, SGST, IGST and round-off add up to its total, or how much interest a buyer owes a micro or small supplier for late payment under sections 15 and 16 of the MSMED Act, 2006. Needs the munim-mcp server.
license: Apache-2.0
compatibility: Needs the munim-mcp MCP server from https://github.com/Gaurav-205/Munim (stdio, run with uv).
---

# Munim checks

These tools run Munim's rules in code. Use them instead of doing the arithmetic or the checksum yourself, and report their answer as given.

## Tools (server `munim-mcp`)

| Tool | Use it for | Arguments |
| --- | --- | --- |
| `check_gstin` | Format, state code, embedded PAN and mod-36 check character of a GSTIN | `gstin` |
| `check_invoice_arithmetic` | Rule INV-TOTAL: taxable total + CGST + SGST + IGST (+ round-off) against the printed total | `taxable_total`, `cgst`, `sgst`, `igst`, `invoice_total`, optional `round_off`, all in rupees as printed, for example `"1,17,999.60"` |
| `compute_msmed_interest` | Due date, days late, and compound interest with monthly rests at three times the RBI Bank Rate | `principal_paise` (integer), `acceptance_date`, `as_on` (YYYY-MM-DD), `agreement` (`"written"` or `"none"`), `credit_days` when written, `bank_rates` |
| `list_rules` | The rule ids, versions and families, to cite a rule | none |

## How to use them

1. Copy values exactly as printed. Do not correct a GSTIN or an amount before checking it; the point is to test what is on the paper.
2. For `check_invoice_arithmetic`, leave `round_off` out when the invoice prints no round-off line. That changes the tolerance (1 paisa with a round-off line, 1.00 without), so do not send `"0"` instead.
3. For `compute_msmed_interest`, money is integer paise: ₹5,00,000.00 is `50000000`. Never send a decimal.
4. `bank_rates` is required. Munim does not assume a rate. Ask the user for the RBI Bank Rate in force, or the rows they rely on, as `[{"effective_from": "2026-10-07", "percent": "5.75"}]`. Say which rate you used.
5. With no written agreement, the due date is 15 days after acceptance. A written agreement can give up to 45 days; the tool applies the cap and says so in `cap_applied`.

## How to report results

- Say **passed** or **failed**, never "verified". A passed check means the computation succeeded on the values given; it does not prove the values are true.
- A `skipped` status means a value could not be read as an amount. Say which one; do not guess it.
- Quote the interest from `interest_formatted` and the basis from the result. Do not recompute it.
- Whether the supplier is protected by the Act (Udyam registration, its date, the buyer's status) is a legal question these tools do not answer. Say so and suggest the user check with counsel.

## Example

User: "Is this GSTIN valid?" followed by a 15-character value. Call `check_gstin` with `{"gstin": "<the value as given>"}`. Report `ok`, and for each rule id in `errors` say what failed, for example "failed GSTIN-CHECKSUM: the last character does not match the other fourteen." If `normalisation_applied` is true, say that spaces, hyphens or lower case were tidied first and give `normalised`.
