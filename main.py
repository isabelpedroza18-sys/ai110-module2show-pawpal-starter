from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime

# Create an Owner
owner = Owner("Sarah")
owner.set_available_hours("Monday", 4.0)  # 4 hours available on Monday

# Create Pets
dog = Pet(
    name="Max",
    breed="Golden Retriever",
    age=3,
    special_needs=["Diabetes medication"]
)

cat = Pet(
    name="Whiskers",
    breed="Persian",
    age=5,
    special_needs=["Medication"]
)

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Create Tasks for the dog
task1 = Task(
    name="Morning Walk",
    description="30-minute walk around the park",
    task_type="Exercise",
    duration_minutes=30,
    priority=8,
    required=True,
    frequency="daily"
)

task2 = Task(
    name="Diabetes Medication",
    description="Give insulin injection",
    task_type="Medication",
    duration_minutes=10,
    priority=9,
    required=True,
    frequency="twice daily"
)

task3 = Task(
    name="Lunch",
    description="Feed Max his lunch",
    task_type="Feeding",
    duration_minutes=15,
    priority=7,
    required=True,
    frequency="daily"
)

# Create Tasks for the cat
task4 = Task(
    name="Cat Medication",
    description="Give cat thyroid medication",
    task_type="Medication",
    duration_minutes=5,
    priority=10,
    required=True,
    frequency="daily"
)

task5 = Task(
    name="Cat Feeding",
    description="Feed Whiskers wet food",
    task_type="Feeding",
    duration_minutes=10,
    priority=8,
    required=True,
    frequency="daily"
)

# Add tasks to pets
dog.add_task(task1)
dog.add_task(task2)
dog.add_task(task3)

cat.add_task(task4)
cat.add_task(task5)

# Create a Scheduler
scheduler = Scheduler(owner, [dog, cat])

# Add all tasks to scheduler
for pet in [dog, cat]:
    for task in pet.get_tasks():
        scheduler.add_task(task)

# Generate schedule for Monday
today = "Monday"
schedule = scheduler.generate_schedule(today)

# Print Today's Schedule
print("\n" + "="*60)
print("TODAY'S SCHEDULE (PAWPAL+)")
print("="*60)
print(f"Date: {today}")
print(f"Owner: {owner.name}")
print(f"Pets: {', '.join([pet.name for pet in owner.get_pets()])}")
print(f"Available Time: {owner.get_available_hours(today)} hours")
print("="*60 + "\n")

if schedule:
    print("SCHEDULED TASKS:\n")
    for i, scheduled_task in enumerate(schedule, 1):
        task = scheduled_task.task
        print(f"{i}. {scheduled_task.time_slot} - {task.name}")
        print(f"   Pet: {task.pet.name}")
        print(f"   Description: {task.description}")
        print(f"   Duration: {task.duration_minutes} minutes")
        print(f"   Priority: {task.priority}/10")
        print()
else:
    print("No tasks scheduled.")

print("="*60)
print("\nDETAILED EXPLANATION:")
print("="*60)
print(scheduler.get_explanation())
print("="*60)
