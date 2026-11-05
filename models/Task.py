from models.Status import Status
from models.TaskLogItem import TaskLogItem
from datetime import datetime,timezone

class Task:
    def __init__(self, task_id: str, name: str, priority: int, status: Status):
        self.task_id = task_id
        self.name = name
        self.priority = priority
        self.status = status
        self.created_at = datetime.now(timezone.utc)
        self.log_handler = []
        self.log_handler.append(TaskLogItem(
            "Task Created", f"Task {self.task_id} created"
        ))

    # Changes the status of the task and logs the event
    def changeStatus(self, status: Status):
        self.log_handler.append(TaskLogItem("Status Changed", f"Status changed from {self.status.name} to {status.name}"))
        self.status = status

    # Returns a formatted version of the log_handler
    def __log_handler(self):
        return [log.__json__() for log in self.log_handler]

    # Returns a formatted version of the task (optionally include logs)
    def __json__(self, include_logs: bool = False):
        return {
            'TaskID': self.task_id,
            'Name': self.name,
            'Priority': self.priority,
            'Status': self.status.name,
            'Created': self.created_at.isoformat(),  # Modern, standard datetime format
            'Logs': self.__log_handler() if include_logs else []
        }

    # Helper function to modify the created_at timestamp
    def changeCreatedAt(self, created_at: datetime):
        self.created_at = created_at

    # Returns the amount of time the task has been pending
    def pendingTime(self):
        if self.status == Status.PENDING:
            currentTime = datetime.now(timezone.utc)
            elapsed = currentTime - self.created_at
            return elapsed
        else:
            raise ValueError("Status is no longer Pending")

    # Simply returns the log handler
    def logDump(self):
        return self.log_handler

    # Runs the task - Optionally accepts a RuntimeError argument to test log handling
    def runTask(self, failure: RuntimeError = None):
        self.changeStatus(Status.RUNNING)
        try:
            if failure is not None:
                raise failure
            # Placeholder for where actual running code would go
        except RuntimeError as e:
            self.log_handler.append(TaskLogItem("Task Execution Failure", f"The task: {self.task_id} failed while executing - {failure.__str__}"))
        self.changeStatus(Status.DONE)