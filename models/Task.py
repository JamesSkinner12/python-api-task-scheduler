from models.Status import Status
from models.TaskLogItem import TaskLogItem
from datetime import datetime,timezone,timedelta
from typing import List

class Task:
    log_handler: List[TaskLogItem] = []

    def __init__(self, task_id: str, name: str, priority: int, status: Status):
        self.task_id = task_id
        self.name = name
        self.priority = priority
        self.status = status
        self.created_at = datetime.now(timezone.utc)
        self.log_handler.append(TaskLogItem("Task Created", f"Task {self.task_id} created"))

    def changeStatus(self, status: Status):
        self.log_handler.append(TaskLogItem("Status Changed", f"Status changed from {self.status} to {status}"))
        self.status = status

    def __json__(self):
        return {
            'TaskID': self.task_id,
            'Name': self.name,
            'Priority': self.priority,
            'Status': self.status.name,
            'Created': self.created_at.ctime()
        }
    def changeCreatedAt(self, created_at: datetime):
        self.created_at = created_at

    def pendingTime(self):
        if self.status == Status.PENDING:
            currentTime = datetime.now(timezone.utc)
            elapsed = currentTime - self.created_at
            return elapsed
        else:
            raise ValueError("Status is no longer Pending")

    def logDump(self):
        return self.log_handler

    def runTask(self, failure: RuntimeError = None):
        self.changeStatus(Status.RUNNING)
        try:
            print(f"Running Task: {self.task_id}")
            if failure is not None:
                raise failure
        except RuntimeError as e:
            self.log_handler.append(TaskLogItem("Task Execution Failuer", f"The task: {self.task_id} failed while executing - {failure.__str__}"))
        self.changeStatus(Status.DONE)
