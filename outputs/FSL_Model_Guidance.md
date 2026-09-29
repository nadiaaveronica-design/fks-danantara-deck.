# FSL Financial Model (revised from v29) — Guidance document

_Workbook: `outputs/FSL_Financial_Model_Revised.xlsx` · generated 29 Sep 2026 · all figures IDR bn unless stated · recalculated with LibreOffice Calc (headless); Microsoft Excel was not used_

## 1. What this model is

A rebuild of the v29 FKS Solusi Logistik (FSL) model with live Excel formulas, organised project by project. v29 remains the source of business assumptions and calculation logic (every input cites its v29 cell); the requested changes are built in: valuation date 31 December 2026 with a DCF from FY2027, the 12 USD m long-term loan carried until the capital injection and repaid from it, capex controlled by annual percentages, Badas as a feasibility-study working paper with dummy data, a Funding Requirement sheet with five funding-only placeholders, and separate With / Without BUMN cases. Sapphire is excluded (as in v29 Output_FSL).

## 2. Headline results (delivered settings)

| Item | Without BUMN | With BUMN |
|---|---|---|
| Enterprise value at 31-Dec-2026 | 3,859 (237 USD m) | 4,391 (270 USD m) |
| Equity value attributable to FSL shareholders | 3,250 (200 USD m) | 3,782 (233 USD m) |
| Terminal value share of EV | 40% | 41% |
| Value of the BUMN operatorship schemes (EV difference) | | 532 |

| Funding (funding case = Without BUMN, conservative) | IDR bn | USD m |
|---|---|---|
| Equity requirement — valuation-scope operations incl. LT loan repayment (received in 2027) | 195.2 | 12.0 |
| Capex-only request — Badas (provisional 10 USD m, dummy) + placeholders F01-F05 (blank) | 162.7 | 10.0 |
| **Total equity funding request** | **357.8** | **22.0** |

The LT loan (195.2 IDR bn) is still outstanding at the valuation date because the injection is assumed on 30 June 2027; the equity bridge therefore deducts it and the equity value is pre-money. Cash at 31-Dec-2026 (Without BUMN) is 3.0 IDR bn: v29's FY2026 capex (419.8) is funded from operating cash with dividends squeezed to the minimum-cash cap. Checks sheet: **ALL PASS**.

Equity value (what the business is worth) and the equity funding request (cash the shareholders must contribute) are different quantities and are shown on different sheets.

## 3. Where to find things

| Need | Sheet |
|---|---|
| Start / navigation | `Navigation` (links to every sheet), `Model Flow` (architecture, changes vs v29, controls, tests) |
| Shared assumptions and switches | `Global Inputs` — timeline & valuation date, FX, tax & working-capital days, switches (depreciation method, interest shield, dividends, funding case, Badas in funding, other balances in bridge), valuation parameters (provisional), opening balance sheet, financing & injection, **project register** (in valuation / case / FSL interest) |
| Each project | `<ID> <Code> Input` (assumptions, capex %), `… Calc` (drivers), `… Output` (P&L, FCFF, net operating assets, funding need, returns). Cigading Ext Conveyor = `P02 CigConveyor Input / Calc / Output` |
| Project comparison | `Project Summary` — comparison table, bridge to company, one section per project |
| Company statements | `FSL Financials — Without BUMN`, `FSL Financials — With BUMN` (IS, BS, CF, funding roll-forward & dividends, consolidation workings) |
| How much equity do we need? | `Funding Requirement` (headline answers, roll-forward of the selected case, needs by project, capex-only projects incl. five placeholders, bridge, use of proceeds vs board deck) |
| Loan and injection mechanics | `Financing` |
| Valuations | `Valuation — Without BUMN`, `Valuation — With BUMN` (same layout) |
| Integrity | `Checks` (PASS/FAIL formulas, warnings, list of v29 source issues), `Reconciliation v29` |
| Badas FS working paper | `P19 Badas FS Working Paper` (inputs with definition, unit, period, status, destination, questions), `P19 Badas Calculation`, `P19 Badas Output` |

## 4. Architecture and conventions

* **Column layout on every time-series sheet:** F = 2023 (opening / pre-2024), G..S = 2024..2036; row 5 = year, row 8 = forecast flag. Same layout everywhere, so cross-sheet links keep the column.
* **Colours:** blue on yellow = input (v29 or derived); bold blue on gold = control switch; light blue = user-requested change; light green = updated information from the user; orange = provisional; salmon = DUMMY (Badas); black = formula; green = link from another sheet.
* **Classification (column D of input rows):** v29 / DERIVED / UPDATED / CHANGE / DUMMY / PROV / CONTROL. Column T cites the v29 cell (effective value, including values typed inside v29 formulas); column U carries notes on v29 quirks.
* **Units:** IDR bn for money, USD m for capex totals, t for volumes, IDR/t for tariffs. Costs are positive in Calc sheets and negative in the statements.
* **Project Output = unlevered:** tax on project EBIT (v29 line method, no loss relief between lines); FCFF = NOPAT + D&A - capex - increase in working capital; no project cash or debt (funded by FSL corporate). Existing fixed assets, other balances, loans and paid-in capital are company-level (v29 only has them at entity level).

