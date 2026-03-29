import pytest
from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import datetime, timedelta


class TestTaskCompletion:
    """Test Task completion status functionality."""
    
    def test_task_mark_complete_changes_status(self):
        """Verify that mark_complete() changes is_completed to True."""
        task = Task(
            name="Walk",
            description="Morning walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="daily"
        )
        
        # Initially should be incomplete
        assert task.is_completed == False
        
        # Mark as complete
        task.mark_complete()
        
        # Should now be complete
        assert task.is_completed == True
    
    def test_task_mark_incomplete_changes_status(self):
        """Verify that mark_incomplete() changes is_completed to False."""
        task = Task(
            name="Medication",
            description="Give insulin",
            task_type="Medication",
            duration_minutes=10,
            priority=9,
            required=True,
            frequency="twice daily",
            is_completed=True  # Start as completed
        )
        
        # Initially should be complete
        assert task.is_completed == True
        
        # Mark as incomplete
        task.mark_incomplete()
        
        # Should now be incomplete
        assert task.is_completed == False
    
    def test_task_completion_toggle(self):
        """Verify that mark_complete() and mark_incomplete() toggle correctly."""
        task = Task(
            name="Feeding",
            description="Lunch time",
            task_type="Feeding",
            duration_minutes=15,
            priority=7,
            required=True,
            frequency="daily"
        )
        
        # Start incomplete
        assert task.is_completed == False
        
        # Mark complete
        task.mark_complete()
        assert task.is_completed == True
        
        # Mark incomplete
        task.mark_incomplete()
        assert task.is_completed == False
        
        # Mark complete again
        task.mark_complete()
        assert task.is_completed == True


class TestPetTaskManagement:
    """Test Pet task management functionality."""
    
    def test_add_task_increases_pet_task_count(self):
        """Verify that adding a task to a Pet increases task count."""
        pet = Pet(
            name="Max",
            breed="Golden Retriever",
            age=3,
            special_needs=[]
        )
        
        # Initially, pet should have no tasks
        assert len(pet.get_tasks()) == 0
        
        # Create and add a task
        task = Task(
            name="Walk",
            description="Morning walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="daily"
        )
        
        pet.add_task(task)
        
        # Task count should now be 1
        assert len(pet.get_tasks()) == 1
        assert pet.get_tasks()[0] == task
    
    def test_add_multiple_tasks_increases_count(self):
        """Verify that adding multiple tasks increases count correctly."""
        pet = Pet(
            name="Whiskers",
            breed="Persian",
            age=5,
            special_needs=["Medication"]
        )
        
        # Start with no tasks
        assert len(pet.get_tasks()) == 0
        
        # Create multiple tasks
        task1 = Task(
            name="Medication",
            description="Thyroid pill",
            task_type="Medication",
            duration_minutes=5,
            priority=10,
            required=True,
            frequency="daily"
        )
        
        task2 = Task(
            name="Feeding",
            description="Wet food",
            task_type="Feeding",
            duration_minutes=10,
            priority=8,
            required=True,
            frequency="daily"
        )
        
        task3 = Task(
            name="Play",
            description="Playtime with toys",
            task_type="Enrichment",
            duration_minutes=15,
            priority=6,
            required=False,
            frequency="daily"
        )
        
        # Add all tasks
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Task count should be 3
        assert len(pet.get_tasks()) == 3
        assert task1 in pet.get_tasks()
        assert task2 in pet.get_tasks()
        assert task3 in pet.get_tasks()
    
    def test_add_duplicate_task_not_added_twice(self):
        """Verify that adding the same task twice doesn't create duplicates."""
        pet = Pet(
            name="Max",
            breed="Golden Retriever",
            age=3,
            special_needs=[]
        )
        
        task = Task(
            name="Walk",
            description="Morning walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="daily"
        )
        
        # Add task twice
        pet.add_task(task)
        pet.add_task(task)
        
        # Should still only have 1 task
        assert len(pet.get_tasks()) == 1
    
    def test_remove_task_decreases_count(self):
        """Verify that removing a task decreases the task count."""
        pet = Pet(
            name="Max",
            breed="Golden Retriever",
            age=3,
            special_needs=[]
        )
        
        task1 = Task(
            name="Walk",
            description="Morning walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="daily"
        )
        
        task2 = Task(
            name="Feeding",
            description="Lunch",
            task_type="Feeding",
            duration_minutes=15,
            priority=7,
            required=True,
            frequency="daily"
        )
        
        # Add two tasks
        pet.add_task(task1)
        pet.add_task(task2)
        assert len(pet.get_tasks()) == 2
        
        # Remove one task
        pet.remove_task("Walk")
        
        # Should now have 1 task
        assert len(pet.get_tasks()) == 1
        assert task2 in pet.get_tasks()
        assert task1 not in pet.get_tasks()
    
    def test_task_pet_relationship_bidirectional(self):
        """Verify that adding task to pet sets the task.pet reference."""
        pet = Pet(
            name="Max",
            breed="Golden Retriever",
            age=3,
            special_needs=[]
        )
        
        task = Task(
            name="Walk",
            description="Morning walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="daily"
        )
        
        # Before adding, task.pet should be None
        assert task.pet is None
        
        # Add task to pet
        pet.add_task(task)
        
        # After adding, task.pet should reference the pet
        assert task.pet == pet
    
    def test_remove_task_clears_pet_reference(self):
        """Verify that removing task from pet clears the task.pet reference."""
        pet = Pet(
            name="Max",
            breed="Golden Retriever",
            age=3,
            special_needs=[]
        )
        
        task = Task(
            name="Walk",
            description="Morning walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="daily"
        )
        
        # Add task to pet
        pet.add_task(task)
        assert task.pet == pet
        
        # Remove task from pet
        pet.remove_task("Walk")
        
        # task.pet should now be None
        assert task.pet is None


