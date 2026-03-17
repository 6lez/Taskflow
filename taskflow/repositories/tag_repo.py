"""Репозиторий для работы с тегами."""
import sqlite3
from typing import Optional
from taskflow.database import Database
from taskflow.models import Tag


class TagRepository:
    # CRUD операции для тегов.

    def __init__(self, db: Database):
        self.db = db

    def add(self, tag: Tag) -> int:
        # Создаёт тег.
        try:
            cursor = self.db.execute('INSERT INTO tags (name) VALUES (?)',
                               (tag.name,))
            self.db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)

    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        # Находит тег по ID.
        try:
            cursor = self.db.execute('SELECT * FROM tags WHERE id = ?',
                                     (tag_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return self._row_to_tag(row)
        except Exception as e:
            print(e)

    def get_by_name(self, name: str) -> Optional[Tag]:
        # Находит тег по имени.
        try:
            cursor = self.db.execute('SELECT * FROM tags WHERE name = ?',
                                     (name,))
            row = cursor.fetchone()
            if row is None:
                return None
            return self._row_to_tag(row)
        except Exception as e:
            print(e)

    def get_all(self) -> list[Tag]:
        # Получает все теги.
        try:
            cursor = self.db.execute('SELECT * FROM tags ORDER BY name ASC')
            rows = cursor.fetchall()
            if rows is None:
                return None
            return [self._row_to_tag(row) for row in rows]
        except Exception as e:
            print(e)

    def delete(self, tag_id: int) -> bool:
        # Удаляет тег.
        try:
            cursor = self.db.execute('DELETE FROM tags WHERE id = ?',
                                     (tag_id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(e)

    def add_tag_to_task(self, task_id: int, tag_id: int) -> bool:
        # Привязывает тег к задаче.
        try:
            cursor = self.db.execute('INSERT INTO task_tags (task_id, tag_id) VALUES (?, ?)',
                                     (task_id, tag_id))
            self.db.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            if "PRIMARY KEY" in str(e):
                print("Запись с таким ID уже существует")
            elif "UNIQUE constraint" in str(e):
                print("Нарушение уникальности")
        except Exception as e:
            print(e)

    def remove_tag_from_task(self, task_id: int, tag_id: int) -> bool:
        # Отвязывает тег от задачи.
        try:
            cursor = self.db.execute('DELETE FROM task_tags WHERE task_id = ? AND tag_id = ?',
                                     (task_id, tag_id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(e)

    def get_tags_for_task(self, task_id: int) -> list[Tag]:
        # Получает все теги конкретной задачи.
        try:
            cursor = self.db.execute('SELECT tags.id, tags.name FROM tags '
                                     'JOIN task_tags ON tags.id = task_tags.tag_id '
                                     'WHERE task_tags.task_id = ?', (task_id,))
            rows = cursor.fetchall()
            return [self._row_to_tag(row) for row in rows]
        except Exception as e:
            print(e)

    def _row_to_tag(self, row) -> Tag:
        # Преобразует строку БД в объект Tag.
        return Tag(id=row["id"],
                   name=row["name"])