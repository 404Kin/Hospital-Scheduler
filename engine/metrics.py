"""Numbers we use to compare strategies. Lower is better for all of them."""
import math
from engine.models import Patient, Doctor


def lounge_waits(patients: list[Patient]) -> list[int]:
    """Minutes each patient sat in the waiting lounge (consult start - arrival)."""
    return [p.start - p.arrival for p in patients]


def percentile(values: list[float], q: float) -> float:
    """Simple percentile (q between 0 and 1) without extra libraries."""
    s = sorted(values)
    idx = max(0, math.ceil(q * len(s)) - 1)
    return s[idx]


def summarize(patients: list[Patient], doctor: Doctor) -> dict:
    waits = lounge_waits(patients)
    last_end = max(p.end for p in patients)
    # idle time of the doctor inside the shift (gaps between consultations)
    idle = max(0, patients[0].start - doctor.shift_start)
    for prev, cur in zip(patients, patients[1:]):
        idle += max(0, cur.start - prev.end)
    return {
        "avg_wait": sum(waits) / len(waits),
        "p90_wait": percentile(waits, 0.9),
        "max_wait": max(waits),
        "overtime": max(0, last_end - doctor.shift_end),
        "idle": idle,
    }
