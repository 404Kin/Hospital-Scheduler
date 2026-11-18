"""
Writes dashboard/data.js so the browser page can show the baselines.
Run:  python -m sim.export_dashboard
Then double-click dashboard/index.html (no server needed).
"""
import json
import statistics as st
from dataclasses import asdict
from engine.models import Doctor
from engine.metrics import summarize
from sim.generator import make_clinic_day
from sim.baselines import run_s0, run_s1

SEEDS = range(1, 31)
N_PATIENTS = 10


def build() -> dict:
    doctor = Doctor()
    days, rows = {}, {"S0": [], "S1": []}
    for seed in SEEDS:
        day = make_clinic_day(seed, N_PATIENTS)
        days[seed] = {}
        for name, fn in (("S0", run_s0), ("S1", run_s1)):
            ps = fn(day, doctor)
            m = summarize(ps, doctor)
            rows[name].append(m)
            days[seed][name] = {"patients": [asdict(p) for p in ps], "metrics": m}
    summary = {n: {k: st.mean(r[k] for r in rs) for k in rs[0]} for n, rs in rows.items()}
    return {"shift_start": doctor.shift_start, "shift_end": doctor.shift_end,
            "n_patients": N_PATIENTS, "days": days, "summary": summary}


if __name__ == "__main__":
    data = build()
    with open("dashboard/data.js", "w", encoding="utf-8") as f:
        f.write("window.DATA = " + json.dumps(data) + ";\n")
    print("wrote dashboard/data.js  ->  now open dashboard/index.html in your browser")
