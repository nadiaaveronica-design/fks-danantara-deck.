# Test results — FSL Financial Model Revised

Run: 2026-09-29 01:37 (LibreOffice Calc headless recalculation; Microsoft Excel was not used)

Model: `outputs/FSL_Financial_Model_Revised.xlsx`

| Test | Condition | Evidence | Result |
|---|---|---|---|
| T0 delivered file | LibreOffice recalculation succeeds with zero formula errors | {"status": "success", "total_formulas": 34969, "total_errors": 0} | **PASS** |
| T0 delivered file | Checks sheet overall status = ALL PASS | ALL PASS | **PASS** |
| T0 delivered file | No Err:/# error strings (incl. circular-reference Err:522) | 0 found [] | **PASS** |
| T0 delivered file | No external workbook links | [] | **PASS** |
| T1 valuation date | Global Inputs valuation date = 31-Dec-2026 | 2026-12-31 00:00:00 | **PASS** |
| T1 valuation date | Discount factors 2024-2026 = 0 and DF(2027) = 1/(1+WACC) (one full year) | 2024: 0.0000 / 2025: 0.0000 / 2026: 0.0000 / 2027: 0.8939 / 2028: 0.7991 / WACC 11.8665% | **PASS** |
| T1 valuation date | FCFF entering the DCF is nil for 2024-2026 and starts in 2027 | 2024: 0.00 / 2025: 0.00 / 2026: 0.00 / 2027: 205.31 | **PASS** |
| T2 injection timing (delivered 30-Jun-2027) | Loan carried to 2026, repaid in 2027; interest 2025-26 full-year, 2027 half-year | balance 2024: 195.18 / 2025: 195.18 / 2026: 195.18 / 2027: 0.00 / 2028: 0.00 / 2029: 0.00 // interest 2024: 5.47 / 2025: 15.27 / 2026: 15.27 / 2027: 7.57 / 2028: 0.00 / 2029: 0.00 | **PASS** |
| T2 injection moved to 30-Jun-2026 | Repayment moves to 2026; 2026 interest = half-year on the repaid amount; 2027 interest nil; loan at valuation date = 0 | balance 2024: 195.18 / 2025: 195.18 / 2026: 0.00 / 2027: 0.00 / 2028: 0.00 // interest 2024: 5.47 / 2025: 15.27 / 2026: 7.57 / 2027: 0.00 / 2028: 0.00 // LT at val date 0.00 | **PASS** |
| T2 injection moved to 30-Jun-2026 | Injection received in 2026 and cash-flow shows equity receipt and repayment separately | inj 2026 195.18; repay 2026 195.18; equity bridge basis: POST-money: injection received on/before the valuation date is inside cash | **PASS** |
| T2 injection moved to 31-Mar-2028 | Loan outstanding through 2027 (and at the valuation date), interest full-year in 2027, repaid 2028 with quarter-year interest | balance 2024: 195.18 / 2025: 195.18 / 2026: 195.18 / 2027: 195.18 / 2028: 0.00 / 2029: 0.00 // interest 2024: 5.47 / 2025: 15.27 / 2026: 15.27 / 2027: 15.27 / 2028: 3.80 / 2029: 0.00 | **PASS** |
| T3 zero injection (mode 2, 0 USD m) | Loan is NOT extinguished: balance 195.18 through 2036, interest keeps accruing, shortfall flagged | 2027: 195.18 / 2036: 195.18 / interest 2030 15.27 / flag: SHORTFALL — planned repayment not fully funded by the injection; balance retained | **PASS** |
| T3 insufficient injection (mode 2, 6 USD m) | Only 6 USD m (97.6) repaid; unpaid balance 97.6 retained and flagged | repay 2027 97.59; balance 2027 97.59; shortfall 97.59; flag SHORTFALL — planned repayment not fully funded by the injection; balance retained | **PASS** |
| T4 capex % (P05 Dumai 100% FY2026 -> 50% FY2027 / 50% FY2028) | Annual capex moves with the percentages and the allocation check stays PASS | before 2025: 0.00 / 2026: 6.48 / 2027: 0.33 / 2028: 0.00 / 2029: 0.00 // after 2025: 0.00 / 2026: 0.00 / 2027: 3.40 / 2028: 3.40 / 2029: 0.00 // check PASS | **PASS** |
| T4 capex % (P05) | Depreciation, post-valuation capex and the funding shortfall update (requirement is floored at the planned loan repayment, so it changes only when the shortfall exceeds it) | dep before 2026: 8.44 / 2027: 8.86 / 2028: 8.86 / 2029: 8.86 / 2030: 8.86 // after 2026: 0.00 / 2027: 4.43 / 2028: 8.86 / 2029: 8.86 / 2030: 8.86 // post-val capex 0.33 -> 6.81 // 2027 pre-equity shortfall 42.8 -> 9.4 // requirement 195.2 -> 195.2 | **PASS** |
| T4 capex % (P05) | Company capex and valuation capex move accordingly (With-BUMN case) | company capex 2027: -160.00 -> -210.10; EV 4390.6 -> 4301.4 | **PASS** |
| T5 Badas inputs replaced (capacity 1.5 m t, handling tariff 60,000) | Badas Calculation and Output update; still outside the valuation (EV unchanged) | revenue before 2029: 31.18 / 2030: 37.96 / 2031: 45.11 // after 2029: 59.15 / 2030: 70.25 / 2031: 81.46 // EV 4390.6 -> 4390.6 | **PASS** |
| T5 Badas switched into the valuation | EV changes, Badas capex leaves the capex-only request (no double count) and enters the company statements | EV 4390.6 -> 4382.7; capex-only Badas 162.7 -> 0.0; company capex 2027 -160.0 -> -257.6 | **PASS** |
| T6 BUMN operatorship switched off | With-BUMN revenue falls to the Without-BUMN level; Without-BUMN unchanged | w/o 807.9 -> 807.9; w/ 957.0 -> 807.9 | **PASS** |
| T6 DMS moved to case 2 (With-BUMN only) | Without-BUMN revenue falls by the DMS revenue; With-BUMN unchanged | w/o 807.9 -> 804.3 (DMS 3.57); w/ 957.0 -> 957.0 | **PASS** |
| T6 funding case switched to With BUMN | Funding requirement changes to the With-BUMN figure | requirement 195.2 (w/o) -> 195.2; w/ figure 195.2 | **PASS** |
| T7 funding-only placeholder F01 = 20 USD m in FY2027 | Total request rises by 20 x FX / 1,000; valuation and statements unchanged | request 357.8 -> 683.1 (+325.3); EV 4390.6 -> 4390.6; company capex 2027 -160.0 -> -160.0; check PASS | **PASS** |
| T8 project -> company reconciliation | Sum of project revenue x flags = company revenue (both cases) and FCFF = valuation FCFF | max diffs: 0.000000 / 0.000000 / 0.000000 | **PASS** |
| T8 balance sheet / cash | Balance sheets balance (within the v29 opening residual 0.006) and cash reconciles | max /BS check/ 0.0062; cash check 0.000000 | **PASS** |
| T8 funding sources = uses | Injection covers the planned repayment; residual gap nil (mode 1) | injection 195.2 >= planned repayment 195.2; residual gap 0.0000 | **PASS** |
| T9 v29 reproduction (dep method 1, injection 31-Dec-2025 = 12 USD m) | Revenue, cost of sales, opex, EBITDA and financing cost match v29 Output_FSL (With BUMN) each year; D&A/EBIT differ only by the documented KBS-warehouse depreciation | revenue: max/diff/ 0.000; cogs: max/diff/ 0.000; opex: max/diff/ 0.000; ebitda: max/diff/ 0.000; da: max/diff/ 4.900; ebit: max/diff/ 4.900; fin_cost: max/diff/ 0.000 | **PASS** |
| T9 v29 reproduction | D&A difference by year (expected = KBS warehouse 6.02 USD m depreciation that v29 never charged, from FY2026) | 2024: -0.000 / 2025: -0.000 / 2026: -0.000 / 2027: -4.900 / 2028: -4.900 / 2029: -4.900 / 2030: -4.900 / 2031: -4.900 / 2032: -4.900 / 2033: -4.900 / 2034: -4.900 / 2035: -4.900 / 2036: -4.900 | **PASS** |

Overall: **ALL PASS** (27 pass / 0 fail)

Variants used for testing are in `model/tests/out/` (the delivered workbook is untouched; delivery settings restored by construction).