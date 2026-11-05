from models.Task import Task
from models.TaskLogItem import TaskLogItem
from models.Status import Status

class Scheduler:
    def __init__(self):
        self.tasks = []

    # Adds a task to the scheduler
    def addTask(self, task: Task):
        self.tasks.append(task)

    # Returns all of the tasks with the provided Status
    def tasksWithStatus(self, status: Status):
        return [t for t in self.tasks if t.status == status]

    # Helper function to get Pending tasks
    def pendingTasks(self):
        return self.tasksWithStatus(Status.PENDING)

    # Sorts all of the tasks by three dimensions, first status - then priority - then creation time
    def tasksByPriority(self):
        self.tasks.sort(key=lambda task: (task.status, task.priority, task.created_at))
        return self.tasks

    # Returns the next task in the queue
    def nextInQueue(self):
        return self.tasksByPriority()[0]