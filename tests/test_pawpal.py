import datetime

from pawpal_system import Pet, Task, Priority, Scheduler


def test_mark_complete_sets_is_complete():
    task = Task(name="Morning walk", duration_minutes=30, priority=Priority.HIGH)
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(name="Flea treatment", duration_minutes=15, priority=Priority.MEDIUM))
    assert len(pet.get_tasks()) == 1


def test_sort_tasks_by_duration_shortest_first():
    pet = Pet(name="Luna", species="Cat", age=2)
    pet.add_task(Task(name="Bath", duration_minutes=45, priority=Priority.LOW))
    pet.add_task(Task(name="Pill", duration_minutes=5, priority=Priority.HIGH))
    pet.add_task(Task(name="Walk", duration_minutes=20, priority=Priority.MEDIUM))
    scheduler = Scheduler(pet, available_minutes=120)
    sorted_tasks = scheduler.sort_tasks_by_duration()
    durations = [t.duration_minutes for t in sorted_tasks]
    assert durations == [5, 20, 45]


def test_mark_complete_daily_task_creates_new_task_due_tomorrow():
    today = datetime.date(2026, 3, 25)
    task = Task(name="Morning walk", duration_minutes=30, priority=Priority.HIGH,
                recurrence="daily", due_date=today)
    next_task = task.mark_complete()
    assert task.is_complete is True
    assert next_task is not None
    assert next_task.due_date == datetime.date(2026, 3, 26)
    assert next_task.is_complete is False


def test_detect_conflicts_flags_tasks_exceeding_budget():
    today = datetime.date(2026, 3, 25)
    pet = Pet(name="Rex", species="Dog", age=4)
    pet.add_task(Task(name="Vet visit", duration_minutes=50, priority=Priority.HIGH, due_date=today))
    pet.add_task(Task(name="Grooming", duration_minutes=40, priority=Priority.MEDIUM, due_date=today))
    scheduler = Scheduler(pet, available_minutes=60)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "Vet visit" in conflicts[0]
    assert "Grooming" in conflicts[0]


def test_pet_with_no_tasks_returns_empty_plan():
    pet = Pet(name="Mochi", species="Cat", age=1)
    scheduler = Scheduler(pet, available_minutes=120)
    assert scheduler.generate_plan() == []


def test_filter_tasks_returns_only_incomplete():
    pet = Pet(name="Buddy", species="Dog", age=3)
    done = Task(name="Bath", duration_minutes=20, priority=Priority.LOW)
    done.mark_complete()
    pending = Task(name="Walk", duration_minutes=30, priority=Priority.HIGH)
    pet.add_task(done)
    pet.add_task(pending)
    scheduler = Scheduler(pet, available_minutes=120)
    incomplete = scheduler.filter_tasks(completed=False)
    assert len(incomplete) == 1
    assert incomplete[0].name == "Walk"
