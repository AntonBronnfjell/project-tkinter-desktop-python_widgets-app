from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any
import uuid


@dataclass
class Task:
    """Domain model representing a to-do task."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    is_completed: bool = False
    created_at_iso: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "is_completed": self.is_completed,
            "created_at_iso": self.created_at_iso,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        return Task(
            id=data.get("id") or str(uuid.uuid4()),
            title=str(data.get("title") or "").strip(),
            is_completed=bool(data.get("is_completed")),
            created_at_iso=str(data.get("created_at_iso") or datetime.utcnow().isoformat()),
        )


