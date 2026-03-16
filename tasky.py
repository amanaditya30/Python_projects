import heapq
class Task:
    
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name

    def __lt__(self, other):
        return self.priority < other.priority
      class TaskScheduler:

    def __init__(self):
        self.heap = []

    def add_task(self, priority, name):
        task = Task(priority, name)
        heapq.heappush(self.heap, task)
        print(f"Task '{name}' added with priority {priority}")

    def execute_task(self):
        if not self.heap:
            print("No tasks available")
            return
        
        task = heapq.heappop(self.heap)
        print(f"Executing task: {task.name}")
      scheduler = TaskScheduler()

scheduler.add_task(2, "Complete Assignment")
scheduler.add_task(1, "Study Machine Learning")
scheduler.add_task(5, "Play Game")

scheduler.execute_task()
scheduler.execute_task()
scheduler.execute_task()
