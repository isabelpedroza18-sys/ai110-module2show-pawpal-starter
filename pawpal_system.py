from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Task:
    """Represents a pet care task with priority and duration."""
    name: str
    task_type: str
    duration_minutes: int
    priority: int
    required: bool

    def get_details(self) -> str:
        """Return a formatted string with task details."""
        pass

    def is_high_priority(self) -> bool:
        """Check if task is high priority."""
        pass


@dataclass
class Pet:
    """Represents a pet with owner and special needs."""
    name: str
    breed: str
    age: int
    special_needs: List[str]
    owner: Optional['Owner'] = None

    def get_info(self) -> str:
        """Return formatted pet information."""
        pass

    def has_special_need(self, need: str) -> bool:
        """Check if pet has a specific special need."""
        pass

    def get_owner(self) -> Optional['Owner']:
        """Return the owner of this pet."""
        pass

    def set_owner(self, owner: 'Owner') -> None:
        """Set the owner of this pet."""
        pass


class Owner:
    """Represents a pet owner with schedule and preferences."""

    def __init__(self, name: str):
        self.name: str = name
        self.available_schedule: dict[str, float] = {}
        self.preferences: List[str] = []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        pass

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name from the owner's pet list."""
        pass

    def get_pets(self) -> List[Pet]:
        """Return list of pets owned by this owner."""
        pass

    def get_available_hours(self, day: str) -> float:
        """Get available hours for a specific day."""
        pass

    def set_available_hours(self, day: str, hours: float) -> None:
        """Set available hours for a specific day."""
        pass

    def add_preference(self, preference: str) -> None:
        """Add a preference to the owner's preferences list."""
        pass


class Scheduler:
    """Handles scheduling of pet care tasks based on owner availability and pet needs."""

    def __init__(self, owner: Owner, pet: Pet):
        self.owner: Owner = owner
        self.pet: Pet = pet
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler's task list."""
        pass

    def remove_task(self, task_name: str) -> None:
        """Remove a task by name from the scheduler's task list."""
        pass

    def generate_schedule(self, day: str) -> List[Task]:
        """Generate an optimized schedule for a specific day."""
        pass

    def get_explanation(self) -> str:
        """Return an explanation of the scheduling logic and decisions."""
        pass

    def get_total_duration_needed(self) -> int:
        """Calculate total duration needed for all tasks in minutes."""
        pass

    def _sort_tasks_by_priority(self) -> List[Task]:
        """Sort tasks by priority (highest first). Private helper method."""
        pass
