# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design. There will be four classes. The classes will be Owner, Pet, Task, and Scheduler. The Owner class will include attributes name: str, available_schedule: dict[str,float], preferences: list[str], and pets: list[Pet]. The Pet class will have the attriibutes name: str, breed:str, age: int, and special_needs: list[str], owner: Owner. The Task class will have attributes name: str, task_type: str, duration_minutes: int, priority: int, required: bool. The Scheduler class will have attributes owner:Owner, pet: Pet, tasks: list[Task].
- What classes did you include, and what responsibilities did you assign to each?The Owner class will be in charge of adding, removing, printing pets list owned by that owner, assigning and getting the available schedule, setting preferences. Task will be in charge of getting details of each task and checking if it is high priority. The Scheduler will be assigned the responsibility of adding tasks, removing tasks, generating schedule, based on priority and available schedule.

**b. Design changes**

- Did your design change during implementation? 
- If yes, describe at least one change and why you made it.
There are a few logic changes made to the classes. For example, the Scheduler class now takes in a list of pets, since an owner might have more than one pet and would need to schedule tasks for those pets.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
