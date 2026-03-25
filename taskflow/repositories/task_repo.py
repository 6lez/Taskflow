"""Репозиторий для работы с задачами."""

from typing import Optional
from taskflow.database import Database
from taskflow.models import Task


class TaskRepository:
    # CRUD операции для задач.
    def __init__(self, db: Database):
        self.db = db

    def add(self, task: Task) -> int:
        # Добавляет задачу в БД.
        try:
            cursor = self.db.execute('INSERT INTO tasks (title, description, priority, '
                                      'status, project_id, deadline)'
                                      'VALUES (?, ?, ?, ?, ?, ?)',
                               (task.title, task.description, task.priority,
                                task.status, task.project_id, task.deadline))
            self.db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)

    def get_by_id(self, task_id: int) -> Optional[Task]:
        # Получает задачу по ID.
        try:
            cursor = self.db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return self._row_to_task(row)
        except Exception as e:
            print(e)

    def get_all(self) -> list[Task]:
        # Получает все задачи.
        try:
            cursor = self.db.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            rows = cursor.fetchall()
            if rows is None:
                return None
            return [self._row_to_task(row) for row in rows]
        except Exception as e:
            print(e)

    def update(self, task: Task) -> bool:
        # Обновляет задачу в БД.
        try:
            cursor = self.db.execute('UPDATE tasks SET title = ?, description = ?, priority = ?, '
                                     'status = ?, project_id = ?, deadline = ?, '
                                     'completed_at = ? WHERE id = ?', (task.title, task.description,
                                                                       task.priority, task.status,
                                                                       task.project_id, task.deadline,
                                                                       task.completed_at, task.id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(e)

    def delete(self, task_id: int) -> bool:
        # Удаляет задачу по ID.
        try:
            cursor = self.db.execute('DELETE FROM tasks WHERE id = ?',
                                     (task_id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(e)

    def _row_to_task(self, row) -> Task:
        # Преобразует строку из БД в объект Task.
        return Task(id=row["id"], title=row["title"],
                                    description=row["description"],
                                    priority=row["priority"],
                                    status=row["status"],
                                    project_id=row["project_id"],
                                    deadline=row["deadline"],
                                    created_at=row["created_at"],
                                    completed_at=row["completed_at"])