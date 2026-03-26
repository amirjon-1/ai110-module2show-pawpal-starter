# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Three core actions:
	1) The user must be able to enter the pets name and other info, and care
	   time availability. 
	2) The user must be able to create tasks with a name, duration (minutes),
  	   and priority level. They can edit and delete these tasks.
	3) Our app must return a task list and constraints, schedules tasks by time
	   and priority. It should also provide explanation for such choices.
 
Classes:
1) Owner - attributes: name, available_minutes
	 - methods: add_pet(), get_pets()

2) Pet - attributes: name, species, age
       - methods: add_task(), get_tasks()

3) Task - attributes: name, duration, priority, completed
	- methods: mark_complete()

4) Schedule - attributes: pet, available_minutes
	    - methods: make_plan(), explain_plan()


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I noticed that anything can be passed into priority, so I changed it from a string
to a Enum with values High, Medium, and Low to prevent random inputs. Minor change, but
important. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers the daily time budget and task priority. Priority mattered most 
because skipping medication is worse than skipping fetch training.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Since tasks have no start times, conflict detection flags pairs that exceed the daily budget 
together, not true time overlaps. For a simple daily planner, that tradeoff is good enough.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used a mix of Claude Code and Copilot for generating skeletons, implementing logic, and wiring the UI. 
Specific prompts worked way better than vague ones.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

Claude suggested itertools.combinations for conflict detection. I didn't just copy it, I read through it and 
made sure I understood the logic before keeping it.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested that mark_complete() sets is_complete to True, adding a task increases the pet's task count, 
sorting returns tasks shortest first, and a daily task creates a new instance due tomorrow.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Pretty confident in the core logic. I'd add tests for a pet with no tasks, a budget of zero, 
and tasks that all have the same priority.


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The scheduling logic came out clean. The greedy priority sort with a readable explain_plan() 
output is something I'm happy with.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd add start times to tasks so conflict detection could check real overlaps instead of just budget totals.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI is great at generating boilerplate but you still have to understand what it gives you. 
The design decisions were all mine, Claude just helped execute them faster.


