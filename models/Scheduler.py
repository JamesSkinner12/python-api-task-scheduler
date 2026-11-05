from models.Task import Task
from models.TaskLogItem import TaskLogItem
from typing import List
from models.Status import Status

class Scheduler:
    tasks: List[Task] = []
    def __init__(self):
        pass

    def addTask(self, task: Task):
        self.tasks.append(task)

    def tasksWithStatus(self, status: Status):
        return [t for t in self.tasks if t.status == status]

    def pendingTasks(self):
        return self.tasksWithStatus(Status.PENDING)

    def tasksByPriority(self):
        self.tasks.sort(key=lambda task: (task.status, task.priority, task.created_at))
        return self.tasks

    def nextInQueue(self):
        return self.tasksByPriority()[0]

    def dumpTasks(self):
        return self.tasks

    def viewQueue(self):
        return self.pendingTasks()