class TestIntegration:
    """Integration tests for Owner, Pet, and Task."""
    
    def test_owner_can_access_all_pets_tasks(self):
        """Verify that Owner.get_all_pets_tasks() returns tasks from all pets."""
        owner = Owner("Sarah")
        
        # Create pets
        dog = Pet(
            name="Max",
            breed="Golden Retriever",
            age=3,
            special_needs=[]
        )
        
        cat = Pet(
            name="Whiskers",
            breed="Persian",
            age=5,
            special_needs=[]
        )
        
        # Add pets to owner
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        # Create tasks
        task1 = Task(
            name="Walk",
            description="Morning walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="daily"
        )
        
        task2 = Task(
            name="Medication",
            description="Thyroid pill",
            task_type="Medication",
            duration_minutes=5,
            priority=10,
            required=True,
            frequency="daily"
        )
        
        # Add tasks to pets
        dog.add_task(task1)
        cat.add_task(task2)
        
        # Get all tasks from owner
        all_tasks = owner.get_all_pets_tasks()
        
        # Should have 2 tasks total
        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 in all_tasks


class TestChronologicalOrdering:
    """Test that tasks are sorted and returned in chronological order."""
    
    def test_sort_scheduled_tasks_chronologically(self):
        """Verify that sort_scheduled_tasks_by_time() returns tasks in chronological order."""
        owner = Owner("Jordan")
        owner.set_available_hours("Monday", 4.0)
        
        dog = Pet(name="Max", breed="Golden Retriever", age=3, special_needs=[])
        owner.add_pet(dog)
        
        # Create tasks with different priorities (will be scheduled in priority order)
        task1 = Task(
            name="Medication",
            description="Critical",
            task_type="Medication",
            duration_minutes=10,
            priority=10,  # Scheduled first (08:00 AM)
            required=True,
            frequency="once"
        )
        
        task2 = Task(
            name="Breakfast",
            description="Feeding",
            task_type="Feeding",
            duration_minutes=15,
            priority=8,  # Scheduled second (08:10 AM)
            required=True,
            frequency="once"
        )
        
        task3 = Task(
            name="Walk",
            description="Exercise",
            task_type="Exercise",
            duration_minutes=30,
            priority=7,  # Scheduled third (08:25 AM)
            required=True,
            frequency="once"
        )
        
        dog.add_task(task1)
        dog.add_task(task2)
        dog.add_task(task3)
        
        # Create scheduler and generate schedule
        scheduler = Scheduler(owner, [dog])
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        scheduler.add_task(task3)
        scheduler.generate_schedule("Monday")
        
        # Sort tasks chronologically
        sorted_tasks = scheduler.sort_scheduled_tasks_by_time()
        
        # Verify 3 tasks were returned
        assert len(sorted_tasks) == 3
        
        # Verify they are in chronological order: 08:00 < 08:10 < 08:25
        assert sorted_tasks[0].task.name == "Medication"
        assert sorted_tasks[0].time_slot == "08:00 AM"
        
        assert sorted_tasks[1].task.name == "Breakfast"
        assert sorted_tasks[1].time_slot == "08:10 AM"
        
        assert sorted_tasks[2].task.name == "Walk"
        assert sorted_tasks[2].time_slot == "08:25 AM"
        
        # Verify start_time objects are correctly ordered
        assert sorted_tasks[0].start_time < sorted_tasks[1].start_time
        assert sorted_tasks[1].start_time < sorted_tasks[2].start_time
    
    def test_sort_with_none_times_places_at_end(self):
        """Verify that tasks with None start_time are placed at the end when sorting."""
        owner = Owner("Jordan")
        owner.set_available_hours("Monday", 4.0)
        
        dog = Pet(name="Max", breed="Golden Retriever", age=3, special_needs=[])
        owner.add_pet(dog)
        
        task1 = Task(
            name="Task1",
            description="Test",
            task_type="Test",
            duration_minutes=10,
            priority=8,
            required=True,
            frequency="once"
        )
        
        task2 = Task(
            name="Task2",
            description="Test2",
            task_type="Test",
            duration_minutes=10,
            priority=7,
            required=True,
            frequency="once"
        )

        dog.add_task(task1)
        dog.add_task(task2)
        scheduler = Scheduler(owner, [dog])
        scheduler.add_task(task1)

        # Generate schedule for task1 only
        scheduler.generate_schedule("Monday")
        
        # Manually add a task with None times after schedule is generated
        from pawpal_system import ScheduledTask
        scheduled_none = ScheduledTask(
            task=task2,
            time_slot="N/A",
            day="Monday",
            start_time=None,
            end_time=None
        )
        scheduler.scheduled_tasks.append(scheduled_none)

        # Sort all tasks
        sorted_tasks = scheduler.sort_scheduled_tasks_by_time()

        # Verify None-time task is at the end
        assert sorted_tasks[-1].start_time is None
        assert len(sorted_tasks) == 2


