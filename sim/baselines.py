"""
Baseline strategies (the 'before' picture we must beat):
  S0 = static fixed slots, no re-plan, no alerts.
  S1 = shift-all: delays push everybody later by the same amount, patients get alerts.
The doctor always serves patients in the SAME ORDER. No AI yet.
"""
import copy
from engine.models import Patient, Doctor

ARRIVE_EARLY = 15   # patients arrive 15 min before the time they believe is theirs


def assign_static_slots(patients: list[Patient], doctor: Doctor) -> None:
    """Back-to-back slots using the PLANNED durations."""
    t = doctor.shift_start
    for p in patients:
        p.original_start = t
        t += p.planned_min


def run_s0(patients: list[Patient], doctor: Doctor) -> list[Patient]:
    ps = copy.deepcopy(patients)
    assign_static_slots(ps, doctor)
    free = doctor.shift_start
    for p in ps:
        p.arrival = p.original_start - ARRIVE_EARLY
        p.start = max(free, p.arrival)
        p.end = p.start + p.real_min
        free = p.end
    return ps


def run_s1(patients: list[Patient], doctor: Doctor, alert_ahead: int = 2) -> list[Patient]:
    """
    Patient i is alerted when patient (i - alert_ahead) finishes. The alert says:
    'your time is now original_start + delay seen so far'. The patient then arrives
    ARRIVE_EARLY minutes before that time, but never before the alert itself.
    (Simple model on purpose. Write any change to it in the report.)
    """
    ps = copy.deepcopy(patients)
    assign_static_slots(ps, doctor)
    free = doctor.shift_start
    for i, p in enumerate(ps):
        if i < alert_ahead:
            p.arrival = p.original_start - ARRIVE_EARLY
        else:
            q = ps[i - alert_ahead]                      # already served
            delay = max(0, q.end - (q.original_start + q.planned_min))
            new_slot = p.original_start + delay
            p.arrival = max(new_slot - ARRIVE_EARLY, q.end)
        p.start = max(free, p.arrival)
        p.end = p.start + p.real_min
        free = p.end
    return ps
