"""Модуль для работы с SQLite базой данных."""

import sqlite3
import os

class Database:
    """Управление подключением и инициализацией БД."""
    def __init__(self, db_path: str = "data/taskflow.db"):
        """
        Инициализация БД.

        Args:
            db_path:.
                     ":memory:" — для тестов (БД в оперативке).
        """
        self.db_path = db_path

        # Создание папки data/, если её нет
        if db_path != ":memory:":
            self._ensure_directory()

        # Подключение к БД
        self.connection = sqlite3.connect(self.db_path)

        # Это позволяет обращаться к колонкам по имени: row["title"]
        self.connection.row_factory = sqlite3.Row

        # Включаем поддержку внешних ключей (FOREIGN KEY)
        self.connection.execute("PRAGMA foreign_keys = ON")

        # Создаём таблицы
        self._create_tables()

    def _ensure_directory(self):
        """Создаёт директорию для файла БД, если не существует."""
        directory = os.path.dirname(self.db_path)
        if directory:  # если путь содержит директорию
            os.makedirs(directory, exist_ok=True)

    def _create_tables(self):
        """Создаёт таблицы, если они ещё не существуют."""
        self.connection.executescript("""
                                      CREATE TABLE IF NOT EXISTS projects
                                      (
                                          id
                                          INTEGER
                                          PRIMARY
                                          KEY
                                          AUTOINCREMENT,
                                          name
                                          TEXT
                                          NOT
                                          NULL
                                          UNIQUE,
                                          description
                                          TEXT,
                                          created_at
                                          TIMESTAMP
                                          DEFAULT
                                          CURRENT_TIMESTAMP
                                      );

                                      CREATE TABLE IF NOT EXISTS tasks
                                      (
                                          id
                                          INTEGER
                                          PRIMARY
                                          KEY
                                          AUTOINCREMENT,
                                          title
                                          TEXT
                                          NOT
                                          NULL,
                                          description
                                          TEXT,
                                          priority
                                          TEXT
                                          CHECK (
                                          priority
                                          IN
                                      (
                                          'low',
                                          'medium',
                                          'high',
                                          'critical'
                                      ))
                                          DEFAULT 'medium',
                                          status TEXT CHECK
                                      (
                                          status
                                          IN
                                      (
                                          'todo',
                                          'in_progress',
                                          'done',
                                          'cancelled'
                                      ))
                                          DEFAULT 'todo',
                                          project_id INTEGER,
                                          deadline TIMESTAMP,
                                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                          completed_at TIMESTAMP,
                                          FOREIGN KEY
                                      (
                                          project_id
                                      ) REFERENCES projects
                                      (
                                          id
                                      )
                                          );
                                      CREATE TABLE IF NOT EXISTS tags
                                      (
                                          id
                                          INTEGER
                                          PRIMARY
                                          KEY
                                          AUTOINCREMENT,
                                          name
                                          TEXT
                                          NOT
                                          NULL
                                          UNIQUE
                                      );

                                      CREATE TABLE IF NOT EXISTS task_tags
                                      (
                                          task_id
                                          INTEGER,
                                          tag_id
                                          INTEGER,
                                          PRIMARY
                                          KEY
                                      (
                                          task_id,
                                          tag_id
                                      ),
                                          FOREIGN KEY
                                      (
                                          task_id
                                      ) REFERENCES tasks
                                      (
                                          id
                                      ) ON DELETE CASCADE,
                                          FOREIGN KEY
                                      (
                                          tag_id
                                      ) REFERENCES tags
                                      (
                                          id
                                      )
                                        ON DELETE CASCADE
                                          );
                                      """)
        self.connection.commit()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """
        Выполняет SQL-запрос.
        Args:
            query: SQL-запрос с плейсхолдерами (?).
            params: параметры для подстановки.

        Returns:
            Курсор с результатами.
        """
        return self.connection.execute(query, params)

    def commit(self):
        """Сохраняет изменения в БД."""
        self.connection.commit()

    def close(self):
        """Закрывает соединение с БД."""
        self.connection.close()