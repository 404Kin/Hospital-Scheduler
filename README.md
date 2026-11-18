# Hospital Scheduler - Starting Baseline (Day 1)

This is the foundation. It simulates ONE doctor and ONE clinic day with two simple strategies, so we have numbers to beat later.

- **S0 static**: fixed slots, no re-plan, no alerts (what clinics do today).
- **S1 shift-all**: delays push everybody later by the same amount, patients get alerts.

## Run it (Python 3.10+, no extra libraries needed)

    python -m sim.run_baselines              # table over 30 seeds
    python -m sim.run_baselines --day 7      # one day in detail (try other seeds)
    python -m sim.run_baselines --patients 12 --overrun 1.5
    python -m tests.test_baselines           # tests (or: pip install pytest, then: python -m pytest)

## Files

| File | What it does | Who will grow it |
|---|---|---|
| engine/models.py | Patient, Doctor classes. Time = minutes since midnight | A |
| engine/metrics.py | avg / p90 / max lounge wait, overtime, idle | B |
| sim/generator.py | Fake clinic days. Same seed = same day | A |
| sim/baselines.py | S0 and S1 | B |
| sim/run_baselines.py | Prints the comparison table | A + B |
| sim/export_dashboard.py | Writes dashboard/data.js | C |
| dashboard/index.html | Browser timeline viewer (plain HTML/JS, works offline) | C |
| tests/test_baselines.py | Basic tests | everyone |

## See it in the browser (no server needed)

    python -m sim.export_dashboard           # refreshes dashboard/data.js
    # then double-click dashboard/index.html

Pick a day, compare S0 and S1 as timelines. Yellow = waiting in lounge, blue = consultation, red = overtime.
Person C will later replace data.js with live data from the API.

## Important simple assumptions (write them in the report)

1. Real consultation time is lognormal with mean = 1.25 x planned time (assumption, not measured).
2. Patients arrive 15 min before the time they believe is theirs.
3. In S1, patient i is alerted when patient i-2 finishes, and never arrives before the alert.
4. The doctor serves patients in the same order in both baselines.
5. Seeds 1 to 30 are for testing. Keep seeds 101 to 130 for tuning later.

## Folders still empty on purpose

`engine/` will get rules.py, csp.py, optimizer.py later. `results/` is for CSV and plots. `docs/` is for interview notes and the report.
