import streamlit as st
from pawpal_system import Owner, Pet, Task, ScheduledTask, Scheduler
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")


# ============================================================================
# HELPER FUNCTIONS FOR CONFLICT DETECTION & DISPLAY
# ============================================================================

def check_task_conflicts_with_existing(new_task: Task, pet, scheduler=None) -> list:
    """
    Check if a newly added task conflicts with existing scheduled tasks.
    Returns list of (existing_task, new_task) tuples that conflict.
    Returns empty list if no scheduler exists or no conflicts found.
    """
    if scheduler is None or not scheduler.scheduled_tasks:
        return []
    
    conflicts = []
    # Create a temporary scheduled task starting at 8:00 AM
    temp_start = datetime(2024, 1, 1, 8, 0, 0)
    temp_end = temp_start + timedelta(minutes=new_task.duration_minutes)
    temp_scheduled = ScheduledTask(
        task=new_task,
        time_slot="08:00 AM",
        day="Monday",
        start_time=temp_start,
        end_time=temp_end
    )
    
    # Check against all existing scheduled tasks
    for existing_scheduled in scheduler.scheduled_tasks:
        if temp_scheduled.has_conflict_with(existing_scheduled):
            conflicts.append((existing_scheduled.task, new_task))
    
    return conflicts


def format_schedule_dataframe(scheduled_tasks: list) -> pd.DataFrame:
    """
    Convert list of ScheduledTask objects to a formatted DataFrame for display.
    """
    data = []
    for st_item in scheduled_tasks:
        data.append({
            "⏰ Time": st_item.time_slot,
            "📋 Task": st_item.task.name,
            "🐾 Pet": st_item.task.pet.name,
            "⏱️ Duration (min)": st_item.task.duration_minutes,
            "⭐ Priority": st_item.task.priority,
            "📅 Day": st_item.day
        })
    return pd.DataFrame(data)


def sort_schedule(scheduled_tasks: list, sort_by: str = "time") -> list:
    """
    Sort scheduled tasks by time, priority, or pet name.
    Returns sorted list of ScheduledTask objects.
    """
    if sort_by == "time":
        return sorted(scheduled_tasks, key=lambda x: x.start_time if x.start_time else datetime.max)
    elif sort_by == "priority":
        return sorted(scheduled_tasks, key=lambda x: x.task.priority, reverse=True)
    elif sort_by == "pet":
        return sorted(scheduled_tasks, key=lambda x: x.task.pet.name)
    return scheduled_tasks


