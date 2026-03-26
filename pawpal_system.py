from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


_PRIORITY_ORDER = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: Priority
    is_complete: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_complete = True


@dataclass
class Pet:
    name: str
    species: str
    age: int
    _tasks: list[Task] = field(default_factory=list, init=False, repr=False)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self._tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return a shallow copy of this pet's task list."""
        return list(self._tasks)


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    _pets: list[Pet] = field(default_factory=list, init=False, repr=False)

    def add_pet(self, pet: Pet) -> None:
        """Append a pet to this owner's pet list."""
        self._pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return a shallow copy of this owner's pet list."""
        return list(self._pets)


class Scheduler:
    def __init__(self, pet: Pet, available_minutes: int) -> None:
        """Initialise the scheduler with a pet and a time budget in minutes."""
        self.pet = pet
        self.available_minutes = available_minutes

    def generate_plan(self) -> list[Task]:
        """Return tasks sorted by priority that fit within the available time budget."""
        sorted_tasks = sorted(
            self.pet.get_tasks(),
            key=lambda t: _PRIORITY_ORDER[t.priority],
        )
        plan: list[Task] = []
        minutes_used = 0
        for task in sorted_tasks:
            if minutes_used + task.duration_minutes <= self.available_minutes:
                plan.append(task)
                minutes_used += task.duration_minutes
        return plan

    def explain_plan(self) -> str:
        """Return a human-readable summary of included and skipped tasks."""
        all_tasks = self.pet.get_tasks()
        plan = self.generate_plan()
        planned_names = {t.name for t in plan}
        skipped = [t for t in all_tasks if t.name not in planned_names]

        minutes_used = sum(t.duration_minutes for t in plan)
        lines: list[str] = [
            f"Schedule for {self.pet.name} "
            f"({minutes_used}/{self.available_minutes} minutes used):",
        ]

        if plan:
            lines.append("  Included:")
            for task in plan:
                lines.append(
                    f"    - {task.name} ({task.duration_minutes} min, {task.priority.value})"
                )
        else:
            lines.append("  Included: none")

        if skipped:
            lines.append("  Skipped (insufficient time):")
            for task in skipped:
                lines.append(
                    f"    - {task.name} ({task.duration_minutes} min, {task.priority.value})"
                )

        return "\n".join(lines)
