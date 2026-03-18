"""Бизнес-логика для управления задачами."""

from datetime import datetime
from taskflow.models import Task
from taskflow.repositories.task_repo import TaskRepository
from taskflow.repositories.project_repo import ProjectRepository
from taskflow.repositories.tag_repo import TagRepository

class TaskService:
    # Сервис управления задачами.

    VALID_PRIORITIES = ("low", "medium", "high", "critical")
    VALID_STATUSES = ("todo", "in_progress", "done", "cancelled")

    def __init__(self, task_repo: TaskRepository,
                 project_repo: ProjectRepository,
                 tag_repo: TagRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.tag_repo = tag_repo

    def create_task(self, title: str, priority: str = "medium",
                    description: str = "", deadline: str = None,
                    project_name: str = None) -> int:
        # Создаёт задачу с валидацией.
        if not title or not title.strip():
            raise ValueError('Название задачи не может быть пустым')

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f'Приоритет должен быть в виде: {self.VALID_PRIORITIES}')

        parsed_deadline = None
        if deadline is not None:
            try:
                parsed_deadline = datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Формат дедлайна: YYYY-MM-DD")

        project_id = None
        if project_name is not None:
            project = self.project_repo.get_by_name(project_name)
            if project is None:
                raise ValueError(f"Проект '{project_name}' не найден!")
            project_id = project.id

        task_id = self.task_repo.add(Task(title=title,
                                          priority=priority,
                                          description=description,
                                          deadline=parsed_deadline,
                                          project_name=project_id))
        return task_id

    def complete_task(self, task_id: int) -> Task:
        # Отмечает задачу как выполненную.
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise ValueError(f'Задача #{task_id} не найдена!')
        if task.status == "done":
            raise ValueError(f'Задача #{task_id} уже выполнена!')
        task.status = "done"
        task.completed_at = datetime.now()
        self.task_repo.update(task)
        return task

    def get_tasks(self, status: str = None, priority: str = None) -> list[Task]:
        # Получает список задач с опциональными фильтрами.
        all_tasks = self.task_repo.get_all()
        if status is not None:
            if status not in self.VALID_STATUSES:
                raise ValueError(f"Статус должен быть в виде: {self.VALID_STATUSES}")
            all_tasks = [t for t in all_tasks if t.status == status]

        if priority is not None:
            if priority not in self.VALID_PRIORITIES:
                raise ValueError(f"Приоритет должен быть в виде: {self.VALID_PRIORITIES}")
            all_tasks = [t for t in all_tasks if t.priority == priority]

        return all_tasks

    def delete_task(self, task_id: int) -> bool:
        # Удаляет задачу.
        if not(self.task_repo.delete(task_id)):
            raise ValueError(f'Задача #{task_id} не найдена')
        return True