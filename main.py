from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def print_section(title: str) -> None:
    print(f"\n--- {title} ---")


def main():
    # Create owner
    owner = Owner(name="Alex", available_minutes_per_day=60)

    # Create pet
    buddy = Pet(name="Buddy", species="Dog", age=3)
    owner.add_pet(buddy)

    # Add tasks intentionally out of order (long, short, medium, shortest)
    buddy.add_task(Task(name="Morning walk",   duration_minutes=30, priority=Priority.HIGH))
    buddy.add_task(Task(name="Flea treatment", duration_minutes=15, priority=Priority.HIGH))
    buddy.add_task(Task(name="Fetch training", duration_minutes=20, priority=Priority.LOW))
    buddy.add_task(Task(name="Teeth brushing", duration_minutes=10, priority=Priority.MEDIUM))

    scheduler = Scheduler(pet=buddy, available_minutes=owner.available_minutes_per_day)

    # Mark one task complete so filtering has something to show
    buddy.get_tasks()[0].mark_complete()  # Morning walk → complete

    print("=" * 45)
    print("         PawPal+ — Method Verification")
    print("=" * 45)

    print_section("Tasks as added (insertion order)")
    for t in buddy.get_tasks():
        print(f"  {t.name:<20} {t.duration_minutes:>3} min  complete={t.is_complete}")

    print_section("sort_tasks_by_duration() — shortest first")
    for t in scheduler.sort_tasks_by_duration():
        print(f"  {t.name:<20} {t.duration_minutes:>3} min")

    print_section("filter_tasks(completed=True)")
    done = scheduler.filter_tasks(completed=True)
    print(f"  {len(done)} task(s): " + (", ".join(t.name for t in done) or "none"))

    print_section("filter_tasks(completed=False)")
    pending = scheduler.filter_tasks(completed=False)
    print(f"  {len(pending)} task(s): " + (", ".join(t.name for t in pending) or "none"))

    print_section("generate_plan() + explain_plan()")
    print(scheduler.explain_plan())

    print("\n" + "=" * 45)


if __name__ == "__main__":
    main()
