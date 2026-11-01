# Real-paper evaluation

**Status: not run yet.** No real paper has been measured, so this file holds no result. Quote nothing from it until the table below is filled from a real run. Target from `docs/PRD.md`: 5 real papers tested locally.

## How to run it
1. Put the papers in `eval/real/`. Git ignores this folder; never commit from it.
2. Add `eval/real/manifest.json` in the same form as `eval/fixtures/manifest.json` (`papers` and `cases`), with each image path relative to `eval/real/`.
3. Add the correct values for each paper in `eval/real/truth/<paper id>.json`, in the same form as `eval/fixtures/truth/`.
4. Start a live reader, then run `MUNIM_PROVIDER=ollama uv run python eval/run_eval.py --real`. The command refuses the replay provider.
5. The report goes to `eval/real/report.json`, because it holds crops and values from the papers. Do not copy that file out of the folder, and do not use `--fixtures eval/real`, which would write to the committed `eval/reports/latest.json`.
6. Copy only the aggregate numbers below, then tick T6.9 in `docs/TASKS.md`.

## Results
Date, model and number of papers: not run.

| Measure | Result |
| --- | --- |
| Required fields that matched | not run |
| Amounts that matched | not run |
| Identifiers that matched | not run |
| Wrong and passed | not run |

## Failure descriptions
Not run. Describe each failure in general terms, such as "a faded stamp was read as absent". Include no names, GSTINs, amounts, invoice numbers or images.
