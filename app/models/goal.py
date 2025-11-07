from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING
from ..db import db

if TYPE_CHECKING:
    from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="goal")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }

    @classmethod
    def from_dict(cls, goal_dict):
        return cls(
            title=goal_dict["title"]
        )
