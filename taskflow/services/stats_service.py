"""Сервис для статистики по задачам."""

from datetime import datetime, timedelta
from taskflow.repositories.task_repo import TaskRepository
from taskflow.repositories.project_repo import ProjectRepository
from taskflow.repositories.tag_repo import TagRepository


class StatsService:
    """Сервис для получения статистики."""

    def __init__(self, task_repo: TaskRepository,
                 project_repo: ProjectRepository,
                 tag_repo: TagRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.tag_repo = tag_repo

    def get_general_stats(self) -> dict:
        """Получает общую статистику по задачам."""
        all_tasks = self.task_repo.get_all()

        total = len(all_tasks)
        done = len([t for t in all_tasks if t.status == "done"])
        in_progress = len([t for t in all_tasks if t.status == "in_progress"])
        todo = len([t for t in all_tasks if t.status == "todo"])
        cancelled = len([t for t in all_tasks if t.status == "cancelled"])

        # Процент выполнения
        completion_rate = (done / total * 100) if total > 0 else 0

        # Задачи с истёкшим дедлайном
        overdue = 0
        now = datetime.now()
        for task in all_tasks:
            if task.deadline and task.status != "done":
                # Парсим дедлайн если он строка
                deadline = task.deadline
                if isinstance(deadline, str):
                    try:
                        deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        try:
                            deadline = datetime.strptime(deadline, "%Y-%m-%d")
                        except ValueError:
                            continue
                if deadline < now:
                    overdue += 1

        return {
            "total": total,
            "done": done,
            "in_progress": in_progress,
            "todo": todo,
            "cancelled": cancelled,
            "overdue": overdue,
            "completion_rate": round(completion_rate, 2)
        }

    def get_stats_by_priority(self) -> dict:
        """Статистика по приоритетам."""
        all_tasks = self.task_repo.get_all()

        stats = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }

        for task in all_tasks:
            if task.priority in stats:
                stats[task.priority] += 1

        return stats

    def get_stats_by_project(self) -> dict:
        """Статистика по проектам."""
        all_tasks = self.task_repo.get_all()
        all_projects = self.project_repo.get_all()

        stats = {}

        # Инициализация
        for project in all_projects:
            stats[project.name] = {
                "total": 0,
                "done": 0,
                "in_progress": 0,
                "todo": 0
            }

        # Задачи без проекта
        stats["Без проекта"] = {
            "total": 0,
            "done": 0,
            "in_progress": 0,
            "todo": 0
        }

        # Подсчёт
        for task in all_tasks:
            if task.project_id:
                project = self.project_repo.get_by_id(task.project_id)
                project_name = project.name if project else "Без проекта"
            else:
                project_name = "Без проекта"

            if project_name in stats:
                stats[project_name]["total"] += 1
                if task.status == "done":
                    stats[project_name]["done"] += 1
                elif task.status == "in_progress":
                    stats[project_name]["in_progress"] += 1
                elif task.status == "todo":
                    stats[project_name]["todo"] += 1

        return stats

    def get_stats_by_tags(self) -> dict:
        """Статистика по тегам."""
        all_tags = self.tag_repo.get_all()
        all_tasks = self.task_repo.get_all()

        stats = {}

        for tag in all_tags:
            count = 0
            for task in all_tasks:
                task_tags = self.tag_repo.get_tags_for_task(task.id)
                if any(t.id == tag.id for t in task_tags):
                    count += 1
            stats[tag.name] = count

        return stats

    def get_productivity_stats(self, days: int = 7) -> dict:
        """Статистика продуктивности за последние N дней."""
        all_tasks = self.task_repo.get_all()
        now = datetime.now()
        cutoff_date = now - timedelta(days=days)

        completed_tasks = []
        created_tasks = []

        for task in all_tasks:
            # Созданные задачи
            if task.created_at:
                created_at = task.created_at
                if isinstance(created_at, str):
                    try:
                        created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        continue
                if created_at >= cutoff_date:
                    created_tasks.append(task)

            # Завершённые задачи
            if task.completed_at:
                completed_at = task.completed_at
                if isinstance(completed_at, str):
                    try:
                        completed_at = datetime.strptime(completed_at, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        continue
                if completed_at >= cutoff_date:
                    completed_tasks.append(task)

        return {
            "days": days,
            "created": len(created_tasks),
            "completed": len(completed_tasks),
            "avg_per_day": round(len(completed_tasks) / days, 2)
        }