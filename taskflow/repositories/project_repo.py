"""Репозиторий для работы с проектами."""

from typing import Optional
from taskflow.database import Database
from taskflow.models import Project

class ProjectRepository:
    # CRUD операции для проектов.

    def __init__(self, db: Database):
        self.db = db

    def add(self, project: Project) -> int:
        # Добавляет проект в БД.
        try:
            cursor = self.db.execute('INSERT INTO projects (name, description) VALUES (?, ?)',
                                     (project.name, project.description))
            self.db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)

    def get_by_id(self, project_id: int) -> Optional[Project]:
        #Находит проект по ID.
        try:
            cursor = self.db.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return self._row_to_project(row)
        except Exception as e:
            print(e)

    def get_by_name(self, name: str) -> Optional[Project]:
        #Находит проект по имени.
        try:
            cursor = self.db.execute('SELECT * FROM projects WHERE name = ?', (name,))
            row = cursor.fetchone()
            if row is None:
                return None
            return self._row_to_project(row)
        except Exception as e:
            print(e)

    def get_all(self) -> list[Project]:
        #Получает все проекты.
        try:
            cursor = self.db.execute('SELECT * FROM projects ORDER BY name ASC')
            rows = cursor.fetchall()
            if rows is None:
                return None
            return [self._row_to_project(row) for row in rows]
        except Exception as e:
            print(e)

    def update(self, project: Project) -> bool:
        # Обновляет проект.
        try:
            cursor = self.db.execute('UPDATE projects SET name = ?, description = ? WHERE id = ?',
                                     (project.name, project.description, project.id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(e)

    def delete(self, project_id: int) -> bool:
        # Удаляет проект по ID.
        try:
            cursor = self.db.execute('DELETE FROM projects WHERE id = ?',
                                     (project_id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(e)

    def _row_to_project(self, row) -> Project:
        # Преобразует строку БД в объект Project.
        return Project(id=row["id"],
                       name=row["name"],
                       description=row["description"],
                       created_at=row["created_at"],)