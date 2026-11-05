from fastapi import FastAPI
from models.Scheduler import Scheduler
from models.Task import Task
from models.Status import Status
from datetime import datetime, timezone
import time
import random
import string

# Helper function to generate random strings when generating tasks
def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Helper function to generate a random time before the current time
def generate_random_recent_time():
    random_offset_seconds = time.time() - random.choice(range(7200))
    return datetime.fromtimestamp(random_offset_seconds, timezone.utc)

# Helper function to generate a task
def task_generator():
    task = Task(generate_random_string(10), generate_random_string(30), random.choice([1,2,3,4,5]), random.choice([Status.PENDING, Status.RUNNING, Status.DONE]))
    task.changeCreatedAt(generate_random_recent_time())
    return task

# Helper function to fetch a task or return None
def find_task(task_id: str):
    return next((t for t in scheduler.tasks if t.task_id == task_id), None)

# Start up application
app = FastAPI()

# Add random tasks if none exist
scheduler = Scheduler()
for i in range(50):
    scheduler.addTask(task_generator())

# Helper endpoint to generate tasks
@app.get("/generate-tasks/{count}")
def generate_tasks(count:int):
    for i in range(count):
        scheduler.addTask(task_generator())
    return scheduler.tasks

# List tasks
@app.get("/tasks")
def read_tasks():
    response = []
    for task in scheduler.tasksByPriority():
        response.append(task.__json__())
    return response

# Get the next task in the queue
@app.get("/tasks/next")
def get_next_in_queue():
    return scheduler.nextInQueue().__json__()

# Show individual task by TaskID
@app.get("/tasks/{task_id}")
def read_task(task_id: str):
    task = find_task(task_id)
    return [task.__json__()] if task is not None else []

# Show detailed task logs
@app.get("/tasks/{task_id}/logs")
def read_task_logs(task_id: str):
    task = find_task(task_id)
    return [task.__json__(True)] if task is not None else []

# Run the selected task 
@app.get("/tasks/{task_id}/run")
def run_task(task_id: str):
    task = find_task(task_id)
    if task.status == 1:
        # This randomly makes the task throw an error to make sure they are handled and logged
        task.runTask(RuntimeError("Generic Error Message") if (random.choice([True,False])) else None)
    return [task.__json__(True)] if task is not None else []