## 5. The two BUMN cases

v29 `Output_FSL` includes the 'Operatorship with BUMN' block (`Output_FSL!F35 = 1`), i.e. it is a With-BUMN view; 'standalone' in v29 refers to per-project blocks, not to a no-BUMN case. The register on Global Inputs gives each project a case: 1 = both cases, 2 = With-BUMN only (P12 BUMN operatorship). Both company cases, both valuations and the two funding requirements are computed simultaneously; the switch `funding_case` chooses which case drives the headline funding answer (delivered: Without BUMN). DMS trucking fees (50/50 with the port operator) are kept in both cases as in the earlier model; set their case to 2 to treat them as BUMN-dependent.

## 6. Valuation timing

Valuation date 31-Dec-2026 (Global Inputs). The DCF window flag is 1 for years after the valuation date; FY2027 is discounted one full year (year-end convention). FCFF is unlevered and consistent with WACC (project line taxes on EBIT; the corporate interest shield is excluded). Terminal value uses a normalised FY2036 cash flow (capex = factor x depreciation because v29 forecasts no capex after FY2028; working capital grows with g). Equity bridge: + cash at the valuation date, - loans at the valuation date (the LT loan is deducted when the injection falls after 31-Dec-2026), +/- other Dec-23 balances (switch, default excluded), - non-controlling interests (35% of the Teluk Lamong lines). Only spend after the valuation date enters the DCF; pre-valuation spend is labelled and excluded.

## 7. Injection-linked loan repayment

Global Inputs: injection date (provisional 30-Jun-2027), mode (1 = sized to the funding requirement; 2 = fixed USD m), planned repayment share (100%). Financing sheet: the LT loan is carried until the injection; repayment = planned share of the balance in the injection year (mode 2: limited to the proceeds; any shortfall is flagged and the balance stays outstanding and keeps accruing interest). Interest = rate x (balance carried for the full year + repaid amount x fraction of the year to the injection date); FY2024 keeps the v29 figure; the rate (7.83%) is implied from v29's FY2025 interest and is provisional. The equity receipt and the loan repayment are separate lines in the cash-flow statement. No circular references: the requirement is computed on a pre-equity cash path and the injection always covers at least the planned repayment.

## 8. Capex percentages

Each project Input sheet: total capex (USD m), annual % of TOTAL capex (2023 column = pre-2024 sunk spend), USD and IDR schedules with the visible exchange rate, spend up to the valuation date vs after it, unallocated, allocation check, 'historical spend confirmed' flag (0 = v29 projected timing, not actuals), building share, useful lives and the capex commissioning year. Depreciation method switch on Global Inputs: 2 (default) = each year's spend over its life from MAX(spend year, commissioning) with an end; 1 = v29 (total x share / life from commissioning, no end). Commissioning (first revenue year) is a separate input from the capex timing.

## 9. Badas working paper

`P19 Badas FS Working Paper` lists every requested input with its definition, unit, period, status ('DUMMY — REPLACE WITH FS DATA' or 'PROVISIONAL'), calculation destination and a question for the operations team. Rows are highlighted in salmon while dummy. Structure follows Dumai / Ciwandan: capacity x utilisation -> throughput; handling, storage and ancillary tariffs; FSL revenue share; variable, concession, maintenance, insurance, staff and fixed costs; 10 USD m provisional capex (board deck Stage 2) phased 60/40 over 2027-28; commissioning 2029; project debt option (50%, 10.5%, 7 years incl. 2 grace) giving an equity IRR. Badas is excluded from the headline valuation (register switch = 0) while its capex is in the funding request (switch 'Badas in funding' = 1). Dumai's and Ciwandan's commercial terms are NOT assumed for Badas.

## 10. Funding-only placeholders

`Funding Requirement` section D: F01-F05 accept a name, total capex (USD m), annual % and an include switch. They add to the equity request only, never to the statements or the valuation, and show 'FS not available' for operating results and returns. Blank placeholders are inactive and error-free.

## 11. Project register (delivered settings)

