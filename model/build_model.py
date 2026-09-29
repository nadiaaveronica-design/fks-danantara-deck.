#!/usr/bin/env python3
"""Build the revised FSL financial model workbook (live formulas) from the specs and the company layer.

Usage: python3 model/build_model.py [--out outputs/FSL_Financial_Model_Revised.xlsx] [--only E1,E2,...] [--no-recalc]
"""
import sys, os, argparse, json, subprocess, warnings, time
warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from fsl.engine import Model
from fsl.project import ProjectPlan, write_project
from fsl.globals_sheet import plan_globals, write_globals
from fsl.company import CompanyPlan
from fsl.specs import load_spec, all_spec_ids, ORDER

RECALC = "/root/.claude/skills/synced/ca1271e6-ddce-4c4e-8f01-c832fbb88730_653470ac-0907-46f7-93c1-15505bb7874c/xlsx/scripts/recalc.py"


def build(path, only=None, extra_layers=True):
    from fsl import valuation, summary, checks, docs  # optional layers (may be absent while developing)
    m = Model()
    pids = [p for p in (only or all_spec_ids())]
    specs = [load_spec(p) for p in pids]
    # sheet order: docs, global, summary, company, valuation, checks, then projects
    docs.plan_docs(m)
    plan_globals(m, specs)
    sm = summary.SummaryPlan(m, specs)  # creates 'Project Summary'
    company = CompanyPlan(m, specs)
    val = valuation.ValuationPlan(m, specs)
    chk = checks.ChecksPlan(m, specs)
    plans = [ProjectPlan(m, sp) for sp in specs]
    # writes
    write_globals(m, specs)
    for pl in plans:
        write_project(m, pl)
    company.write()
    val.write()
    summary.write(m, sm)
    chk.write()
    docs.write_docs(m, specs)
    m.wb.save(path)
    return m


def recalc(path, timeout=300):
    out = subprocess.run([sys.executable, RECALC, path, str(timeout)], capture_output=True, text=True)
    try:
        return json.loads(out.stdout.strip())
    except Exception:
        print(out.stdout, out.stderr)
        raise


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(ROOT), "outputs", "FSL_Financial_Model_Revised.xlsx"))
    ap.add_argument("--only", default=None)
    ap.add_argument("--no-recalc", action="store_true")
    a = ap.parse_args()
    only = a.only.split(",") if a.only else None
    t0 = time.time()
    m = build(a.out, only=only)
    print(f"built {a.out} with sheets: {len(m.wb.sheetnames)} in {time.time()-t0:.1f}s")
    if not a.no_recalc:
        j = recalc(a.out)
        print(json.dumps({k: j.get(k) for k in ("status", "total_formulas", "total_errors", "error")}, indent=1))
        if j.get("error_summary"):
            print(json.dumps(j["error_summary"], indent=1)[:4000])
