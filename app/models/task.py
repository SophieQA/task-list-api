from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from datetime import datetime
from typing import Optional
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"), nullable=True)
    
    goal: Mapped[Optional["Goal"]] = relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id
        return task_dict

    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title=task_dict["title"],
            description=task_dict["description"]
        )
