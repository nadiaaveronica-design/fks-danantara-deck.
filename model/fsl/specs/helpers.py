"""Helpers to write compact specs for v29-style blocks."""
Y = list(range(2024, 2037))


def const(v, years=Y, first=None):
    """Annual dict with the same value each year; optional different value for 2024."""
    d = {y: v for y in years}
    if first is not None:
        d[2024] = first
    return d


def annual(key, label, unit, values, source, cls="v29", section="Operating assumptions", note=None, fmt=None):
    d = {"key": key, "label": label, "unit": unit, "kind": "annual", "values": values, "source": source, "cls": cls, "section": section}
    if note:
        d["note"] = note
    if fmt:
        d["fmt"] = fmt
    return d


def scalar(key, label, unit, value, source, cls="v29", section="Operating assumptions", note=None, fmt=None):
    d = {"key": key, "label": label, "unit": unit, "kind": "scalar", "value": value, "source": source, "cls": cls, "section": section}
    if note:
        d["note"] = note
    if fmt:
        d["fmt"] = fmt
    return d


def row(key, label, unit, f, section, f0=None, fmt=None, total=False, bold=False, link=False, note=None, src=None):
    d = {"key": key, "label": label, "unit": unit, "f": f, "section": section}
    if f0 is not None:
        d["f0"] = f0
    if fmt:
        d["fmt"] = fmt
    if total:
        d["total"] = True
    if bold:
        d["bold"] = True
    if link:
        d["link"] = True
    if note:
        d["note"] = note
    if src:
        d["src"] = src
    return d


def growth_index(key, label, growth_in, section, start=1):
    """v29-style index: 1 in the 2023 column, then prior x (1 + growth of the year) x forecast flag."""
    return row(key, label, "index", f"={{c:{key}@prev}}*(1+{{in:{growth_in}}})*{{flag}}", section, f0=f"={start}", fmt="idx")


def fixed_cost(key, label, base_in, growth_in, section, total=True):
    """Fixed cost line: index row + cost = base (2023 IDR bn) x index."""
    return [
        growth_index(f"{key}_idx", f"{label} — index", growth_in, section),
        row(key, f"{label} = base x index", "IDR bn", f"={{in:{base_in}}}*{{c:{key}_idx}}*{{flag}}", section, fmt="idr_bn", total=total),
    ]


def per_ton_cost(key, label, base_cost_in, base_vol_in, growth_in, volume_c, section, uplift=None, total=True):
    """Variable cost line: cost per ton (2023) = base cost / base volume x 1e9 [x uplift]; index; cost/t; cost = cost/t x volume / 1e9."""
    up = f"*{{in:{uplift}}}" if uplift else ""
    return [
        row(f"{key}_cost_t0", f"{label} — cost per ton in 2023 (base cost / base volume)", "IDR/t", f"={{in:{base_cost_in}}}/{{in:{base_vol_in}}}*10^9{up}", section, fmt="idr_t"),
        growth_index(f"{key}_idx", f"{label} — cost index", growth_in, section),
        row(f"{key}_cost_t", f"{label} — cost per ton", "IDR/t", f"={{c:{key}_cost_t0}}*{{c:{key}_idx}}", section, fmt="idr_t"),
        row(key, f"{label} = cost per ton x volume / 1e9", "IDR bn", f"={{c:{key}_cost_t}}*{{c:{volume_c}}}/10^9", section, fmt="idr_bn", total=total),
    ]


def sum_rows(key, label, keys, section, unit="IDR bn", fmt="idr_bn", bold=True, total=True):
    return row(key, label, unit, "=" + "+".join(f"{{c:{k}}}" for k in keys), section, fmt=fmt, bold=bold, total=total)
