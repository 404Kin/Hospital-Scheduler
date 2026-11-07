"""Basic data classes. All times are MINUTES since midnight (09:00 = 540)."""
from dataclasses import dataclass


@dataclass
class Patient:
    id: int
    age: int
    visit_type: str          # "new", "follow_up", "post_op", "fasting_test"
    planned_min: int         # how long the slot was planned for
    real_min: int            # how long the consultation REALLY takes (hidden from planner)
    original_start: int = 0  # promised time (filled by static slot assignment)
    # filled in by the simulation:
    arrival: int = 0         # when the patient reaches the hospital
    start: int = 0           # when the consultation really starts
    end: int = 0             # when it really ends


@dataclass
class Doctor:
    id: int = 1
    name: str = "Dr. A"
    shift_start: int = 9 * 60    # 09:00
    shift_end: int = 12 * 60     # 12:00


def hhmm(minutes: int) -> str:
    """540 -> '09:00'"""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"
