# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

puthon -m pytest
the test suite in tests/test_pawpal.py comprehensively covers 19 tests across seven test classes. It validates core functionality including task status management (mark complete/incomplete), pet task operations (add, remove, retrieve tasks), and owner-level integration (accessing all pets' tasks). The tests also verify intelligent scheduling features: chronological sorting of scheduled tasks with proper handling of None times, recurring task expansion patterns (daily, twice-daily, weekly), duplicate prevention in the scheduler, and conflict detection for overlapping tasks. Together, these tests ensure the app's data model integrity, state management correctness, and scheduling logic accuracy across both baseline features and advanced optimizations.

Confidence level: 4 stars

## Features

### Core Data Model
- **Bidirectional Relationships**: Owner ↔ Pet, Pet ↔ Task relationships automatically maintained (when a pet is added to owner, owner reference is set on pet; when task is added to pet, pet reference is set on task)
- **Per-Day Availability**: Owner can set available hours for each day of the week independently (Monday–Sunday)
- **Task Metadata**: Tasks track name, description, type, duration (minutes), priority (1-10), frequency (daily/weekly/twice daily/once), and completion status
- **Pet Profiles**: Pets store breed, age, special needs (as optimized set for O(1) lookup), and maintain their own task list

### Scheduling Engine

#### 1. **Priority-Based Task Ordering Algorithm**
- Sorts all tasks by priority in descending order (highest first)
- High-priority tasks (priority > 7) are scheduled earlier in the day
- Required tasks take precedence over optional tasks
- Uses caching mechanism to optimize repeated sorts (cache invalidated when tasks added/removed)

#### 2. **Time Slot Allocation Algorithm**
- Generates time slots starting at 08:00 AM, spaced by task duration
- Calculates start_time and end_time for each ScheduledTask using datetime objects
- Formats time slots in human-readable format (e.g., "09:00 AM", "02:30 PM")
- Assigns tasks to specific day with chronological ordering

#### 3. **Conflict Detection Algorithm**
- Identifies overlapping tasks by comparing start_time and end_time
- Two tasks conflict if: `task1.start_time < task2.end_time AND task2.start_time < task1.end_time`
- Only detects conflicts on the same day
- Returns list of conflicting task pairs for user resolution

#### 4. **Feasibility Checking Algorithm**
- Validates that total task duration fits within owner's available hours for the day
- Calculates total duration by summing all task durations in minutes
- Converts owner's available hours to minutes for precise comparison
- Provides warning if tasks exceed available time (overbooking detection)

#### 5. **Constraint Validation Algorithm**
- Ensures all required tasks are included in the schedule
- Validates that pet special needs are addressed (matching task types to special needs)
- Checks data integrity before generating schedule
- Returns true only if all constraints satisfied

### Advanced Scheduling Features

#### 6. **Recurring Task Expansion Algorithm**
- Expands single tasks across multiple days based on frequency type:
  - **"daily"**: Task appears every day for num_days
  - **"twice daily"**: Task scheduled twice per day (morning and afternoon blocks)
  - **"weekly"**: Task appears once per week on the specified base_day
  - **"once"**: Task appears only on base_day
- Generates new ScheduledTask instances for each occurrence
- Preserves task metadata (duration, priority, pet reference)

#### 7. **Sorting & Filtering Pipelines**
- **Chronological Sort**: `sort_scheduled_tasks_by_time()` orders tasks by start_time (earliest first)
- **Pet Filter**: `filter_by_pet(pet_name)` returns only tasks for specific pet (useful for multi-pet households)
- **Status Filter**: `filter_by_status(is_completed)` separates completed from pending tasks
- All filters return filtered ScheduledTask lists without modifying original schedule

#### 8. **Explanation Generation Algorithm**
- Generates human-readable explanation of scheduling decisions
- Documents:
  - Owner name and pets involved
  - Total scheduled tasks count
  - Scheduling logic (3-rule priority algorithm)
  - List of all scheduled tasks with times
  - Unused time calculation and display (hours and minutes)
- Helps users understand why tasks were scheduled in that order

### User Interface Features

#### 9. **Multi-Day Schedule Support**
- Users can set available hours for each day of the week
- Generate schedules for any day (not limited to Monday)
- Schedule displays adapt to selected day

#### 10. **Real-Time Conflict Preview**
- Detects potential conflicts as tasks are added (before generation)
- Shows actual conflicts immediately after schedule generation
- Lists each conflicting pair with times and pet names
- Provides one-click resolution (remove conflicting task)

#### 11. **Professional Display Components**
- **Schedule Table**: Sortable dataframe with time, task, pet, duration, priority, day
- **Status Metrics**: Dashboard showing tasks scheduled, conflicts, time remaining, health status
- **Detailed Cards**: Expandable section showing full task descriptions
- **Advanced View**: Collapsible section for:
  - Sorting (by time, priority, or pet name)
  - Filtering (by specific pets)
  - View options (table, cards, or both)

#### 12. **Overbooking Detection & Warnings**
- Calculates exact overbooked duration
- Shows available hours vs. needed hours comparison
- Displays "Overbooked" status when tasks exceed available time
- Suggests solutions (remove tasks or increase available hours)
- Time remaining never displays as negative (capped at 0h 0m)


## Demo
<a href="/course_images/ai110/PawPalWeb.png" target="_blank"><img src='/course_images/ai110/PawPalWeb.png' title='PawPal+ App' width='600' alt='PawPal+ App' class='center-block' /></a>