def filter_schedule_by_pets(scheduled_tasks: list, pet_names: list) -> list:
    """
    Filter scheduled tasks to only include specified pets.
    Returns filtered list of ScheduledTask objects.
    """
    if not pet_names:
        return scheduled_tasks
    return [st_item for st_item in scheduled_tasks if st_item.task.pet.name in pet_names]

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
    
    # Set available hours for any day of the week
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_day = st.selectbox(
            "Choose day of week",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            key="day_select"
        )
    
    with col2:
        available_hours = st.number_input(
            f"Available hours ({selected_day})",
            min_value=0.0,
            max_value=24.0,
            value=4.0,
            step=0.5,
            key="hours_input"
        )
    
    with col3:
        st.write("")  # Spacing
        if st.button("Set Available Hours", key="set_hours_btn"):
            st.session_state.owner.set_available_hours(selected_day, available_hours)
            st.success(f"✓ Set {available_hours} hours available on {selected_day}")
    
    # Display all set available hours
    all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    set_hours = {}
    for day in all_days:
        try:
            hours = st.session_state.owner.get_available_hours(day)
            if hours > 0:
                set_hours[day] = hours
        except:
            pass
    
    if set_hours:
        st.write("**Scheduled Hours:**")
        hours_display = " | ".join([f"{day}: {hours}h" for day, hours in set_hours.items()])
        st.caption(f"📅 {hours_display}")
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
        # Check if pet with this name already exists
        existing_pets = st.session_state.owner.get_pets()
        existing_names = [p.name for p in existing_pets]
        
        if pet_name in existing_names:
            st.warning(f"⚠️ A pet named '{pet_name}' already exists. Please use a different name.")
        else:
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
            st.rerun()
    
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
        
        # PHASE 1: Check for real-time conflicts with existing schedule
        if st.session_state.scheduler is not None:
            conflicts = check_task_conflicts_with_existing(new_task, selected_pet, st.session_state.scheduler)
            if conflicts:
                st.warning(
                    f"⚠️ **Potential Conflict Detected!**\n\n"
                    f"The task '{task_name}' may overlap with:\n"
                    + "\n".join([f"  • **{conflict[0].name}** ({conflict[0].pet.name})" for conflict in conflicts]) +
                    f"\n\n*This is a preview. Generate schedule to see final conflicts.*"
                )
    
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
        selected_pet_for_removal = st.selectbox("Select pet", pet_names, key="pet_select_for_task")
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
        col1, col2 = st.columns([2, 1])
        with col1:
            schedule_day = st.selectbox(
                "Select day to generate schedule for",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                key="schedule_day_select"
            )
        
        with col2:
            st.write("")  # Spacing
            generate_btn = st.button("🚀 Generate Schedule", key="generate_schedule_btn")
        
        if generate_btn:
            # Create Scheduler instance using pawpal_system.Scheduler class
            st.session_state.scheduler = Scheduler(st.session_state.owner, pets)
            
            # Add all tasks to scheduler using Scheduler.add_task() method
            for pet in pets:
                for task in pet.get_tasks():
                    st.session_state.scheduler.add_task(task)
            
            # Generate schedule using Scheduler.generate_schedule() method with selected day
            schedule = st.session_state.scheduler.generate_schedule(schedule_day)
            
            if schedule:
                st.success(f"✓ Schedule generated with {len(schedule)} tasks!")
                
                # PHASE 2: Detect conflicts post-generation
                conflicts = st.session_state.scheduler.detect_conflicts()
                
                # Display conflict warnings if any exist
                if conflicts:
                    with st.container(border=True):
                        st.error("🚨 **Scheduling Conflicts Detected!**")
                        st.markdown(f"**{len(conflicts)} conflict(s) found:**")
                        for conflict_pair in conflicts:
                            task1, task2 = conflict_pair
                            st.markdown(
                                f"  • **{task1.name}** ({task1.pet.name}) @ {task1.time_slot} "
                                f"overlaps with **{task2.name}** ({task2.pet.name}) @ {task2.time_slot}"
                            )
                        st.info("👉 Scroll down to **'🚨 Manage Conflicts'** section to resolve.")
                
                # PHASE 2: Display status indicator
                st.divider()
                cols = st.columns(4)
                with cols[0]:
                    st.metric("📊 Tasks Scheduled", len(schedule))
                with cols[1]:
                    st.metric("⚠️ Conflicts", len(conflicts))
                with cols[2]:
                    # Use get_available_hours() method to safely retrieve available hours for selected day
                    try:
                        owner_hours = st.session_state.owner.get_available_hours(schedule_day) * 60
                    except (AttributeError, TypeError):
                        owner_hours = 8 * 60  # Default to 8 hours if method doesn't work
                    
                    total_duration = sum(task.duration_minutes for task in st.session_state.scheduler.tasks)
                    unused_minutes = max(0, owner_hours - total_duration)  # Never go below 0
                    hours_left = unused_minutes // 60
                    mins_left = unused_minutes % 60
                    st.metric("⏰ Time Remaining", f"{int(hours_left)}h {int(mins_left)}m")
                with cols[3]:
                    # Check if tasks exceed available time
                    if total_duration > owner_hours:
                        status_color = "🔴"
                        status_text = "Overbooked"
                    elif len(conflicts) == 0:
                        status_color = "🟢"
                        status_text = "Healthy"
                    else:
                        status_color = "🔴"
                        status_text = "Issues"
                    st.metric("Status", f"{status_color} {status_text}")
                
                # Show warning if tasks exceed available time
                if total_duration > owner_hours:
                    st.warning(
                        f"⚠️ **Tasks exceed available time!**\n\n"
                        f"Available: {owner_hours / 60:.1f} hours\n"
                        f"Needed: {total_duration / 60:.1f} hours\n"
                        f"Overbooked by: {(total_duration - owner_hours) / 60:.1f} hours\n\n"
                        f"Consider removing tasks or increasing available hours."
                    )
                st.divider()
                
                # PHASE 2: Display schedule in table format (default sorted by time)
                sorted_schedule = st.session_state.scheduler.sort_scheduled_tasks_by_time()
                st.subheader(f"📅 {schedule_day}'s Schedule")
                
                # Create dataframe for table display
                schedule_df = format_schedule_dataframe(sorted_schedule)
                st.dataframe(
                    schedule_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "⏰ Time": st.column_config.TextColumn(width="medium"),
                        "📋 Task": st.column_config.TextColumn(width="large"),
                        "🐾 Pet": st.column_config.TextColumn(width="medium"),
                        "⏱️ Duration (min)": st.column_config.NumberColumn(width="small"),
                        "⭐ Priority": st.column_config.NumberColumn(width="small"),
                        "📅 Day": st.column_config.TextColumn(width="small"),
                    }
                )
                
                # PHASE 2: Expandable detailed view
                with st.expander("📝 Detailed Task Cards"):
                    st.write("*Expand below to see full task details and descriptions:*")
                    for idx, scheduled_task in enumerate(sorted_schedule, 1):
                        task = scheduled_task.task
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col1:
                                st.write(f"**{scheduled_task.time_slot}**")
                            with col2:
                                st.write(f"**{task.name}** ({task.pet.name})")
                            with col3:
                                st.caption(f"{task.duration_minutes}min | ⭐{task.priority}")
                            st.caption(f"*{task.description}*")
                
                # PHASE 3: Advanced View section with sorting & filtering
                with st.expander("⚙️ Advanced View"):
                    st.write("**Sort & Filter Options**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        sort_option = st.selectbox(
                            "Sort by:",
                            ["Time (earliest first)", "Priority (highest first)", "Pet Name"],
                            key="sort_select"
                        )
                    
                    with col2:
                        # Get unique pet names from schedule
                        all_pet_names = list(set(st_item.task.pet.name for st_item in sorted_schedule))
                        selected_pets = st.multiselect(
                            "Filter by pet:",
                            all_pet_names,
                            default=all_pet_names,
                            key="filter_pets_select"
                        )
                    
                    # Apply sorting based on selection
                    if sort_option == "Time (earliest first)":
                        filtered_schedule = filter_schedule_by_pets(sorted_schedule, selected_pets)
                    elif sort_option == "Priority (highest first)":
                        filtered_schedule = sort_schedule(sorted_schedule, sort_by="priority")
                        filtered_schedule = filter_schedule_by_pets(filtered_schedule, selected_pets)
                    else:  # Pet Name
                        filtered_schedule = sort_schedule(sorted_schedule, sort_by="pet")
                        filtered_schedule = filter_schedule_by_pets(filtered_schedule, selected_pets)
                    
                    # Display view toggle
                    view_option = st.radio(
                        "View as:",
                        ["Table", "Cards", "Both"],
                        horizontal=True,
                        key="view_toggle"
                    )
                    
                    # Render based on view option
                    if view_option in ["Table", "Both"]:
                        st.write("**Filtered & Sorted Schedule**")
                        filtered_df = format_schedule_dataframe(filtered_schedule)
                        st.dataframe(
                            filtered_df,
                            use_container_width=True,
                            hide_index=True,
                        )
                    
                    if view_option in ["Cards", "Both"]:
                        if view_option == "Both":
                            st.divider()
                        st.write("**Detailed View**")
                        for idx, scheduled_task in enumerate(filtered_schedule, 1):
                            task = scheduled_task.task
                            with st.container(border=True):
                                col1, col2, col3 = st.columns([1, 2, 1])
                                with col1:
                                    st.write(f"**{scheduled_task.time_slot}**")
                                with col2:
                                    st.write(f"**{task.name}** ({task.pet.name})")
                                with col3:
                                    st.caption(f"{task.duration_minutes}min | ⭐{task.priority}")
                                st.caption(f"*{task.description}*")
                
                # Display explanation using Scheduler.get_explanation() method
                with st.expander("📖 Scheduling Logic & Explanation"):
                    st.write(st.session_state.scheduler.get_explanation())
            else:
                st.warning("⚠️ No tasks could be scheduled. Check available time vs. task duration.")
    else:
        st.info("💡 Add tasks to your pets before generating a schedule!")
