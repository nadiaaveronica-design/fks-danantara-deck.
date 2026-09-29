"""P19 Badas — feasibility-study working paper (DUMMY inputs), calculation and output.

Not in v29. Structure adapted from the Dumai / Ciwandan blocks (capacity x utilisation -> throughput; handling, storage and
ancillary tariffs -> revenue x FSL revenue share; variable, staff, fixed, maintenance, insurance and concession costs; capex by
year with commissioning; depreciation; working capital; project debt; economic ownership). Every operating assumption is a DUMMY
placeholder to be replaced with FS data; the total investment (10 USD m) is provisional from the board deck Dec-2024 (Stage 2).
Badas is excluded from the headline valuation by default (Global Inputs register: In valuation = 0) and its capex enters the
funding request through the separate 'Badas in funding' switch.
"""
from .helpers import Y

D = "DUMMY — REPLACE WITH FS DATA"
COMM = 2029
CAP, TAR, VAR, FIX, INV, FINC, OWN = ("Capacity, utilisation and throughput", "Tariffs and revenue streams", "Variable costs", "Fixed costs, staffing and maintenance",
                                     "Investment and commissioning (capex allocation below)", "Project financing (project-level debt)", "Economic ownership and sharing")


def dummy(key, label, unit, kind, val, section, definition, period, dest, question=None, note=None, cls="DUMMY", status=D, fmt=None):
    d = {"key": key, "label": label, "unit": unit, "kind": kind, "section": section, "cls": cls, "source": status,
         "definition": definition, "period": period, "status": status, "dest": dest}
    if kind == "annual":
        d["values"] = val
    else:
        d["value"] = val
    if question:
        d["question"] = question
    if note:
        d["note"] = note
    if fmt:
        d["fmt"] = fmt
    return d


def ramp(start, steps, tail):
    """Annual dict: 0 before commissioning, then the ramp values, then the steady-state tail."""
    out = {}
    for y in Y:
        if y < COMM:
            out[y] = 0
        else:
            i = y - COMM
            out[y] = steps[i] if i < len(steps) else tail
    return out


def grow(base, g, start=COMM):
    out = {}
    for y in Y:
        out[y] = 0 if y < start else round(base * (1 + g) ** (y - start), 4)
    return out


