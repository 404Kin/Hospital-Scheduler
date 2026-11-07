"""Run with:  python -m pytest   (or without pytest:  python -m tests.test_baselines)"""
from engine.models import Patient, Doctor
from engine.metrics import summarize, percentile
from sim.generator import make_clinic_day
from sim.baselines import run_s0, run_s1


def test_generator_is_reproducible():
    a = make_clinic_day(5); b = make_clinic_day(5)
    assert [(p.visit_type, p.real_min, p.age) for p in a] == [(p.visit_type, p.real_min, p.age) for p in b]


def test_no_overlap_and_order_kept():
    doc = Doctor()
    for seed in range(1, 31):
        for fn in (run_s0, run_s1):
            ps = fn(make_clinic_day(seed), doc)
            for prev, cur in zip(ps, ps[1:]):
                assert cur.start >= prev.end
            assert all(p.start >= p.arrival for p in ps)


def test_s0_known_case():
    # patient 1: planned 10, really 25.  patient 2: planned 10, really 10.
    day = [Patient(1, 30, "new", 10, 25), Patient(2, 40, "new", 10, 10)]
    ps = run_s0(day, Doctor())
    assert (ps[0].arrival, ps[0].start, ps[0].end) == (525, 540, 565)
    assert (ps[1].arrival, ps[1].start, ps[1].end) == (535, 565, 575)
    s = summarize(ps, Doctor())
    assert s["avg_wait"] == (15 + 30) / 2 and s["overtime"] == 0


def test_overtime_and_percentile():
    day = [Patient(i, 30, "new", 60, 60) for i in range(1, 5)]   # 4h of work in a 3h shift
    s = summarize(run_s0(day, Doctor()), Doctor())
    assert s["overtime"] == 60
    assert percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.9) == 9


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        t(); print("PASS", t.__name__)