else:
    st.warning("👉 Complete Steps 1-3 first!")

st.divider()

# --- PHASE 4: CONFLICT RESOLUTION ---
if st.session_state.scheduler is not None and st.session_state.scheduler.detect_conflicts():
    st.subheader("🚨 Manage Conflicts")
    
    conflicts = st.session_state.scheduler.detect_conflicts()
    
    for idx, (task1, task2) in enumerate(conflicts, 1):
        with st.container(border=True):
            st.write(
                f"**Conflict {idx}:** {task1.name} ({task1.pet.name}) @ {task1.time_slot} "
                f"↔ {task2.name} ({task2.pet.name}) @ {task2.time_slot}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(
                    f"🗑️ Remove '{task1.name}'",
                    key=f"remove_conflict_{idx}_task1"
                ):
                    task1.pet.remove_task(task1.name)
                    st.success(f"✓ Task '{task1.name}' removed. Regenerate schedule to update.")
                    st.rerun()
            
            with col2:
                if st.button(
                    f"🗑️ Remove '{task2.name}'",
                    key=f"remove_conflict_{idx}_task2"
                ):
                    task2.pet.remove_task(task2.name)
                    st.success(f"✓ Task '{task2.name}' removed. Regenerate schedule to update.")
                    st.rerun()
    
    st.info("💡 **Tip:** Remove one conflicting task, then regenerate the schedule. Or edit task details in Step 3.")

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
