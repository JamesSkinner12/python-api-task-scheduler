# python-api-task-scheduler
A simple task scheduling API made with Python's FastAPI

# Requirements
- Python 3
- venv
- FastAPI

Set up venv and run source ./venv/bin/activate

## Running It
```python
## Load virtual environment (venv)
source ./venv/bin/activate

## Run the main.py script
fastapi dev main.py
```

## Available Endpoints
| Endpoint | Method | Description |
| :---         | :---:    | ---:          |
| `/tasks`         | `GET`     | Lists all tasks in order of status, priority, and creation time          |
| `/tasks/next` | `GET` | Returns the next task in the queue |
| `/tasks/{task_id}`         | `GET`     | Returns details for a specific task based on the TaskID          |
| `/tasks/{task_id}/logs` | `GET` | Returns the task specified, and includes all log information |
| `/tasks/{task_id}/run` | `GET` | Runs the provided task and returns the same information as the logs endpoint |
| `/generate-tasks/{count}`         | `GET`     | This will generate the provided number of tasks using random data          |