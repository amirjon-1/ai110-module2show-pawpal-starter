from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def main():
    # Create owner
    owner = Owner(name="Alex", available_minutes_per_day=60)

    # Create pets
    buddy = Pet(name="Buddy", species="Dog", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", age=5)

    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # Add tasks to Buddy
    buddy.add_task(Task(name="Morning walk",       duration_minutes=30, priority=Priority.HIGH))
    buddy.add_task(Task(name="Flea treatment",     duration_minutes=15, priority=Priority.HIGH))
    buddy.add_task(Task(name="Teeth brushing",     duration_minutes=10, priority=Priority.MEDIUM))
    buddy.add_task(Task(name="Fetch training",     duration_minutes=20, priority=Priority.LOW))

    # Add tasks to Whiskers
    whiskers.add_task(Task(name="Litter box clean", duration_minutes=10, priority=Priority.HIGH))
    whiskers.add_task(Task(name="Grooming",         duration_minutes=20, priority=Priority.MEDIUM))
    whiskers.add_task(Task(name="Laser toy play",   duration_minutes=15, priority=Priority.LOW))

    print("=" * 45)
    print("         PawPal+ — Today's Schedule")
    print("=" * 45)
    print(f"Owner : {owner.name}")
    print(f"Budget: {owner.available_minutes_per_day} minutes/day")
    print()

    for pet in owner.get_pets():
        scheduler = Scheduler(pet=pet, available_minutes=owner.available_minutes_per_day)
        print(scheduler.explain_plan())
        print()

    print("=" * 45)


if __name__ == "__main__":
    main()
