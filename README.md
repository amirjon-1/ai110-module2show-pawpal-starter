# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

Beyond the core greedy planner, four additional features improve how tasks are managed:

**Sorting by duration** — `Scheduler.sort_tasks_by_duration()` returns tasks ordered shortest to longest using `sorted()` with a lambda. Useful for fitting the most tasks into a tight time budget.

**Filtering by completion status** — `Scheduler.filter_tasks(completed=True/False)` returns only tasks matching the given status. Makes it easy to show a pet's pending tasks or review what has already been done today.

**Recurring tasks** — `Task` has a `recurrence` field (`"none"`, `"daily"`, `"weekly"`) and a `due_date` field. When `mark_complete()` is called on a recurring task, it returns a new `Task` instance with `due_date` advanced by 1 or 7 days via `timedelta`, leaving the original marked complete.

**Conflict detection** — `Scheduler.detect_conflicts()` groups tasks by `due_date` and checks every pair within the same date. If any two tasks combined would exceed the available time budget, a warning string is returned — no exceptions raised.

## Testing PawPal+

**Confidence: ★★★★☆ (4/5)**

Run the full test suite:

```bash
pytest tests/test_pawpal.py -v
```

| Test | Description |
|---|---|
| `test_mark_complete_sets_is_complete` | Calling `mark_complete()` flips `is_complete` from `False` to `True` |
| `test_add_task_increases_pet_task_count` | `add_task()` appends to the pet's task list and increments its length |
| `test_sort_tasks_by_duration_shortest_first` | `sort_tasks_by_duration()` returns tasks in ascending order of duration |
| `test_mark_complete_daily_task_creates_new_task_due_tomorrow` | Completing a daily recurring task returns a fresh task with `due_date` advanced by one day |
| `test_detect_conflicts_flags_tasks_exceeding_budget` | Two same-date tasks whose combined duration exceeds the budget produce a conflict warning |
| `test_pet_with_no_tasks_returns_empty_plan` | `generate_plan()` on a pet with no tasks returns an empty list |
| `test_filter_tasks_returns_only_incomplete` | `filter_tasks(completed=False)` excludes already-completed tasks |