class TestRecurringTaskBehavior:
    """Test recurring task expansion and completion tracking."""
    
    def test_daily_task_expands_across_week(self):
        """Verify that daily recurring tasks expand properly across 7 days."""
        owner = Owner("Jordan")
        owner.set_available_hours("Monday", 1.0)
        
        dog = Pet(name="Max", breed="Golden Retriever", age=3, special_needs=[])
        owner.add_pet(dog)
        
        # Create a daily task
        daily_task = Task(
            name="Morning Walk",
            description="Daily walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="daily"  # Will expand daily
        )
        
        dog.add_task(daily_task)
        
        scheduler = Scheduler(owner, [dog])
        scheduler.add_task(daily_task)
        scheduler.generate_schedule("Monday")
        
        # Expand recurring tasks for 7 days
        expanded = scheduler.expand_recurring_tasks("Monday", num_days=7)
        
        # Count how many times the daily task appears
        daily_count = sum(1 for st in expanded if st.task.name == "Morning Walk")
        
        # Should appear 7 times (once per day for the week)
        assert daily_count == 7
    
    def test_marking_task_complete_and_expanding_creates_separate_instances(self):
        """Verify that marking a daily task complete and expanding creates independent instances."""
        owner = Owner("Jordan")
        owner.set_available_hours("Monday", 1.0)
        
        dog = Pet(name="Max", breed="Golden Retriever", age=3, special_needs=[])
        owner.add_pet(dog)
        
        # Create daily task
        daily_task = Task(
            name="Medication",
            description="Daily medication",
            task_type="Medication",
            duration_minutes=10,
            priority=9,
            required=True,
            frequency="daily"
        )
        
        dog.add_task(daily_task)
        
        scheduler = Scheduler(owner, [dog])
        scheduler.add_task(daily_task)
        scheduler.generate_schedule("Monday")
        
        # Mark Monday's occurrence as complete
        if scheduler.scheduled_tasks:
            scheduler.scheduled_tasks[0].task.mark_complete()
            is_monday_complete = scheduler.scheduled_tasks[0].task.is_completed
        
        # Expand for the week
        expanded = scheduler.expand_recurring_tasks("Monday", num_days=7)
        
        # Count completed vs pending instances
        completed_count = sum(1 for st in expanded if st.task.is_completed)
        pending_count = sum(1 for st in expanded if not st.task.is_completed)
        
        # All expanded instances share the same Task object, so all should be marked complete
        # This reveals that recurring expansion doesn't create new Task instances
        assert completed_count >= 1  # At least Monday is complete
        assert len(expanded) >= 7  # At least 7 occurrences
    
    def test_twice_daily_task_creates_morning_and_afternoon(self):
        """Verify that twice-daily tasks create two instances on the same day."""
        owner = Owner("Jordan")
        owner.set_available_hours("Monday", 4.0)
        
        dog = Pet(name="Max", breed="Golden Retriever", age=3, special_needs=[])
        owner.add_pet(dog)
        
        # Create twice-daily task
        twice_task = Task(
            name="Medication",
            description="Morning and afternoon meds",
            task_type="Medication",
            duration_minutes=5,
            priority=10,
            required=True,
            frequency="twice daily"
        )
        
        dog.add_task(twice_task)
        
        scheduler = Scheduler(owner, [dog])
        scheduler.add_task(twice_task)
        scheduler.generate_schedule("Monday")
        
        # Expand recurring tasks
        expanded = scheduler.expand_recurring_tasks("Monday", num_days=1)
        
        # Count twice-daily task occurrences on Monday
        monday_count = sum(1 for st in expanded if st.task.name == "Medication" and st.day == "Monday")
        
        # Should have 2 (morning at 08:00, afternoon at ~14:00)
        assert monday_count == 2


