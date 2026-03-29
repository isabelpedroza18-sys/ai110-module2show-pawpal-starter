# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design. There will be four classes. The classes will be Owner, Pet, Task, and Scheduler. The Owner class will include attributes name: str, available_schedule: dict[str,float], preferences: list[str], and pets: list[Pet]. The Pet class will have the attriibutes name: str, breed:str, age: int, and special_needs: list[str], owner: Owner. The Task class will have attributes name: str, task_type: str, duration_minutes: int, priority: int, required: bool. The Scheduler class will have attributes owner:Owner, pet: Pet, tasks: list[Task].
- What classes did you include, and what responsibilities did you assign to each?The Owner class will be in charge of adding, removing, printing pets list owned by that owner, assigning and getting the available schedule, setting preferences. Task will be in charge of getting details of each task and checking if it is high priority. The Scheduler will be assigned the responsibility of adding tasks, removing tasks, generating schedule, based on priority and available schedule.

**b. Design changes**

- Did your design change during implementation? 
- If yes, describe at least one change and why you made it.
There are a few logic changes made to the classes. For example, the Scheduler class now takes in a list of pets, instead of just one Pet object, because an owner might have more than one pet and would need to schedule tasks for all of their pets.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)? The Scheduler class considers any special health and safety needs, priority, and time feasability.
- How did you decide which constraints mattered most? I decided pet health and safety is the most important to consider because these needs can be life or death such as medication needed. With PawPal+ we want to keep pets alive and healthy.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario? The Scheduler prioritizes simplicity, predictability, and domain-appropriateness over theoretical optimization. For a pet care app, having a clear, understandable schedule that prioritizes critical tasks (medication, feeding) is more valuable than a theoretically optimal but confusing schedule. This is a sound trade-off for this use case.For example, the schedule always starts at 8 AM, so is best for consistent pet routines rather thatn flexible workers.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)? I used AI to help me with the design brainstorming for the original classes and what attributes would be best to include such as to create a UML Diagram. Then I would write code and have AI check if the logic in my code was still cohesive and functional with all of the classes combined. I also asked for guidance in writing the logic for more complex methods in the Scheduler class.
- What kinds of prompts or questions were most helpful? I had to be very specific with my prompts and it was very helpful to include which files I was referring to or which files to gather information from to provide the best ideas. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested? It was during the design phase that I rejected its first few suggestions, since I would forget to specify exactly what I wanted or I would get more ideas that would require a different suggestion from AI. For Example, it suggested I had an attribute named type for the Pet class and I wanted it to be named breed instead. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test? I tested to verify that the method mark_complete from the Task class would actually change the status of the task. In addition, I tested to verify that adding a Task to the Pet class would add the number of tasks a Pet had. 
- Why were these tests important? These tests are important to the logic of the system because every class is tied together and these small functions can make a difference in the reliability of the results/output.

**b. Confidence**

- How confident are you that your scheduler works correctly? I am fairly confident.
- What edge cases would you test next if you had more time? If I had more time I would add more tasks, so that the available time is less than the task time needed, therefore I would like to see only highest priority tasks be completed before the time needed ran out. In conclusion, I would have liked to test my code more.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with? I am most satisfied with how all the classes were able to work together to complete the requirements specified in the README file.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign? I would like to test the code more to verify it can cover unexpected input.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project? I learned that it takes a lot of time and supervision to make sure AI is implementing correct suggestions. I learned that the draft will likely be changed over and over again throughout the coding process, as relevant questions or problems arise.
