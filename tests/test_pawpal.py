from pawpal_system import Pet, Task, Priority


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
