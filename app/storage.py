from __future__ import annotations

import json
import os
import tempfile
from typing import List

from .models import Task


class JsonTaskRepository:
    """JSON-backed storage for tasks with atomic writes."""

    def __init__(self, file_path: str) -> None:
        self.file_path = os.path.abspath(file_path)
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.file_path):
            self._write_json([])

    def load_tasks(self) -> List[Task]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Task.from_dict(item) for item in data]
        except json.JSONDecodeError:
            return []
        except FileNotFoundError:
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        serialized = [task.to_dict() for task in tasks]
        self._write_json(serialized)

    def _write_json(self, data) -> None:
        directory = os.path.dirname(self.file_path)
        with tempfile.NamedTemporaryFile("w", delete=False, dir=directory, encoding="utf-8") as temp_file:
            json.dump(data, temp_file, ensure_ascii=False, indent=2)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            temp_path = temp_file.name
        os.replace(temp_path, self.file_path)


