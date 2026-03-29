import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
