"""Makes fake (synthetic) clinic days. Same seed -> same day, always."""
import math
import random
from engine.models import Patient

PLANNED_MIN = {"new": 20, "follow_up": 10, "post_op": 15, "fasting_test": 10}
TYPE_WEIGHTS = {"new": 0.35, "follow_up": 0.40, "post_op": 0.10, "fasting_test": 0.15}


def make_clinic_day(seed: int, n_patients: int = 10,
                    overrun_factor: float = 1.25, cv: float = 0.5) -> list[Patient]:
    """
    Real consultation time is lognormal: mean = overrun_factor * planned time,
    coefficient of variation = cv. This is an ASSUMPTION (say so in the report).
    """
    rng = random.Random(seed)
    types = list(TYPE_WEIGHTS)
    weights = list(TYPE_WEIGHTS.values())
    sigma2 = math.log(1 + cv ** 2)
    patients = []
    for i in range(1, n_patients + 1):
        vt = rng.choices(types, weights)[0]
        planned = PLANNED_MIN[vt]
        mean = planned * overrun_factor
        mu = math.log(mean) - sigma2 / 2
        real = max(3, round(rng.lognormvariate(mu, math.sqrt(sigma2))))
        patients.append(Patient(id=i, age=rng.randint(5, 85), visit_type=vt,
                                planned_min=planned, real_min=real))
    return patients