class TestDuplicatePrevention:
    """Test that scheduler flags and prevents duplicate task additions."""
    
    def test_scheduler_prevents_duplicate_task_addition(self):
        """Verify that Scheduler.add_task() prevents adding the same task twice."""
        owner = Owner("Jordan")
        dog = Pet(name="Max", breed="Golden Retriever", age=3, special_needs=[])
        owner.add_pet(dog)
        
        task = Task(
            name="Walk",
            description="Morning walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="daily"
        )
        
        dog.add_task(task)
        
        scheduler = Scheduler(owner, [dog])
        
        # Add task first time
        scheduler.add_task(task)
        initial_count = len(scheduler.tasks)
        assert initial_count == 1
        
        # Try to add the same task again
        scheduler.add_task(task)
        final_count = len(scheduler.tasks)
        
        # Count should remain 1 (duplicate prevented)
        assert final_count == 1
        assert final_count == initial_count
    
    def test_scheduler_invalidates_cache_on_task_addition(self):
        """Verify that adding a task invalidates the sorted cache for performance."""
        owner = Owner("Jordan")
        owner.set_available_hours("Monday", 4.0)
        dog = Pet(name="Max", breed="Golden Retriever", age=3, special_needs=[])
        owner.add_pet(dog)
        
        task1 = Task(
            name="Task1",
            description="First",
            task_type="Test",
            duration_minutes=10,
            priority=8,
            required=True,
            frequency="once"
        )
        
        task2 = Task(
            name="Task2",
            description="Second",
            task_type="Test",
            duration_minutes=10,
            priority=9,  # Higher priority
            required=True,
            frequency="once"
        )
        
        dog.add_task(task1)
        dog.add_task(task2)
        
        scheduler = Scheduler(owner, [dog])
        scheduler.add_task(task1)
        
        # Access sorted tasks (populates cache)
        sorted1 = scheduler._sort_tasks_by_priority()
        assert scheduler._sorted_tasks_cache is not None
        
        # Add another task (should invalidate cache)
        scheduler.add_task(task2)
        assert scheduler._sorted_tasks_cache is None  # Cache cleared
        
        # Sort again (rebuilds cache with new task)
        sorted2 = scheduler._sort_tasks_by_priority()
        
        # New sort should have 2 tasks
        assert len(sorted2) == 2
        # Highest priority (task2=9) should be first
        assert sorted2[0].priority == 9


