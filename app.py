from pawpal_system import Owner, Pet, Task, Scheduler, Priority
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Owner setup (runs once; persists across reruns via session_state) ---

if "owner" not in st.session_state:
    st.subheader("Create your owner profile")
    with st.form("owner_form"):
        owner_name = st.text_input("Your name", value="Jordan")
        available_minutes = st.number_input(
            "Available minutes per day",
            min_value=1,
            max_value=1440,
            value=60,
        )
        submitted = st.form_submit_button("Save profile")

    if submitted:
        st.session_state.owner = Owner(
            name=owner_name,
            available_minutes_per_day=int(available_minutes),
        )
        st.rerun()

    st.stop()

# --- Everything below only runs once an Owner exists ---

owner: Owner = st.session_state.owner
st.success(
    f"Owner: **{owner.name}** — {owner.available_minutes_per_day} min/day available"
)

if st.button("Reset owner profile"):
    del st.session_state.owner
    st.rerun()

st.divider()

# --- Add pet ---

st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
    st.rerun()

pets = owner.get_pets()
if not pets:
    st.info("No pets yet. Add one above.")
    st.stop()

st.write(f"**{len(pets)} pet(s):** " + ", ".join(p.name for p in pets))

st.divider()

# --- Add task ---

st.subheader("Add a Task")
with st.form("add_task_form"):
    selected_pet_name = st.selectbox("Pet", [p.name for p in pets])
    task_name = st.text_input("Task name", value="Morning walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["high", "medium", "low"])
    add_task_submitted = st.form_submit_button("Add task")

if add_task_submitted:
    target_pet = next(p for p in pets if p.name == selected_pet_name)
    target_pet.add_task(Task(
        name=task_name,
        duration_minutes=int(duration),
        priority=Priority[priority.upper()],
    ))
    st.rerun()

for pet in pets:
    tasks = pet.get_tasks()
    if tasks:
        with st.expander(f"{pet.name}'s tasks ({len(tasks)})"):
            st.table([
                {
                    "Task": t.name,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority.value,
                    "Complete": t.is_complete,
                }
                for t in tasks
            ])

st.divider()

# --- Generate plan ---

st.subheader("Generate Plan")
selected_plan_pet_name = st.selectbox("Select pet to schedule", [p.name for p in pets], key="plan_pet")

if st.button("Generate schedule"):
    plan_pet = next(p for p in pets if p.name == selected_plan_pet_name)

    if not plan_pet.get_tasks():
        st.warning(f"{plan_pet.name} has no tasks. Add some above first.")
    else:
        scheduler = Scheduler(pet=plan_pet, available_minutes=owner.available_minutes_per_day)
        plan = scheduler.generate_plan()
        explanation = scheduler.explain_plan()

        st.markdown("#### Today's Schedule")
        st.code(explanation)

        if plan:
            total = sum(t.duration_minutes for t in plan)
            st.progress(
                total / owner.available_minutes_per_day,
                text=f"{total} of {owner.available_minutes_per_day} minutes used",
            )
