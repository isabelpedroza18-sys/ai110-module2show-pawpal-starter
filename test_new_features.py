"""
Test script to demonstrate the four new scheduling features:
1. Sorting tasks by time
2. Filtering by pet/status
3. Handling recurring tasks
4. Basic conflict detection
"""

from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime

# Create an Owner
owner = Owner("Jordan")
owner.set_available_hours("Monday", 5.0)

# Create Pets
dog = Pet(name="Max", breed="Golden Retriever", age=3, special_needs={"diabetes medication"})
cat = Pet(name="Whiskers", breed="Persian", age=5, special_needs={"medication"})

owner.add_pet(dog)
owner.add_pet(cat)

# Create Tasks with different frequencies
task1 = Task(
    name="Morning Walk",
    description="30-minute walk",
    task_type="Exercise",
    duration_minutes=30,
    priority=8,
    required=True,
    frequency="daily"  # Daily recurring task
)

task2 = Task(
    name="Medication (Dog)",
    description="Give insulin injection",
    task_type="Medication",
    duration_minutes=10,
    priority=9,
    required=True,
    frequency="twice daily"  # Twice daily task
)

task3 = Task(
    name="Feeding",
    description="Feed Max",
    task_type="Feeding",
    duration_minutes=15,
    priority=7,
    required=True,
    frequency="daily"
)

task4 = Task(
    name="Cat Medication",
    description="Give cat medicine",
    task_type="Medication",
    duration_minutes=5,
    priority=10,
    required=True,
    frequency="once"
)

# Add tasks to pets
dog.add_task(task1)
dog.add_task(task2)
dog.add_task(task3)
cat.add_task(task4)

# Create scheduler and add tasks
scheduler = Scheduler(owner, [dog, cat])
for pet in [dog, cat]:
    for task in pet.get_tasks():
        scheduler.add_task(task)

# Generate schedule
print("=" * 70)
print("BASIC SCHEDULE FOR MONDAY")
print("=" * 70)
schedule = scheduler.generate_schedule("Monday")
for scheduled_task in schedule:
    print(f"{scheduled_task.time_slot} - {scheduled_task.task.name} ({scheduled_task.task.pet.name})")

print("\n" + "=" * 70)
print("FEATURE 1: SORTING TASKS BY TIME")
print("=" * 70)
sorted_by_time = scheduler.sort_scheduled_tasks_by_time()
print(f"Tasks sorted chronologically:")
for st in sorted_by_time:
    print(f"  {st.time_slot}: {st.task.name}")

print("\n" + "=" * 70)
print("FEATURE 2: FILTERING BY PET")
print("=" * 70)
max_tasks = scheduler.filter_by_pet("Max")
print(f"Tasks for Max ({len(max_tasks)}):")
for st in max_tasks:
    print(f"  - {st.task.name} at {st.time_slot}")

whiskers_tasks = scheduler.filter_by_pet("Whiskers")
print(f"\nTasks for Whiskers ({len(whiskers_tasks)}):")
for st in whiskers_tasks:
    print(f"  - {st.task.name} at {st.time_slot}")

print("\n" + "=" * 70)
print("FEATURE 2b: FILTERING BY STATUS")
print("=" * 70)
pending_tasks = scheduler.filter_by_status(False)
print(f"Pending tasks ({len(pending_tasks)}):")
for st in pending_tasks:
    print(f"  - {st.task.name} (Priority: {st.task.priority})")

# Mark one task as complete
schedule[0].task.mark_complete()
completed_tasks = scheduler.filter_by_status(True)
print(f"\nCompleted tasks ({len(completed_tasks)}):")
for st in completed_tasks:
    print(f"  - {st.task.name}")

print("\n" + "=" * 70)
print("FEATURE 3: HANDLING RECURRING TASKS")
print("=" * 70)
expanded = scheduler.expand_recurring_tasks("Monday", num_days=7)
print(f"Generated schedule for 7 days with recurring tasks:")
daily_count = {}
for st in expanded:
    task_name = st.task.name
    if task_name not in daily_count:
        daily_count[task_name] = 0
    daily_count[task_name] += 1

for task_name, count in sorted(daily_count.items()):
    print(f"  - {task_name}: {count} occurrence(s)")

print("\n" + "=" * 70)
print("FEATURE 4: CONFLICT DETECTION")
print("=" * 70)
conflicts = scheduler.detect_conflicts()
if conflicts:
    print(f"Found {len(conflicts)} scheduling conflict(s):")
    for task1, task2 in conflicts:
        print(f"  ⚠️  CONFLICT: {task1.task.name} ({task1.time_slot}) overlaps with {task2.task.name} ({task2.time_slot})")
else:
    print("✓ No scheduling conflicts detected! All tasks fit perfectly.")

print("\n" + "=" * 70)
print("SCHEDULE SUMMARY")
print("=" * 70)
print(f"Total scheduled tasks: {len(schedule)}")
print(f"Owner: {owner.name}")
print(f"Pets: {', '.join([p.name for p in owner.get_pets()])}")
print(f"Available time: {owner.get_available_hours('Monday')} hours")
print("=" * 70)
