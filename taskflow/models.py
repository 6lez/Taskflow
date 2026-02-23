"""Модели данных приложения."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """Модель задачи."""
    id: Optional[int] = None  # None для новых, число для существующих
    title: str = ""
    description: str = ""
    priority: str = "medium"  # low, medium, high, critical
    status: str = "todo"  # todo, in_progress, done, cancelled
    project_id: Optional[int] = None # Для объединения в проекты
    deadline: Optional[datetime] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Это поле не хранится в БД, заполняется при необходимости
    tags: list = field(default_factory=list)
    project_name: Optional[str] = None

@dataclass
class Project:
    """Модель проекта."""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    created_at: Optional[datetime] = None

@dataclass
class Tag:
    """Модель тега."""
    id: Optional[int] = None
    name: str = ""