inputs = [
    dummy("capacity", "Design capacity (annual throughput at 100% utilisation)", "t", "scalar", 1000000, CAP,
          "Maximum tonnes per year the terminal can handle with the planned berth, unloading/loading equipment and storage.", "Parameter",
          "Calc: throughput = capacity x utilisation", "What is the design capacity of the Badas facility (t p.a.) and its binding constraint (berth, equipment, storage)?"),
    dummy("utilisation", "Utilisation of design capacity", "%", "annual", ramp(COMM, [0.55, 0.65, 0.75], 0.80), CAP,
          "Expected throughput / design capacity in each operating year (ramp-up to steady state).", "Annual FY2024-36",
          "Calc: throughput", "Which commodities and customers underpin the volume ramp-up, and how firm are the offtake / handling agreements?"),
    dummy("stored_share", "Share of throughput stored in the terminal", "%", "annual", ramp(COMM, [0.5], 0.5), CAP,
          "Share of the annual throughput that uses the storage facility (silo / warehouse) before onward delivery.", "Annual FY2024-36",
          "Calc: stored tonnes = throughput x share", "What share of the cargo will be stored on site rather than delivered directly?"),
    dummy("storage_months", "Average storage period", "months", "scalar", 1.5, CAP,
          "Average number of months a stored tonne stays in storage (drives storage revenue = stored tonnes x months x tariff).", "Parameter",
          "Calc: storage revenue", "What dwell time do customers expect and how is storage charged (per month, per day, minimum period)?"),
    dummy("ancillary_share", "Share of throughput using ancillary services (bagging / weighing)", "%", "annual", ramp(COMM, [0.3], 0.3), CAP,
          "Share of throughput that is bagged or weighed as an additional paid service.", "Annual FY2024-36", "Calc: ancillary revenue",
          "Which ancillary services (bagging, weighing, trucking, fumigation) will Badas offer and at what expected take-up?"),
    dummy("t_handling", "Handling tariff (100%, before revenue sharing)", "IDR/t", "annual", grow(45000, 0.03), TAR,
          "Stevedoring / cargodoring tariff per tonne handled, in nominal IDR, by year.", "Annual FY2024-36", "Calc: handling revenue = throughput x tariff",
          "What handling tariff is assumed and is it regulated (port authority) or negotiated? Any indexation?"),
    dummy("t_storage", "Storage tariff", "IDR/t/month", "annual", grow(12000, 0.03), TAR,
          "Storage tariff per tonne per month in nominal IDR.", "Annual FY2024-36", "Calc: storage revenue", "What storage tariff and indexation are assumed?"),
    dummy("t_ancillary", "Ancillary services tariff (bagging / weighing)", "IDR/t", "annual", grow(9000, 0.03), TAR,
          "Tariff per tonne for ancillary services.", "Annual FY2024-36", "Calc: ancillary revenue", "What do bagging / weighing services cost customers today at comparable ports?"),
    dummy("fsl_rev_share", "FSL share of gross revenue (revenue sharing with the port owner / concession grantor)", "%", "scalar", 1.0, OWN,
          "Share of gross terminal revenue that accrues to FSL under the port cooperation / concession agreement (the balance goes to the port owner).", "Parameter",
          "Calc: FSL revenue = gross revenue x share", "Is the Badas scheme a revenue share (like Ciwandan 52% / KBS warehouse 49%), a concession fee, or a fully owned operation?"),
    dummy("concession_pct", "Concession / port fee (% of gross revenue)", "%", "annual", ramp(COMM, [0.05], 0.05), VAR,
          "Fee paid to the port owner or concession grantor as a percentage of gross revenue (in addition to any revenue share).", "Annual FY2024-36",
          "Calc: cost of sales", "Are port dues / concession fees payable on top of the revenue share, and at what rate?"),
    dummy("var_cost_t", "Variable operating cost per tonne (fuel, power, casual labour, consumables)", "IDR/t", "annual", grow(8500, 0.03), VAR,
          "Direct cost per tonne handled, nominal IDR.", "Annual FY2024-36", "Calc: cost of sales", "What are the expected fuel / power / casual labour costs per tonne for the chosen equipment configuration?"),
    dummy("headcount", "Permanent staff headcount", "persons", "annual", ramp(COMM, [40], 40), FIX,
          "Number of permanent employees (operations, maintenance, administration) by year.", "Annual FY2024-36", "Calc: staff cost = headcount x cost per head",
          "What is the staffing plan (headcount by function) and when is recruitment needed relative to commissioning?"),
    dummy("cost_per_head", "Staff cost per head (salary, benefits, allowances)", "IDR m p.a.", "annual", grow(150, 0.05), FIX,
          "Average annual employment cost per permanent employee, IDR million.", "Annual FY2024-36", "Calc: staff cost",
          "What average employment cost per head applies at Badas (regional wage levels)?"),
    dummy("other_fixed", "Other fixed operating costs (G&A, security, utilities, IT, licences)", "IDR bn p.a.", "annual", grow(2.5, 0.03), FIX,
          "Fixed overheads not driven by volume, IDR bn per year.", "Annual FY2024-36", "Calc: operating expenses", "Which fixed costs are expected (security, utilities, office, insurance not covered below)?"),
    dummy("maint_pct", "Maintenance (% of total capex p.a.)", "%", "annual", ramp(COMM, [0.015], 0.015), FIX,
          "Annual maintenance cost as a percentage of the total investment (from commissioning).", "Annual FY2024-36", "Calc: cost of sales", "What maintenance regime and cost (% of capex or IDR per year) is planned for the equipment?"),
    dummy("ins_pct", "Insurance (% of total capex p.a.)", "%", "annual", ramp(COMM, [0.005], 0.005), FIX,
          "Annual insurance premium as a percentage of the total investment (from commissioning).", "Annual FY2024-36", "Calc: cost of sales", "What insurance cover and premium are assumed?"),
    dummy("preop_cost", "Pre-operating costs (recruitment, training, commissioning), expensed in the year before commissioning", "IDR bn", "scalar", 1.5, INV,
          "One-off costs incurred before commercial operations, expensed.", "Parameter", "Calc: operating expenses (year before commissioning)",
          "What pre-operating and commissioning costs are expected and when are they incurred?"),
    dummy("debt_share", "Project debt — share of capex funded by project-level debt", "%", "scalar", 0.5, FINC,
          "Share of each year's capex financed with project debt (the balance is equity from FSL / partners).", "Parameter", "Calc: debt drawdown = capex x share; Output: equity IRR",
          "Is project-level debt envisaged for Badas (lender, leverage), or will FSL fund it fully from the capital injection?"),
    dummy("debt_rate", "Project debt — interest rate", "%", "annual", {y: 0.105 for y in Y}, FINC,
          "All-in interest rate on the project debt (nominal IDR), by year.", "Annual FY2024-36", "Calc: interest", "Indicative lending terms (rate, tenor, grace, security)?", fmt="pct2"),
    dummy("debt_tenor", "Project debt — tenor of each drawdown incl. grace period", "years", "scalar", 7, FINC,
          "Years from drawdown to final repayment.", "Parameter", "Calc: repayment schedule", None),
    dummy("debt_grace", "Project debt — grace period before principal repayments start", "years", "scalar", 2, FINC,
          "Years after drawdown during which no principal is repaid.", "Parameter", "Calc: repayment schedule", None),
]

