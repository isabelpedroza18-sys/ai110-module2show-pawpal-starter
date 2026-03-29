# PawPal+ System API Documentation

## Class: Task
**Purpose:** Represents a single pet care activity with description, timing, frequency, and status.

### Methods
| Method | Signature | Docstring |
|--------|-----------|-----------|
| `get_details()` | `() -> str` | Return a formatted string with task details. |
| `is_high_priority()` | `() -> bool` | Check if task is high priority. |
| `mark_complete()` | `() -> None` | Mark the task as completed. |
| `mark_incomplete()` | `() -> None` | Mark the task as not completed. |

---

## Class: ScheduledTask
**Purpose:** Represents a task scheduled at a specific time.

### Methods
| Method | Signature | Docstring |
|--------|-----------|-----------|
| `get_scheduled_info()` | `() -> str` | Return formatted scheduled task information. |

---

## Class: Pet
**Purpose:** Represents a pet with owner, special needs, and associated tasks.

### Methods
| Method | Signature | Docstring |
|--------|-----------|-----------|
| `get_info()` | `() -> str` | Return formatted pet information. |
| `has_special_need()` | `(need: str) -> bool` | Check if pet has a specific special need. |
| `get_owner()` | `() -> Optional[Owner]` | Return the owner of this pet. |
| `set_owner()` | `(owner: Owner) -> None` | Set the owner of this pet. |
| `add_task()` | `(task: Task) -> None` | Add a task to the pet's task list. |
| `remove_task()` | `(task_name: str) -> None` | Remove a task by name from the pet's task list. |
| `get_tasks()` | `() -> List[Task]` | Return all tasks associated with this pet. |

---

## Class: Owner
**Purpose:** Represents a pet owner with schedule and preferences.

### Methods
| Method | Signature | Docstring |
|--------|-----------|-----------|
| `add_pet()` | `(pet: Pet) -> None` | Add a pet to the owner's pet list and set bidirectional relationship. |
| `remove_pet()` | `(pet_name: str) -> None` | Remove a pet by name and clear its owner reference. |
| `get_pets()` | `() -> List[Pet]` | Return list of pets owned by this owner. |
| `get_all_pets_tasks()` | `() -> List[Task]` | Return all tasks for all pets owned by this owner. |
| `get_available_hours()` | `(day: str) -> float` | Get available hours for a specific day. |
| `set_available_hours()` | `(day: str, hours: float) -> None` | Set available hours for a specific day. |
| `add_preference()` | `(preference: str) -> None` | Add a preference to the owner's preferences list. |

---

## Class: Scheduler
**Purpose:** Handles scheduling of pet care tasks for multiple pets based on owner availability and pet needs.

### Methods
| Method | Signature | Docstring |
|--------|-----------|-----------|
| `add_task()` | `(task: Task) -> None` | Add a task to the scheduler's task list. |
| `remove_task()` | `(task_name: str) -> None` | Remove a task by name from the scheduler's task list. |
| `generate_schedule()` | `(day: str) -> List[ScheduledTask]` | Generate an optimized schedule for a specific day with time slots. |
| `get_explanation()` | `() -> str` | Return an explanation of the scheduling logic and decisions. |
| `get_total_duration_needed()` | `() -> int` | Calculate total duration needed for all tasks in minutes. |
| `_sort_tasks_by_priority()` | `() -> List[Task]` | Sort tasks by priority (highest first). Private helper method. |
| `_validate_constraints()` | `() -> bool` | Validate that all required tasks and pet special needs are addressed. |
| `_check_feasibility()` | `(day: str) -> bool` | Check if all tasks fit within owner's available time for the day. |

---

## Key Relationships

### Bidirectional Links
- **Owner ↔ Pet**: One-to-many relationship (an owner can have multiple pets)
- **Pet ↔ Task**: One-to-many relationship (a pet can have multiple tasks)
- **Task ↔ Pet**: Back-reference to track which pet a task belongs to

### Usage Flow
1. Create an Owner with name and set available hours per day
2. Create Pets and add to Owner (maintains bidirectional relationship)
3. Create Tasks and add to Pets (maintains bidirectional relationship)
4. Create a Scheduler with Owner and Pets list
5. Call `generate_schedule(day)` to create optimized schedule
6. Call `get_explanation()` to understand scheduling decisions