| ID | Project | Category | In valuation | Case | Capex USD m | NPV @ 31-Dec-26 (IDR bn) | Full-life IRR |
|---|---|---|---|---|---|---|---|
| E1 | Teluk Lamong (NPLOG) cargodoring & delivery | Existing business | 1 | 1 | 0.00 | 1,190 | n/a — existing business (no entry cost / original investment data) |
| E2 | Cigading Existing Terminal (SGT 2) | Existing business | 1 | 1 | 0.00 | 461 | n/a — existing business (no entry cost / original investment data) |
| E3 | Belawan terminal (SGT3) incl. Belawan expansion | Existing business | 1 | 1 | 14.02 | 238 | n/a — existing business (no entry cost / original investment data) |
| E4 | WIN stevedoring (Cilegon, Makassar, Surabaya, Medan) | Existing business | 1 | 1 | 0.00 | 214 | n/a — existing business (no entry cost / original investment data) |
| P01 | Cigading Wharf 2 | Committed project | 1 | 1 | 12.80 | 960 | 27.6% |
| P02 | Cigading Extended Conveyor | Committed project | 1 | 1 | 8.00 | 281 | 16.2% |
| P03 | KBS Warehouse Revitalisation (Cigading) | Planned project | 1 | 1 | 6.02 | 190 | 13.3% |
| P04 | Teluk Lamong Silo | Planned project | 1 | 1 | 3.76 | 105 | 12.3% |
| P05 | Dumai bagging & weighbridge | Planned project | 1 | 1 | 6.81 | 198 | 19.3% |
| P06 | Ciwandan Expansion | Planned project | 1 | 1 | 5.02 | 476 | 38.6% |
| P08 | DMS trucking fee (Teluk Lamong, Cigading, Ciwandan, Belawan) | Planned project | 1 | 1 | 0.00 | 24 | n/a |
| P12 | BUMN operatorship schemes (Pelindo Teluk Lamong, KBS Cigading, Pelindo Belawan) | BUMN synergy | 1 | 2 | 0.00 | 532 | n/a |
| P15 | TBM — Tanjung Batu / Pelindo land lease, warehousing and cargo handling | Pipeline (excluded by default) | 0 | 1 | 40.02 | 1,326 | 9.5% |
| P19 | Badas bulk terminal (FS pending — DUMMY data) | Pipeline — FS pending (DUMMY inputs, excluded from headline valuation) | 0 | 1 | 10.00 | 35 | 0.4% |

NPV = PV at the valuation date of FY2027+ FCFF incl. a plain Gordon terminal value at the company WACC; full-life IRR uses FCFF 2023-2036 incl. pre-2024 spend and no terminal value (existing businesses: n/a).

## 12. Reconciliation to v29 and source issues

`Reconciliation v29` compares the With-BUMN case with v29 `Output_FSL` line by line (static v29 values, explanations per line). With depreciation method 1 and the injection set to 31-Dec-2025 (mode 2, 12 USD m) revenue, cost of sales, opex, EBITDA and financing cost match v29 in every year; D&A differs only by the KBS-warehouse depreciation that v29 never charged (broken reference). v29 source issues are documented, not corrected silently (Checks sheet, S1-S11): typed opening receivables/payables and a 0.006 imbalance, existing-asset depreciation without a book-value cap, KBS warehouse capex never depreciated, DMS equipment depreciated without capex, inventory dropping to nil from FY2034, Belawan expansion volume ending FY2034, WIN Makassar sugar tariff nil FY2034-36, Teluk Lamong G&A staff growth from the wrong row, Cigading volume typed over the input, provisional loan terms, minority interest treatment.

## 13. Tests performed

`model/tests/run_tests.py` builds variants of the delivered file, recalculates each with LibreOffice and checks: zero formula errors / no external links; valuation date and DCF window; injection date moved to 2026 and 2028 (repayment, interest, loan at the valuation date, pre/post-money); zero and insufficient proceeds (loan retained, shortfall flagged); capex % moved between years (capex, depreciation, post-valuation capex, funding shortfall, company capex, EV); Badas inputs replaced and Badas switched into the valuation (no double count); BUMN operatorship off, DMS moved to case 2, funding case switched; placeholder F01 populated (request up, valuation unchanged); project -> company reconciliation, balance sheets, cash, sources = uses; v29 reproduction mode. Evidence: `model/tests/test_results.md`.

## 14. Assumptions still requiring confirmation

* Capital injection date and amount (provisional 30-Jun-2027; sized to the requirement in mode 1).
* LT loan terms: 12 USD m principal, 7.83% implied rate, currency and maturity; FY2024 repayment of the other loans (29.3) as in v29.
* FY2024-FY2026 figures are v29 projections; actual spend to date on Wharf 2, conveyor, Dumai, KBS warehouse, TTL silo, Ciwandan and Belawan should replace the 'unconfirmed' pre-valuation percentages.
* Valuation parameters (WACC build-up 11.87%, terminal growth 3%, normalised capex factor) are provisional.
* Badas: all operating inputs dummy; 10 USD m capex from the board deck.
* Board-deck use of proceeds vs v29 (Ciwandan 17.0 vs 11.0; Dumai 20.0 vs 6.8; Port LT warehouse 60; Vietnam 15; TBM 108) — the model keeps v29 totals; use the placeholders for items without an FS.
* Minimum operating cash (3.0, v29), dividend policy (30% payout, v29 rules) and the treatment of DMS fees as non-BUMN drive the funding answer; all are switches / inputs.

## 15. Reproducing the build

```
python3 model/build_model.py            # builds outputs/FSL_Financial_Model_Revised.xlsx and recalculates it (LibreOffice)
python3 model/verify/verify_block.py P02 # per-block reconciliation to v29
python3 model/tests/run_tests.py         # scenario tests -> model/tests/test_results.md
python3 model/make_guidance.py           # this document
```
Specs live in `model/fsl/specs/` (one Python file per project, docstring = effective v29 logic); the framework in `model/fsl/`. Original files in `model/source/` are read-only and unchanged.
