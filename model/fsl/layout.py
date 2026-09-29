"""Generic two-phase sheet builder for company-level sheets: a list of row descriptors is planned
(rows registered) and then written.

Descriptor forms (tuples):
  ("section", text)                                  section header
  ("sub", text)                                      sub-section header
  ("note", text)                                     italic note line
  ("blank",)                                         empty row
  ("row", key, label, unit, template, fmt, opts)     annual formula row; opts: f0, total, bold, link, note, src, years, fill, indent
  ("scalar", key, label, unit, value_or_template, fmt, opts)    scalar in column E; opts: cls (input class -> input styling), note, src, bold, link, check
  ("values", key, label, unit, {year: v}, fmt, opts)   annual hard-coded inputs; opts: cls, note, src
  ("text", key_or_None, label, value, opts)          label + text in E
  ("custom", callable)                               callable(model, sheetkey, row, ctx) executed in the write phase (no registration)
"""
from . import styles as S
from .engine import (Model, YEARS, YEAR_COL, FCOL, LCOL, L, DATA_ROW0, SCALAR_COL, LABEL_COL, UNIT_COL, TYPE_COL, SRC_COL, NOTE_COL, CLASS_FILL)


def plan_layout(model: Model, sheetkey, rows, start=DATA_ROW0):
    r = start
    planned = []
    for d in rows:
        typ = d[0]
        if typ == "blank":
            r += 1
            continue
        if typ in ("row", "values"):
            key, fmt = d[1], d[5]
            if key:
                model.register(sheetkey, key, r, kind="annual", fmt=fmt, label=d[2])
        elif typ == "scalar":
            key, fmt = d[1], d[5]
            if key:
                model.register(sheetkey, key, r, kind="scalar", fmt=fmt, label=d[2])
        elif typ == "text":
            if d[1]:
                model.register(sheetkey, d[1], r, kind="scalar", fmt="text", label=d[2])
        planned.append((r, d))
        r += 1
    return planned, r


def write_layout(model: Model, sheetkey, planned, ctx):
    ws = model.ws(sheetkey)
    for r, d in planned:
        typ = d[0]
        if typ == "section":
            model.section(sheetkey, r, d[1])
        elif typ == "sub":
            model.section(sheetkey, r, d[1], level=2)
        elif typ == "note":
            ws.cell(r, LABEL_COL).value = d[1]
            ws.cell(r, LABEL_COL).font = S.F_NOTE
        elif typ == "row":
            _, key, label, unit, tpl, fmt, opts = d
            opts = opts or {}
            model.write_label(ws, r, label, unit=unit, typ=opts.get("typ"), bold=opts.get("bold", False), src=opts.get("src"), note=opts.get("note"),
                              indent=opts.get("indent", 0))
            font = S.F_LINK if opts.get("link") else (S.F_BOLD if opts.get("bold") else S.F_BODY)
            model.write_annual_formula(sheetkey, r, tpl, ctx, fmt, f0=opts.get("f0"), years=opts.get("years"), font=font,
                                       total=opts.get("total", False), bold=opts.get("bold", False), fill=opts.get("fill"),
                                       border=S.B_TOTAL if opts.get("bold") else None)
            if opts.get("pre_shade"):
                model.shade_pre_valuation(sheetkey, r)
        elif typ == "values":
            _, key, label, unit, vals, fmt, opts = d
            opts = opts or {}
            cls = opts.get("cls", "v29")
            model.write_label(ws, r, label, unit=unit, typ=cls, src=opts.get("src"), note=opts.get("note"))
            model.write_annual_values(sheetkey, r, vals, fmt, fill=CLASS_FILL.get(cls, S.FILL_INPUT))
            if opts.get("total"):
                t = ws.cell(r, SCALAR_COL)
                t.value = f"=SUM({FCOL}{r}:{LCOL}{r})"
                t.number_format = S.NF[fmt]
                t.font = S.F_BOLD
                t.alignment = S.A_RIGHT
        elif typ == "scalar":
            _, key, label, unit, val, fmt, opts = d
            opts = opts or {}
            cls = opts.get("cls")
            model.write_label(ws, r, label, unit=unit, typ=cls if cls else opts.get("typ"), bold=opts.get("bold", False), src=opts.get("src"), note=opts.get("note"))
            is_formula = isinstance(val, str) and val.startswith("=")
            if cls:
                font = S.F_INPUT_B if cls == "CONTROL" else S.F_INPUT
                fill = CLASS_FILL.get(cls, S.FILL_INPUT)
            else:
                font = S.F_LINK if opts.get("link") else (S.F_BOLD if opts.get("bold") else S.F_BODY)
                fill = opts.get("fill")
            cell = model.write_scalar(sheetkey, r, val, fmt, ctx=ctx, font=font, fill=fill)
            if opts.get("check"):
                cell.alignment = S.A_CENTER
                cell.font = S.F_BOLD
        elif typ == "text":
            _, key, label, value, opts = d
            opts = opts or {}
            model.write_label(ws, r, label, bold=opts.get("bold", False), src=opts.get("src"), note=opts.get("note"))
            c = ws.cell(r, SCALAR_COL)
            c.value = model.resolve(value, SCALAR_COL, ctx) if (isinstance(value, str) and value.startswith("=")) else value
            c.font = S.F_LINK if opts.get("link") else S.F_BODY
            c.alignment = S.A_LEFT
        elif typ == "custom":
            d[1](model, sheetkey, r, ctx)
