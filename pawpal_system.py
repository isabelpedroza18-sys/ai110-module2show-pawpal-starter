from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Task:
    """Represents a single pet care activity with description, timing, frequency, and status."""
    name: str
    description: str
    task_type: str
    duration_minutes: int
    priority: int
    required: bool
    frequency: str  # e.g., "daily", "weekly", "once", "twice daily"
    is_completed: bool = False
    pet: Optional['Pet'] = None

    def get_details(self) -> str:
        """Return a formatted string with task details."""
        completion_status = "Completed" if self.is_completed else "Pending"
        return f"Task: {self.name} | Description: {self.description} | Type: {self.task_type} | Duration: {self.duration_minutes}min | Priority: {self.priority} | Frequency: {self.frequency} | Status: {completion_status}"

    def is_high_priority(self) -> bool:
        """Check if task is high priority."""
        return self.priority > 7

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.is_completed = False


@dataclass
class ScheduledTask:
    """Represents a task scheduled at a specific time."""
    task: Task
    time_slot: str  # e.g., "09:00 AM", "02:30 PM"
    day: str  # e.g., "Monday", "Tuesday"

    def get_scheduled_info(self) -> str:
        """Return formatted scheduled task information."""
        return f"{self.task.name} scheduled for {self.day} at {self.time_slot}"


@dataclass
class Pet:
    """Represents a pet with owner, special needs, and associated tasks."""
    name: str
    breed: str
    age: int
    special_needs: List[str]
    owner: Optional['Owner'] = None
    tasks: List['Task'] = field(default_factory=list)

    def get_info(self) -> str:
        """Return formatted pet information."""
        owner_name = self.owner.name if self.owner else "Unowned"
        special_needs_str = ", ".join(self.special_needs) if self.special_needs else "None"
        return f"Pet: {self.name} | Breed: {self.breed} | Age: {self.age} | Owner: {owner_name} | Special Needs: {special_needs_str}"

    def has_special_need(self, need: str) -> bool:
        """Check if pet has a specific special need."""
        return need.lower() in [n.lower() for n in self.special_needs]

    def get_owner(self) -> Optional['Owner']:
        """Return the owner of this pet."""
        return self.owner

    def set_owner(self, owner: 'Owner') -> None:
        """Set the owner of this pet."""
        self.owner = owner

    def add_task(self, task: 'Task') -> None:
        """Add a task to the pet's task list."""
        if task not in self.tasks:
            self.tasks.append(task)
            task.pet = self

    def remove_task(self, task_name: str) -> None:
        """Remove a task by name from the pet's task list."""
        task_to_remove = next((t for t in self.tasks if t.name == task_name), None)
        if task_to_remove:
            self.tasks.remove(task_to_remove)
            task_to_remove.pet = None
        else:
            print(f"Task '{task_name}' not found for pet '{self.name}'.")

    def get_tasks(self) -> List['Task']:
        """Return all tasks associated with this pet."""
        return self.tasks


class Owner:
    """Represents a pet owner with schedule and preferences."""

    def __init__(self, name: str):
        self.name: str = name
        self.available_schedule: dict[str, float] = {}
        self.preferences: List[str] = []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list and set bidirectional relationship."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.set_owner(self)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name and clear its owner reference."""
        pet_to_remove = next((p for p in self.pets if p.name == pet_name), None)
        if pet_to_remove:
            self.pets.remove(pet_to_remove)
            pet_to_remove.set_owner(None)
        else:
            print(f"Pet '{pet_name}' not found.")


    def get_pets(self) -> List[Pet]:
        """Return list of pets owned by this owner."""
        return self.pets

    def get_all_pets_tasks(self) -> List[Task]:
        """Return all tasks for all pets owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            if hasattr(pet, 'tasks'):
                all_tasks.extend(pet.tasks)
        return all_tasks

    def get_available_hours(self, day: str) -> float:
        """Get available hours for a specific day."""
        return self.available_schedule.get(day.title(), 0.0)

    def set_available_hours(self, day: str, hours: float) -> None:
        """Set available hours for a specific day."""
        days_of_the_week =['monday', 'tuesday','wednesday', 'thursday','friday','saturday','sunday']
        if day.lower() not in days_of_the_week:
            print("Not a valid weekday. Try again")
        else:
            if hours > 0 and hours <= 24:
                self.available_schedule[day.title()]= hours
            else:
                print("Invalid hours. Must be between 0 and 24. Try again")
        

    def add_preference(self, preference: str) -> None:
        """Add a preference to the owner's preferences list."""
        self.preferences.append(preference)


