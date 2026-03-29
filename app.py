import streamlit as st
from pawpal_system import Owner, Pet, Task, ScheduledTask, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# Initialize session state "vault" - check if objects already exist before creating
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** — your pet care planning assistant!

This app helps you create optimized daily schedules for your pet(s).
"""
)

st.divider()

# --- OWNER SETUP ---
st.subheader("Step 1: Owner Setup")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan", key="owner_input")

with col2:
    if st.button("Create/Load Owner", key="create_owner_btn"):
        # Check if owner already exists in session vault
        if st.session_state.owner is None:
            # Create new Owner using pawpal_system.Owner class
            st.session_state.owner = Owner(owner_name)
            st.success(f"✓ Owner '{owner_name}' created!")
        else:
            # Owner already exists - update name
            st.session_state.owner.name = owner_name
            st.info(f"✓ Owner name updated to '{owner_name}' (existing owner reused)")

# Display current owner
if st.session_state.owner:
    st.write(f"**Current Owner:** {st.session_state.owner.name}")
    
    # Set available hours using Owner.set_available_hours() method
    available_hours = st.slider(
        "Available hours (Monday)", 
        min_value=0.0, 
        max_value=24.0, 
        value=4.0,
        step=0.5,
        key="hours_slider"
    )
    if st.button("Set Available Hours", key="set_hours_btn"):
        st.session_state.owner.set_available_hours("Monday", available_hours)
        st.success(f"✓ Set {available_hours} hours available on Monday")
else:
    st.warning("👉 Create an owner first to begin!")

st.divider()

# --- PET MANAGEMENT ---
st.subheader("Step 2: Add Pets")

if st.session_state.owner:
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
    with col2:
        breed = st.text_input("Breed", value="Golden Retriever", key="breed_input")
    with col3:
        age = st.number_input("Age (years)", min_value=0, max_value=30, value=3, key="age_input")
    
    if st.button("Add Pet", key="add_pet_btn"):
        # Create Pet using pawpal_system.Pet class
        new_pet = Pet(
            name=pet_name,
            breed=breed,
            age=age,
            special_needs=[]
        )
        # Use Owner.add_pet() method to maintain bidirectional relationship
        st.session_state.owner.add_pet(new_pet)
        st.success(f"✓ Pet '{pet_name}' added to {st.session_state.owner.name}!")
    
    # Get all pets once and batch all pet-related calculations
    pets = st.session_state.owner.get_pets()
    pet_names = [p.name for p in pets]  # Compute once, reuse throughout
    
    # Display all pets from owner using Owner.get_pets() method
    if pets:
        st.write(f"**Your Pets ({len(pets)}):**")
        for pet in pets:
            st.write(f"🐾 {pet.name} — {pet.breed}, {pet.age} years old")
    
    st.divider()
    
    # --- REMOVE PET SECTION ---
    st.subheader("Remove Pet")
    
    if pets:
        pet_to_remove_name = st.selectbox("Select pet to remove", pet_names, key="pet_remove_select")
        
        if st.button("🗑️ Remove Pet", key="remove_pet_btn"):
            # Use Owner.remove_pet() method
            st.session_state.owner.remove_pet(pet_to_remove_name)
            st.success(f"✓ Pet '{pet_to_remove_name}' removed!")
            st.rerun()
    else:
        st.info("No pets to remove")
else:
    st.warning("👉 Create an owner first!")

st.divider()

# --- TASK MANAGEMENT ---
st.subheader("Step 3: Add Tasks")

if st.session_state.owner and st.session_state.owner.get_pets():
    # Get pets from owner's vault
    pets = st.session_state.owner.get_pets()
    pet_names = [p.name for p in pets]
    
    col1, col2 = st.columns(2)
    with col1:
        selected_pet_name = st.selectbox("Select pet for task", pet_names, key="pet_select")
    with col2:
        st.write("")  # Spacing
    
    task_name = st.text_input("Task name", value="Morning walk", key="task_name_input")
    description = st.text_area("Description", value="30-minute walk around the park", key="task_desc_input", height=80)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        duration = st.number_input("Duration (minutes)", min_value=1, value=30, key="duration_input")
    with col2:
        priority = st.slider("Priority (1-10)", 1, 10, 8, key="priority_input")
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "twice daily", "once"], key="freq_select")
    
    if st.button("Add Task", key="add_task_btn"):
        # Find the selected pet in owner's pet list
        selected_pet = next(p for p in pets if p.name == selected_pet_name)
        
        # Create Task using pawpal_system.Task class (dataclass)
        new_task = Task(
            name=task_name,
            description=description,
            task_type="General",
            duration_minutes=int(duration),
            priority=priority,
            required=True,
            frequency=frequency
        )
        
        # Use Pet.add_task() method to maintain bidirectional relationship
        selected_pet.add_task(new_task)
        st.success(f"✓ Task '{task_name}' added to {selected_pet_name}!")
    
    # Display all tasks by pet using Pet.get_tasks() method
    st.write("**Current Tasks:**")
    for pet in pets:
        tasks = pet.get_tasks()
        if tasks:
            st.write(f"*{pet.name}'s tasks:*")
            for task in tasks:
                st.caption(f"  • {task.name} ({task.duration_minutes}min, Priority {task.priority})")
        else:
            st.caption(f"  ℹ️ {pet.name} has no tasks yet")
    
    st.divider()
    
    # --- REMOVE TASK SECTION ---
    st.subheader("Remove or Edit Task")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_pet_for_removal = st.selectbox("Select pet", pet_names, key="pet_remove_select")
    with col2:
        removal_pet = next(p for p in pets if p.name == selected_pet_for_removal)
        removal_task_names = [t.name for t in removal_pet.get_tasks()]
        
        if removal_task_names:
            selected_task_name = st.selectbox("Select task to modify", removal_task_names, key="task_modify_select")
        else:
            st.info("No tasks for this pet")
    
    if removal_task_names:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Remove Task", key="remove_task_btn"):
                removal_pet.remove_task(selected_task_name)
                st.success(f"✓ Task '{selected_task_name}' removed from {selected_pet_for_removal}!")
        
        with col2:
            if st.button("✏️ Edit Task", key="edit_task_btn"):
                # Find the task to edit
                task_to_edit = next(t for t in removal_pet.get_tasks() if t.name == selected_task_name)
                st.session_state.edit_mode = True
                st.session_state.edit_task = task_to_edit
                st.session_state.edit_pet = removal_pet
    
    # Show edit form if in edit mode
    if "edit_mode" in st.session_state and st.session_state.edit_mode:
        st.subheader("Edit Task")
        task_to_edit = st.session_state.edit_task
        
        new_name = st.text_input("Task name", value=task_to_edit.name, key="edit_name")
        new_description = st.text_area("Description", value=task_to_edit.description, key="edit_desc", height=60)
        new_duration = st.number_input("Duration (minutes)", min_value=1, value=task_to_edit.duration_minutes, key="edit_duration")
        new_priority = st.slider("Priority (1-10)", 1, 10, task_to_edit.priority, key="edit_priority")
        new_frequency = st.selectbox("Frequency", ["daily", "weekly", "twice daily", "once"], key="edit_frequency")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes", key="save_edit_btn"):
                # Update task attributes
                task_to_edit.name = new_name
                task_to_edit.description = new_description
                task_to_edit.duration_minutes = new_duration
                task_to_edit.priority = new_priority
                task_to_edit.frequency = new_frequency
                
                st.success(f"✓ Task '{new_name}' updated!")
                st.session_state.edit_mode = False
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel", key="cancel_edit_btn"):
                st.session_state.edit_mode = False
                st.rerun()
else:
    st.warning("👉 Create an owner and at least one pet first!")

st.divider()

# --- SCHEDULE GENERATION ---
st.subheader("Step 4: Generate Schedule")

if st.session_state.owner and st.session_state.owner.get_pets():
    # Get pets from owner
    pets = st.session_state.owner.get_pets()
    has_tasks = any(pet.get_tasks() for pet in pets)
    
    if has_tasks:
        if st.button("🚀 Generate Schedule for Monday", key="generate_schedule_btn"):
            # Create Scheduler instance using pawpal_system.Scheduler class
            st.session_state.scheduler = Scheduler(st.session_state.owner, pets)
            
            # Add all tasks to scheduler using Scheduler.add_task() method
            for pet in pets:
                for task in pet.get_tasks():
                    st.session_state.scheduler.add_task(task)
            
            # Generate schedule using Scheduler.generate_schedule() method
            schedule = st.session_state.scheduler.generate_schedule("Monday")
            
            if schedule:
                st.success(f"✓ Schedule generated with {len(schedule)} tasks!")
                
                # Display schedule
                st.subheader("📅 Today's Schedule (Monday)")
                
                for idx, scheduled_task in enumerate(schedule, 1):
                    task = scheduled_task.task
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        st.write(f"**{scheduled_task.time_slot}**")
                    with col2:
                        st.write(f"{task.name} ({task.pet.name})")
                    with col3:
                        st.caption(f"{task.duration_minutes}min | ⭐{task.priority}")
                    st.caption(task.description)
                
                # Display explanation using Scheduler.get_explanation() method
                with st.expander("📝 See Detailed Explanation"):
                    st.write(st.session_state.scheduler.get_explanation())
            else:
                st.warning("⚠️ No tasks could be scheduled. Check available time vs. task duration.")
    else:
        st.info("💡 Add tasks to your pets before generating a schedule!")
else:
    st.warning("👉 Complete Steps 1-3 first!")

st.divider()

st.markdown("""
### How PawPal+ Works:
1. **Owner Setup** — Create your profile and set available hours
2. **Add Pets** — Register your pets with their breeds and ages
3. **Add Tasks** — Define pet care tasks with duration and priority
4. **Generate Schedule** — Get an optimized daily plan based on constraints
5. **View Explanation** — Understand why tasks were scheduled in that order

**Smart Scheduling:**
- 🎯 High-priority tasks (medication, feeding) scheduled first
- ⏰ Tasks fit within your available time
- 🐾 Each pet's special needs are considered
- 📊 Clear explanations of scheduling decisions
""")