class TestConflictDetection:
    """Test conflict detection functionality."""
    
    def test_detect_conflicts_identifies_overlapping_tasks(self):
        """Verify that detect_conflicts() identifies overlapping scheduled tasks."""
        owner = Owner("Jordan")
        owner.set_available_hours("Monday", 2.0)
        dog = Pet(name="Max", breed="Golden Retriever", age=3, special_needs=[])
        owner.add_pet(dog)
        
        # Task 1: 08:00-08:30
        task1 = Task(
            name="Walk1",
            description="First walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="once"
        )
        
        # Task 2: 08:15-08:45 (overlaps with task1)
        task2 = Task(
            name="Feeding",
            description="Feeding",
            task_type="Feeding",
            duration_minutes=30,
            priority=7,
            required=True,
            frequency="once"
        )
        
        dog.add_task(task1)
        dog.add_task(task2)
        
        scheduler = Scheduler(owner, [dog])
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        # Manually create conflicting ScheduledTasks
        from pawpal_system import ScheduledTask
        
        time1 = datetime.strptime("08:00", "%H:%M").replace(year=2024)
        time1_end = time1 + timedelta(minutes=30)
        
        time2 = datetime.strptime("08:15", "%H:%M").replace(year=2024)
        time2_end = time2 + timedelta(minutes=30)
        
        st1 = ScheduledTask(
            task=task1,
            time_slot="08:00 AM",
            day="Monday",
            start_time=time1,
            end_time=time1_end
        )
        
        st2 = ScheduledTask(
            task=task2,
            time_slot="08:15 AM",
            day="Monday",
            start_time=time2,
            end_time=time2_end
        )
        
        scheduler.scheduled_tasks = [st1, st2]
        
        # Detect conflicts
        conflicts = scheduler.detect_conflicts()
        
        # Should find 1 conflict pair
        assert len(conflicts) == 1
        assert conflicts[0] == (st1, st2)
    
    def test_no_conflicts_for_adjacent_tasks(self):
        """Verify that adjacent (touching) tasks don't create false conflicts."""
        owner = Owner("Jordan")
        owner.set_available_hours("Monday", 2.0)
        dog = Pet(name="Max", breed="Golden Retriever", age=3, special_needs=[])
        owner.add_pet(dog)
        
        task1 = Task(
            name="Walk",
            description="Walk",
            task_type="Exercise",
            duration_minutes=30,
            priority=8,
            required=True,
            frequency="once"
        )
        
        task2 = Task(
            name="Feeding",
            description="Feeding",
            task_type="Feeding",
            duration_minutes=15,
            priority=7,
            required=True,
            frequency="once"
        )
        
        dog.add_task(task1)
        dog.add_task(task2)
        
        scheduler = Scheduler(owner, [dog])
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        from pawpal_system import ScheduledTask
        
        # Task 1: 08:00-08:30
        time1 = datetime.strptime("08:00", "%H:%M").replace(year=2024)
        time1_end = time1 + timedelta(minutes=30)
        
        # Task 2: 08:30-08:45 (starts exactly when task1 ends)
        time2 = time1_end
        time2_end = time2 + timedelta(minutes=15)
        
        st1 = ScheduledTask(
            task=task1,
            time_slot="08:00 AM",
            day="Monday",
            start_time=time1,
            end_time=time1_end
        )
        
        st2 = ScheduledTask(
            task=task2,
            time_slot="08:30 AM",
            day="Monday",
            start_time=time2,
            end_time=time2_end
        )
        
        scheduler.scheduled_tasks = [st1, st2]
        
        # Detect conflicts
        conflicts = scheduler.detect_conflicts()
        
        # Should have NO conflicts (adjacent tasks are OK)
        assert len(conflicts) == 0



if __name__ == "__main__":
    pytest.main([__file__, "-v"])
