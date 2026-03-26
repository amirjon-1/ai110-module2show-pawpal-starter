from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: str
    is_complete: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    _tasks: list[Task] = field(default_factory=list, init=False, repr=False)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    _pets: list[Pet] = field(default_factory=list, init=False, repr=False)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> list[Pet]:
        pass


class Scheduler:
    def __init__(self, pet: Pet, available_minutes: int) -> None:
        self.pet = pet
        self.available_minutes = available_minutes

    def generate_plan(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass
