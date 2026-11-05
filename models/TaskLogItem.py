from datetime import datetime, timezone

class TaskLogItem:

    def __init__(self, label: str, details: str):
        self.label = label
        self.details = details
        self.created_at = datetime.now(timezone.utc)    

    def __str__(self):
        return f"{self.label} - {self.details} | {self.created_at.isoformat()}"

    def __json__(self):
        return {
            'Label': self.label,
            'Details': self.details,
            'Created': self.created_at.isoformat()
        }