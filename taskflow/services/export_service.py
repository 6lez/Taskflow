"""Сервис для экспорта задач в различные форматы."""

import json
import csv
from datetime import datetime
from taskflow.repositories.task_repo import TaskRepository
from taskflow.repositories.project_repo import ProjectRepository
from taskflow.repositories.tag_repo import TagRepository


class ExportService:
    """Сервис экспорта данных."""

    def __init__(self, task_repo: TaskRepository,
                 project_repo: ProjectRepository,
                 tag_repo: TagRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.tag_repo = tag_repo

    def export_to_json(self, filename: str = "tasks_export.json") -> str:
        """Экспортирует задачи в JSON."""
        all_tasks = self.task_repo.get_all()

        tasks_data = []
        for task in all_tasks:
            # Получаем проект
            project_name = None
            if task.project_id:
                project = self.project_repo.get_by_id(task.project_id)
                project_name = project.name if project else None

            # Получаем теги
            tags = self.tag_repo.get_tags_for_task(task.id)
            tag_names = [tag.name for tag in tags]

            # Форматируем даты
            deadline_str = None
            if task.deadline:
                if isinstance(task.deadline, datetime):
                    deadline_str = task.deadline.strftime("%Y-%m-%d")
                else:
                    deadline_str = str(task.deadline)

            created_at_str = None
            if task.created_at:
                if isinstance(task.created_at, datetime):
                    created_at_str = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    created_at_str = str(task.created_at)

            completed_at_str = None
            if task.completed_at:
                if isinstance(task.completed_at, datetime):
                    completed_at_str = task.completed_at.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    completed_at_str = str(task.completed_at)

            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "status": task.status,
                "project": project_name,
                "tags": tag_names,
                "deadline": deadline_str,
                "created_at": created_at_str,
                "completed_at": completed_at_str
            }
            tasks_data.append(task_dict)

        # Сохраняем в файл
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)

        return filename

    def export_to_csv(self, filename: str = "tasks_export.csv") -> str:
        """Экспортирует задачи в CSV."""
        all_tasks = self.task_repo.get_all()

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ID', 'Название', 'Описание', 'Приоритет',
                          'Статус', 'Проект', 'Теги', 'Дедлайн',
                          'Создано', 'Завершено']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for task in all_tasks:
                # Получаем проект
                project_name = ""
                if task.project_id:
                    project = self.project_repo.get_by_id(task.project_id)
                    project_name = project.name if project else ""

                # Получаем теги
                tags = self.tag_repo.get_tags_for_task(task.id)
                tag_names = ", ".join([tag.name for tag in tags])

                # Форматируем даты
                deadline_str = ""
                if task.deadline:
                    if isinstance(task.deadline, datetime):
                        deadline_str = task.deadline.strftime("%Y-%m-%d")
                    else:
                        deadline_str = str(task.deadline)

                created_at_str = ""
                if task.created_at:
                    if isinstance(task.created_at, datetime):
                        created_at_str = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        created_at_str = str(task.created_at)

                completed_at_str = ""
                if task.completed_at:
                    if isinstance(task.completed_at, datetime):
                        completed_at_str = task.completed_at.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        completed_at_str = str(task.completed_at)

                writer.writerow({
                    'ID': task.id,
                    'Название': task.title,
                    'Описание': task.description,
                    'Приоритет': task.priority,
                    'Статус': task.status,
                    'Проект': project_name,
                    'Теги': tag_names,
                    'Дедлайн': deadline_str,
                    'Создано': created_at_str,
                    'Завершено': completed_at_str
                })

        return filename

    def export_to_markdown(self, filename: str = "tasks_export.md") -> str:
        """Экспортирует задачи в Markdown."""
        all_tasks = self.task_repo.get_all()
        all_projects = self.project_repo.get_all()

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 📋 Экспорт задач TaskFlow\n\n")
            f.write(f"*Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M')}*\n\n")
            f.write("---\n\n")

            # Группировка по проектам
            tasks_by_project = {}
            for task in all_tasks:
                if task.project_id:
                    project = self.project_repo.get_by_id(task.project_id)
                    project_name = project.name if project else "Без проекта"
                else:
                    project_name = "Без проекта"

                if project_name not in tasks_by_project:
                    tasks_by_project[project_name] = []
                tasks_by_project[project_name].append(task)

            # Вывод по проектам
            for project_name, tasks in tasks_by_project.items():
                f.write(f"## 📁 {project_name}\n\n")

                for task in tasks:
                    # Чекбокс
                    checkbox = "- [x]" if task.status == "done" else "- [ ]"

                    # Приоритет
                    priority_emoji = {
                        "critical": "🔴",
                        "high": "🟠",
                        "medium": "🟡",
                        "low": "🟢"
                    }.get(task.priority, "⚪")

                    # Теги
                    tags = self.tag_repo.get_tags_for_task(task.id)
                    tags_str = " ".join([f"`{tag.name}`" for tag in tags])

                    # Дедлайн
                    deadline_str = ""
                    if task.deadline:
                        if isinstance(task.deadline, datetime):
                            deadline_str = f" 📅 {task.deadline.strftime('%d.%m.%Y')}"
                        else:
                            deadline_str = f" 📅 {task.deadline}"

                    f.write(f"{checkbox} {priority_emoji} **{task.title}**{deadline_str}")
                    if tags_str:
                        f.write(f" {tags_str}")
                    f.write("\n")

                    if task.description:
                        f.write(f"  > {task.description}\n")

                    f.write("\n")

                f.write("\n")

        return filename