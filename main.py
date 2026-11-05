from fastapi import FastAPI
from models.Scheduler import Scheduler
from models.Task import Task
from models.Status import Status
from datetime import datetime, timezone
import time
import random
import string

def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def generate_random_recent_time():
    random_offset_seconds = time.time() - random.choice(range(7200))
    return datetime.fromtimestamp(random_offset_seconds, timezone.utc)

def task_generator():
    task = Task(generate_random_string(10), generate_random_string(30), random.choice([1,2,3,4,5]), random.choice([Status.PENDING, Status.RUNNING, Status.DONE]))
    task.changeCreatedAt(generate_random_recent_time())
    return task

app = FastAPI()
scheduler = Scheduler()

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

# Show individual task by TaskID
@app.get("/tasks/{task_id}")
def read_task(task_id: str):
    task = next((t for t in scheduler.tasks if t.task_id == task_id), None)
    return [task.__json__()] if task is not None else []