calc = [
    {"key": "throughput", "label": "Throughput = capacity x utilisation x operating flag", "unit": "t", "f": "={in:capacity}*{in:utilisation}*{c:opflag}", "fmt": "tons", "section": "Volume", "total": True},
    {"key": "stored_t", "label": "Stored tonnes = throughput x share stored", "unit": "t", "f": "={c:throughput}*{in:stored_share}", "fmt": "tons", "section": "Volume"},
    {"key": "anc_t", "label": "Tonnes using ancillary services", "unit": "t", "f": "={c:throughput}*{in:ancillary_share}", "fmt": "tons", "section": "Volume"},
    {"key": "rev_handling", "label": "Handling revenue = throughput x tariff / 1e9", "unit": "IDR bn", "f": "={c:throughput}*{in:t_handling}/10^9", "fmt": "idr_bn", "section": "Revenue (gross, 100%)", "total": True},
    {"key": "rev_storage", "label": "Storage revenue = stored tonnes x months x tariff / 1e9", "unit": "IDR bn", "f": "={c:stored_t}*{in:storage_months}*{in:t_storage}/10^9", "fmt": "idr_bn", "section": "Revenue (gross, 100%)", "total": True},
    {"key": "rev_anc", "label": "Ancillary revenue = tonnes x tariff / 1e9", "unit": "IDR bn", "f": "={c:anc_t}*{in:t_ancillary}/10^9", "fmt": "idr_bn", "section": "Revenue (gross, 100%)", "total": True},
    {"key": "rev_gross", "label": "Gross terminal revenue", "unit": "IDR bn", "f": "={c:rev_handling}+{c:rev_storage}+{c:rev_anc}", "fmt": "idr_bn", "section": "Revenue (gross, 100%)", "total": True, "bold": True},
    {"key": "revenue", "label": "FSL revenue = gross revenue x FSL revenue share", "unit": "IDR bn", "f": "={c:rev_gross}*{in:fsl_rev_share}", "fmt": "idr_bn", "section": "Revenue (gross, 100%)", "total": True, "bold": True},
    {"key": "c_var", "label": "Variable cost = throughput x cost per tonne / 1e9", "unit": "IDR bn", "f": "={c:throughput}*{in:var_cost_t}/10^9", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
    {"key": "c_conc", "label": "Concession / port fee = gross revenue x %", "unit": "IDR bn", "f": "={c:rev_gross}*{in:concession_pct}", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
    {"key": "c_maint", "label": "Maintenance = total capex (IDR bn) x % x capex-in-service flag", "unit": "IDR bn", "f": "=SUM({c:capex_idr@all})*{in:maint_pct}*{c:capflag}", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
    {"key": "c_ins", "label": "Insurance = total capex (IDR bn) x % x capex-in-service flag", "unit": "IDR bn", "f": "=SUM({c:capex_idr@all})*{in:ins_pct}*{c:capflag}", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
    {"key": "cogs", "label": "Total cost of sales (excl. depreciation)", "unit": "IDR bn", "f": "={c:c_var}+{c:c_conc}+{c:c_maint}+{c:c_ins}", "fmt": "idr_bn", "section": "Cost of sales", "total": True, "bold": True},
    {"key": "c_staff", "label": "Staff cost = headcount x cost per head / 1,000", "unit": "IDR bn", "f": "={in:headcount}*{in:cost_per_head}/1000*{flag}", "fmt": "idr_bn", "section": "Operating expenses", "total": True},
    {"key": "c_fixed", "label": "Other fixed costs", "unit": "IDR bn", "f": "={in:other_fixed}*{flag}", "fmt": "idr_bn", "section": "Operating expenses", "total": True},
    {"key": "c_preop", "label": "Pre-operating costs (year before commissioning)", "unit": "IDR bn", "f": "=IF({y}={in:commissioning}-1,{in:preop_cost},0)", "fmt": "idr_bn", "section": "Operating expenses", "total": True},
    {"key": "opex", "label": "Total operating expenses", "unit": "IDR bn", "f": "={c:c_staff}+{c:c_fixed}+{c:c_preop}", "fmt": "idr_bn", "section": "Operating expenses", "total": True, "bold": True},
    {"key": "d_draw", "label": "Project debt drawdown = capex (IDR bn) x debt share", "unit": "IDR bn", "f": "={c:capex_idr}*{in:debt_share}", "fmt": "idr_bn", "section": "Project debt (DUMMY financing plan)", "total": True},
    {"key": "d_open", "label": "Project debt — opening balance", "unit": "IDR bn", "f": "={c:d_close@prev}", "f0": "=0", "fmt": "idr_bn", "section": "Project debt (DUMMY financing plan)"},
    {"key": "d_repay", "label": "Project debt — repayment (each drawdown repaid straight-line after the grace period)", "unit": "IDR bn",
     "f": "=SUMPRODUCT({c:d_draw@all},--({g:year@all}+{in:debt_grace}<{y}),--({y}<={g:year@all}+{in:debt_tenor}))/({in:debt_tenor}-{in:debt_grace})", "f0": "=0", "fmt": "idr_bn", "section": "Project debt (DUMMY financing plan)", "total": True},
    {"key": "d_close", "label": "Project debt — closing balance", "unit": "IDR bn", "f": "={c:d_open}+{c:d_draw}-{c:d_repay}", "f0": "={c:d_draw}", "fmt": "idr_bn", "section": "Project debt (DUMMY financing plan)"},
    {"key": "d_int", "label": "Project debt — interest = rate x opening balance", "unit": "IDR bn", "f": "={in:debt_rate}*{c:d_open}", "f0": "=0", "fmt": "idr_bn", "section": "Project debt (DUMMY financing plan)", "total": True},
]

SPEC = {
    "id": "P19",
    "code": "Badas",
    "titles": ("P19 Badas FS Working Paper", "P19 Badas Calculation", "P19 Badas Output"),
    "working_paper": True,
    "name": "Badas bulk terminal (FS pending — DUMMY data)",
    "short": "Badas",
    "entity": "New project company (FSL share DUMMY 100%) — Badas port, Sumbawa (NTB)",
    "entity_short": "Badas (new)",
    "category": "Pipeline — FS pending (DUMMY inputs, excluded from headline valuation)",
    "description": "Bulk cargo terminal at Badas: capacity x utilisation -> throughput; handling, storage and ancillary tariffs; variable, staff, fixed, maintenance, insurance and concession costs; 10 USD m provisional capex; project debt option. ALL operating inputs are DUMMY placeholders until the feasibility study is received.",
    "v29": {"calc": "not in v29 (structure adapted from Dumai rows 168-218 and Ciwandan rows 508-546)", "input": "board deck Dec-2024 Stage 2: Badas 10.0 USD m", "standalone": "n/a", "flag": "Global Inputs register (delivered: In valuation = 0; Badas in funding = 1)"},
    "defaults": {"in_valuation": 0, "case": 1, "econ_interest": 1.0},
    "existing": False,
    "depends": [],
    "commissioning": {"year": COMM, "source": D, "cls": "DUMMY", "note": "First year of commercial operations (construction 2027-28). Q: expected construction period and COD?"},
    "capex": {
        "total_usd": 10.0, "source": "Board deck Dec-2024 use of proceeds, Stage 2 (Badas 10.0 USD m) — PROVISIONAL", "cls": "UPDATED",
        "pct": {2027: 0.6, 2028: 0.4}, "pct_source": "DUMMY — REPLACE WITH FS DATA (construction phasing)", "pct_cls": "DUMMY",
        "building_share": 0.6, "building_source": D, "life_b": 20, "life_e": 10, "lives_source": D,
        "hist_confirmed": 0,
        "note": "Q: total investment incl. contingency, split civil works / equipment, and construction schedule?",
    },
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": "opex", "da_other": None},
    "project_debt": {"draw": "d_draw", "repay": "d_repay", "interest": "d_int", "balance": "d_close"},
    "recon_note": "Not in v29 — illustrative results on DUMMY inputs.",
}