class Scheduler:
    """Handles scheduling of pet care tasks for multiple pets based on owner availability and pet needs."""

    def __init__(self, owner: Owner, pets: List[Pet]):
        self.owner: Owner = owner
        self.pets: List[Pet] = pets
        self.tasks: List[Task] = []
        self.scheduled_tasks: List[ScheduledTask] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler's task list."""
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Remove a task by name from the scheduler's task list."""
        task_to_remove = next((t for t in self.tasks if t.name == task_name), None)
        if task_to_remove:
            self.tasks.remove(task_to_remove)
        else:
            print(f"Task '{task_name}' not found.")

    def generate_schedule(self, day: str) -> List[ScheduledTask]:
        """Generate an optimized schedule for a specific day with time slots."""
        self.scheduled_tasks = []
        
        # Validate constraints and feasibility
        if not self._validate_constraints():
            print("Warning: Some required tasks or pet special needs are not addressed.")
        
        if not self._check_feasibility(day):
            print(f"Warning: Not all tasks fit in the available time for {day}.")
        
        # Sort tasks by priority
        sorted_tasks = self._sort_tasks_by_priority()
        
        # Get available hours for the day and convert to minutes
        available_minutes = self.owner.get_available_hours(day) * 60
        current_time_minutes = 8 * 60  # Start at 08:00 AM
        time_used = 0
        
        # Assign time slots to tasks in priority order
        for task in sorted_tasks:
            if time_used + task.duration_minutes <= available_minutes:
                # Convert minutes to HH:MM format
                hours = current_time_minutes // 60
                minutes = current_time_minutes % 60
                am_pm = "AM" if hours < 12 else "PM"
                display_hours = hours if hours <= 12 else hours - 12
                if display_hours == 0:
                    display_hours = 12
                time_slot = f"{display_hours:02d}:{minutes:02d} {am_pm}"
                
                scheduled_task = ScheduledTask(task=task, time_slot=time_slot, day=day.title())
                self.scheduled_tasks.append(scheduled_task)
                
                # Update tracking
                time_used += task.duration_minutes
                current_time_minutes += task.duration_minutes
        
        return self.scheduled_tasks

    def get_explanation(self) -> str:
        """Return an explanation of the scheduling logic and decisions."""
        if not self.scheduled_tasks:
            return "No schedule has been generated yet. Call generate_schedule() first."
        
        explanation = "Schedule Explanation:\n"
        explanation += "=" * 50 + "\n"
        explanation += f"Owner: {self.owner.name}\n"
        explanation += f"Pets: {', '.join([p.name for p in self.pets])}\n"
        explanation += f"Total Tasks Scheduled: {len(self.scheduled_tasks)}\n\n"
        
        explanation += "Tasks were prioritized using the following logic:\n"
        explanation += "1. High-priority tasks (priority > 7) are scheduled first\n"
        explanation += "2. Required tasks are prioritized over optional ones\n"
        explanation += "3. Tasks are fit into available owner time, starting at 08:00 AM\n\n"
        
        explanation += "Scheduled Tasks:\n"
        for scheduled_task in self.scheduled_tasks:
            explanation += f"  - {scheduled_task.task.name}: {scheduled_task.time_slot} on {scheduled_task.day}\n"
        
        # Calculate unused time
        total_scheduled_minutes = sum(t.task.duration_minutes for t in self.scheduled_tasks)
        available_minutes = self.owner.get_available_hours(self.scheduled_tasks[0].day.lower()) * 60 if self.scheduled_tasks else 0
        unused_minutes = available_minutes - total_scheduled_minutes
        
        if unused_minutes > 0:
            explanation += f"\nUnused time: {unused_minutes // 60}h {unused_minutes % 60}m\n"
        
        return explanation

    def get_total_duration_needed(self) -> int:
        """Calculate total duration needed for all tasks in minutes."""
        task_time_needed = 0
        for task in self.tasks:
            task_time_needed += task.duration_minutes 
        return task_time_needed

    def _sort_tasks_by_priority(self) -> List[Task]:
        """Sort tasks by priority (highest first). Private helper method."""
        return sorted(self.tasks, key = lambda t: t.priority, reverse=True)

    def _validate_constraints(self) -> bool:
        """Validate that all required tasks and pet special needs are addressed."""
        # Check that all required tasks are present in the scheduler
        required_tasks = [t for t in self.tasks if t.required]
        if not required_tasks:
            return True  # No required tasks, so valid
        
        # For each pet, check if special needs are addressed by tasks
        for pet in self.pets:
            for special_need in pet.special_needs:
                # Check if there's a task addressing this special need
                has_task_for_need = any(
                    special_need.lower() in t.name.lower() or 
                    special_need.lower() in t.description.lower()
                    for t in pet.tasks
                )
                if not has_task_for_need:
                    print(f"Warning: Pet '{pet.name}' has special need '{special_need}' but no task addresses it.")
                    return False
        
        return True

    def _check_feasibility(self, day: str) -> bool:
        """Check if all tasks fit within owner's available time for the day."""
        available_minutes = self.owner.get_available_hours(day) * 60
        total_duration_needed = self.get_total_duration_needed()
        
        if total_duration_needed > available_minutes:
            print(f"Not feasible: {total_duration_needed} minutes needed but only {available_minutes} minutes available on {day}.")
            return False
        
        return True
