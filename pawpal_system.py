from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, timedelta


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
    start_time: Optional[datetime] = None  # Actual datetime for conflict detection
    end_time: Optional[datetime] = None    # End time for duration tracking

    def get_scheduled_info(self) -> str:
        """Return formatted scheduled task information."""
        return f"{self.task.name} scheduled for {self.day} at {self.time_slot}"
    
    def has_conflict_with(self, other: 'ScheduledTask') -> bool:
        """Check if this task overlaps with another on the same day."""
        if self.day != other.day or self.start_time is None or other.start_time is None:
            return False
        # Tasks conflict if one starts before the other ends
        return self.start_time < other.end_time and other.start_time < self.end_time


@dataclass
class Pet:
    """Represents a pet with owner, special needs, and associated tasks."""
    name: str
    breed: str
    age: int
    special_needs: set[str]
    owner: Optional['Owner'] = None
    tasks: List['Task'] = field(default_factory=list)
    
    def __post_init__(self):
        """Normalize special_needs to lowercase set for consistent case-insensitive lookups."""
        if isinstance(self.special_needs, list):
            self.special_needs = {need.lower() for need in self.special_needs}
        else:
            self.special_needs = {need.lower() for need in self.special_needs}

    def get_info(self) -> str:
        """Return formatted pet information."""
        owner_name = self.owner.name if self.owner else "Unowned"
        special_needs_str = ", ".join(sorted(self.special_needs)) if self.special_needs else "None"
        return f"Pet: {self.name} | Breed: {self.breed} | Age: {self.age} | Owner: {owner_name} | Special Needs: {special_needs_str}"

    def has_special_need(self, need: str) -> bool:
        """Check if pet has a specific special need (O(1) set lookup)."""
        return need.lower() in self.special_needs

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
        return [task for pet in self.pets for task in pet.tasks]

    def get_available_hours(self, day: str) -> float:
        """Get available hours for a specific day (using lowercase normalized key)."""
        return self.available_schedule.get(day.lower(), 0.0)

    def set_available_hours(self, day: str, hours: float) -> None:
        """Set available hours for a specific day (using lowercase normalized key)."""
        days_of_the_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_lower = day.lower()
        if day_lower not in days_of_the_week:
            print("Not a valid weekday. Try again")
        else:
            if hours > 0 and hours <= 24:
                self.available_schedule[day_lower] = hours
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
        self._sorted_tasks_cache: Optional[List[Task]] = None

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler's task list (preventing duplicates)."""
        if task not in self.tasks:
            self.tasks.append(task)
            self._sorted_tasks_cache = None  # Invalidate cache

    def remove_task(self, task_name: str) -> None:
        """Remove a task by name from the scheduler's task list."""
        task_to_remove = next((t for t in self.tasks if t.name == task_name), None)
        if task_to_remove:
            self.tasks.remove(task_to_remove)
            self._sorted_tasks_cache = None  # Invalidate cache
        else:
            print(f"Task '{task_name}' not found.")

    def generate_schedule(self, day: str) -> List[ScheduledTask]:
        """Generate an optimized schedule for a specific day with time slots."""
        self.scheduled_tasks = []
        
        # Calculate total duration needed once (for validation and reuse)
        total_duration_needed = self.get_total_duration_needed()
        
        # Validate constraints and feasibility
        if not self._validate_constraints():
            print("Warning: Some required tasks or pet special needs are not addressed.")
        
        available_minutes = self.owner.get_available_hours(day) * 60
        if total_duration_needed > available_minutes:
            print(f"Warning: Not all tasks fit in the available time for {day}.")
        
        # Sort tasks by priority
        sorted_tasks = self._sort_tasks_by_priority()
        
        # Set up time tracking with datetime for cleaner formatting
        current_time = datetime.strptime("08:00", "%H:%M")  # Start at 08:00 AM
        time_used = 0
        
        # Assign time slots to tasks in priority order
        for task in sorted_tasks:
            if time_used + task.duration_minutes <= available_minutes:
                # Format time using strftime for cleaner code
                time_slot = current_time.strftime("%I:%M %p")
                end_time = current_time + timedelta(minutes=task.duration_minutes)
                
                scheduled_task = ScheduledTask(
                    task=task, 
                    time_slot=time_slot, 
                    day=day.title(),
                    start_time=current_time.replace(year=2024),  # Use consistent year for comparison
                    end_time=end_time.replace(year=2024)
                )
                self.scheduled_tasks.append(scheduled_task)
                
                # Update tracking
                time_used += task.duration_minutes
                current_time += timedelta(minutes=task.duration_minutes)
        
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
        if self._sorted_tasks_cache is None:
            self._sorted_tasks_cache = sorted(self.tasks, key=lambda t: t.priority, reverse=True)
        return self._sorted_tasks_cache

    def _validate_constraints(self) -> bool:
        """Validate that all required tasks and pet special needs are addressed."""
        # Check that all required tasks are present in the scheduler
        required_tasks = [t for t in self.tasks if t.required]
        if not required_tasks:
            return True  # No required tasks, so valid
        
        # For each pet, build a combined lowercase string for efficient substring matching
        for pet in self.pets:
            if not pet.special_needs:
                continue  # No special needs to validate
            
            # Create a single lowercase string combining all task content for efficient matching
            task_content = " ".join(
                f"{task.name} {task.description}".lower() 
                for task in pet.tasks
            )
            
            # Check each special need with simple substring matching (very fast)
            for special_need in pet.special_needs:
                if special_need not in task_content:
                    print(f"Warning: Pet '{pet.name}' has special need '{special_need}' but no task addresses it.")
                    return False
        
        return True

    def _check_feasibility(self, day: str) -> bool:
        """Check if all tasks fit within owner's available time for the day."""
        available_minutes = self.owner.get_available_hours(day) * 60
        total_duration_needed = self.get_total_duration_needed()
        
        if total_duration_needed <= available_minutes:
            return True
        
        print(f"Not feasible: {total_duration_needed} minutes needed but only {available_minutes} minutes available on {day}.")
        return False

    def sort_scheduled_tasks_by_time(self) -> List[ScheduledTask]:
        """Sort all scheduled tasks chronologically by start time."""
        if not self.scheduled_tasks:
            return []
        return sorted(self.scheduled_tasks, key=lambda st: st.start_time if st.start_time else datetime.max)

    def filter_by_pet(self, pet_name: str) -> List[ScheduledTask]:
        """Get all scheduled tasks for a specific pet."""
        return [st for st in self.scheduled_tasks if st.task.pet and st.task.pet.name == pet_name]

    def filter_by_status(self, is_completed: bool) -> List[ScheduledTask]:
        """Get scheduled tasks filtered by completion status."""
        return [st for st in self.scheduled_tasks if st.task.is_completed == is_completed]

    def expand_recurring_tasks(self, base_day: str, num_days: int = 7) -> List[ScheduledTask]:
        """Expand recurring tasks across multiple days based on frequency."""
        expanded_schedule = []
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        base_day_lower = base_day.lower()
        start_index = days_of_week.index(base_day_lower) if base_day_lower in days_of_week else 0
        
        for task in self.tasks:
            # Add initial scheduled task
            matching_scheduled = [st for st in self.scheduled_tasks if st.task == task]
            if matching_scheduled:
                expanded_schedule.extend(matching_scheduled)
            
            # Expand recurring tasks
            if task.frequency == "daily":
                for day_offset in range(1, min(num_days, 7)):
                    next_day_index = (start_index + day_offset) % 7
                    next_day = days_of_week[next_day_index].title()
                    # Create duplicate with new day
                    if matching_scheduled:
                        original = matching_scheduled[0]
                        expanded_schedule.append(ScheduledTask(
                            task=task,
                            time_slot=original.time_slot,
                            day=next_day,
                            start_time=original.start_time,
                            end_time=original.end_time
                        ))
            elif task.frequency == "twice daily":
                if matching_scheduled:
                    original = matching_scheduled[0]
                    # Add a second time slot for the same day (afternoon)
                    afternoon_time = original.start_time + timedelta(hours=6) if original.start_time else None
                    if afternoon_time:
                        expanded_schedule.append(ScheduledTask(
                            task=task,
                            time_slot=afternoon_time.strftime("%I:%M %p"),
                            day=original.day,
                            start_time=afternoon_time,
                            end_time=afternoon_time + timedelta(minutes=task.duration_minutes)
                        ))
            elif task.frequency == "weekly":
                # Recur once per week for num_days
                if num_days >= 7 and matching_scheduled:
                    original = matching_scheduled[0]
                    expanded_schedule.append(ScheduledTask(
                        task=task,
                        time_slot=original.time_slot,
                        day=original.day,
                        start_time=original.start_time,
                        end_time=original.end_time
                    ))
        
        return expanded_schedule

    def detect_conflicts(self) -> List[tuple[ScheduledTask, ScheduledTask]]:
        """Identify overlapping scheduled tasks that create conflicts."""
        conflicts = []
        for i, task1 in enumerate(self.scheduled_tasks):
            for task2 in self.scheduled_tasks[i + 1:]:
                if task1.has_conflict_with(task2):
                    conflicts.append((task1, task2))
        return conflicts
