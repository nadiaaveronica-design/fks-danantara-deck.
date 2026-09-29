"""Project specs registry. Each module exposes SPEC (dict). IDs map to module names below."""
import importlib

SPEC_MODULES = {
    "E1": "e1_telukLamong",
    "E2": "e2_cigadingExisting",
    "E3": "e3_belawan",
    "E4": "e4_win",
    "P01": "p01_cigWharf2",
    "P02": "p02_cigConveyor",
    "P03": "p03_kbsWarehouse",
    "P04": "p04_ttlSilo",
    "P05": "p05_dumai",
    "P06": "p06_ciwandan",
    "P08": "p08_dms",
    "P12": "p12_bumnOps",
    "P15": "p15_tbm",
    "P19": "p19_badas",
}

# order in which project sheets appear in the workbook
ORDER = ["E1", "E2", "E3", "E4", "P01", "P02", "P03", "P04", "P05", "P06", "P08", "P12", "P15", "P19"]


def load_spec(pid):
    mod = importlib.import_module(f"fsl.specs.{SPEC_MODULES[pid]}")
    return mod.SPEC


def all_spec_ids():
    out = []
    for pid in ORDER:
        try:
            load_spec(pid)
            out.append(pid)
        except ModuleNotFoundError:
            pass
    return out
