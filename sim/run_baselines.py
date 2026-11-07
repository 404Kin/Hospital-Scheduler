"""
Run:  python -m sim.run_baselines            -> table over 30 seeds
      python -m sim.run_baselines --day 7    -> print one day in detail
"""
import argparse
import statistics as st
from engine.models import Doctor, hhmm
from engine.metrics import summarize
from sim.generator import make_clinic_day
from sim.baselines import run_s0, run_s1

TEST_SEEDS = range(1, 31)
STRATEGIES = {"S0 static": run_s0, "S1 shift-all": run_s1}


def table(n_patients: int, overrun: float) -> None:
    doctor = Doctor()
    print(f"\n{len(TEST_SEEDS)} days, {n_patients} patients/day, real = {overrun} x planned\n")
    print(f"{'strategy':<14}{'avg wait':>10}{'p90 wait':>10}{'overtime':>10}{'idle':>8}")
    for name, fn in STRATEGIES.items():
        rows = [summarize(fn(make_clinic_day(s, n_patients, overrun), doctor), doctor) for s in TEST_SEEDS]
        m = lambda k: st.mean(r[k] for r in rows)
        print(f"{name:<14}{m('avg_wait'):>10.1f}{m('p90_wait'):>10.1f}{m('overtime'):>10.1f}{m('idle'):>8.1f}")
    print("\n(all numbers in minutes, averaged over the seeds)")


def one_day(seed: int, n_patients: int, overrun: float) -> None:
    doctor = Doctor()
    day = make_clinic_day(seed, n_patients, overrun)
    for name, fn in STRATEGIES.items():
        ps = fn(day, doctor)
        print(f"\n=== {name}, seed {seed} ===")
        print(f"{'id':>3} {'type':<13}{'planned':>8}{'real':>6}{'slot':>7}{'arrive':>8}{'start':>7}{'end':>7}{'wait':>6}")
        for p in ps:
            print(f"{p.id:>3} {p.visit_type:<13}{p.planned_min:>8}{p.real_min:>6}{hhmm(p.original_start):>7}"
                  f"{hhmm(p.arrival):>8}{hhmm(p.start):>7}{hhmm(p.end):>7}{p.start - p.arrival:>6}")
        s = summarize(ps, doctor)
        print(f"avg wait {s['avg_wait']:.1f} | p90 {s['p90_wait']} | overtime {s['overtime']} | idle {s['idle']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", type=int, help="show one day for this seed")
    ap.add_argument("--patients", type=int, default=10)
    ap.add_argument("--overrun", type=float, default=1.25)
    a = ap.parse_args()
    one_day(a.day, a.patients, a.overrun) if a.day else table(a.patients, a.overrun)
