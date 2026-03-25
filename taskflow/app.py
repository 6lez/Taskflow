"""Интерфейс Taskflow."""

import argparse
from taskflow.database import Database
from taskflow.models import Project, Tag
from taskflow.repositories.task_repo import TaskRepository
from taskflow.repositories.project_repo import ProjectRepository
from taskflow.repositories.tag_repo import TagRepository
from taskflow.services.task_service import TaskService

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Taskflow — менеджер задач"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Команда: add
    add_parser = subparsers.add_parser("add", help="Добавить задачу")
    add_parser.add_argument("title", help="Название задачи")
    add_parser.add_argument(
        "--priority", "-p",
        choices=["low", "medium", "high", "critical"],
        default="medium",
        help="Приоритет задачи"
    )
    add_parser.add_argument(
        "--deadline", "-d",
        help="Дедлайн (формат: YYYY-MM-DD)"
    )
    add_parser.add_argument(
        "--project",
        help="Название проекта"
    )
    add_parser.add_argument(
        "--description",
        default="",
        help="Описание задачи"
    )

    # Команда: list
    list_parser = subparsers.add_parser("list", help="Список задач")
    list_parser.add_argument("--status", "-s", help="Фильтр по статусу")
    list_parser.add_argument("--priority", "-p", help="Фильтр по приоритету")
    list_parser.add_argument("--tag", "-t", help="Фильтр по тегу")

    # Команда: done
    done_parser = subparsers.add_parser("done", help="Завершить задачу")
    done_parser.add_argument("id", type=int, help="ID задачи")

    # Команда: delete
    delete_parser = subparsers.add_parser("delete", help="Удалить задачу")
    delete_parser.add_argument("id", type=int, help="ID задачи")

    # Команда: projects
    project_parser = subparsers.add_parser("project", help="Управление проектами")
    project_subparsers = project_parser.add_subparsers(dest="project_command")
    # project list
    project_subparsers.add_parser("list", help="Показать все проекты")
    # project add
    project_add_parser = project_subparsers.add_parser("add", help="Создать проект")
    project_add_parser.add_argument("name", help="Название проекта")
    project_add_parser.add_argument("--description", default="", help="Описание проекта")
    # project delete
    project_delete_parser = project_subparsers.add_parser("delete", help="Удалить проект")
    project_delete_parser.add_argument("name", help="Название проекта для удаления")

    # Команда: tag
    tag_parser = subparsers.add_parser("tag", help="Добавить тег к задаче")
    tag_parser.add_argument("task_id", type=int, help="ID задачи")
    tag_parser.add_argument("tag_name", help="Название тега")
    # Команда: untag
    untag_parser = subparsers.add_parser("untag", help="Убрать тег с задачи")
    untag_parser.add_argument("task_id", type=int, help="ID задачи")
    untag_parser.add_argument("tag_name", help="Название тега")
    # Команда: tags
    subparsers.add_parser("tags", help="Показать все теги")

    return parser

def display_tasks(tasks, tag_repo=None):
    if not tasks:
        print("📭 Задач не найдено.")
        return
    priority_icons = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢"
    }
    status_icons = {
        "todo": "📌",
        "in_progress": "🔄",
        "done": "✅",
        "cancelled": "❌"
    }
    print(f"\n📋 Список задач ({len(tasks)}):\n")
    print(f" {'ID':>3} │ {'Название':<25}│ {'Приоритет':<12}│ {'Статус':<13}│ {'Дедлайн':<14}│ {'Теги':<14}")
    print(f"{'─' * 4}┼{'─' * 26}┼{'─' * 13}┼{'─' * 14}┼{'─' * 15}┼{'─' * 15}")
    for task in tasks:
        # Иконка приоритета
        icon = priority_icons.get(task.priority, "⚪")
        priority_str = f"{icon} {task.priority}"
        # Иконка статуса
        status_icon = status_icons.get(task.status, "❓")
        status_str = f"{status_icon} {task.status}"
        if tag_repo:
            tags = ', '.join(tag_repo.get_tags_for_task(task.id))
        if task.deadline:
            if hasattr(task.deadline, 'strftime'):
                deadline_str = task.deadline.strftime("%d.%m.%Y")
            else:
                deadline_str = str(task.deadline)
        else:
            deadline_str = "—"
        title = task.title
        # Обрезание
        if len(title) > 23:
            title = title[:20] + "..."
        print(f" {task.id:>3} │ {title:<25}│ {priority_str:<12}│ {status_str:<13}│ {deadline_str:<14}│ {tags:<14}")
    print()

def display_projects(projects):
    # Вывод списка проектов.
    if not projects:
        print("📭 Проектов не найдено.")
        return
    print(f"\n📁 Проекты ({len(projects)}):\n")
    print(f" {'ID':>3} │ {'Название':<20}│ {'Описание':<30}")
    print(f"{'─' * 4}┼{'─' * 21}┼{'─' * 31}")
    for project in projects:
        name = project.name
        if len(name) > 18:
            name = name[:15] + "..."
        description = project.description or ""
        if len(description) > 28:
            description = project.description[:25] + "..."
        print(f" {project.id:>3} │ {name:<21}│ {description:<31}")
    print()

def main():
    parser = create_parser()
    args = parser.parse_args()

    db = Database()
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    tag_repo = TagRepository(db)
    service = TaskService(task_repo, project_repo, tag_repo)

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "add":
            task_id = service.create_task(
                title=args.title,
                priority=args.priority,
                deadline=args.deadline,
                project_name=args.project,
                description=args.description
            )
            print(f'✅ Задача #{task_id} создана!')


        elif args.command == "list":
            tasks = service.get_tasks(status=args.status, priority=args.priority)
            # Фильтрация по тегу.
            if args.tag:
                tag = tag_repo.get_by_name(args.tag)
                if tag is None:
                    print(f"❌ Тег '{args.tag}' не найден")
                    return
                tagged_task_ids = {t.id for t in ...}  # подумай как получить
                tasks = [t for t in tasks if t.id in tagged_task_ids]
            display_tasks(tasks, tag_repo=tag_repo)

        elif args.command == "done":
            service.complete_task(args.id)
            print(f'✅ Задача #{args.id} выполнена!')

        elif args.command == "delete":
            service.delete_task(args.id)
            print(f'🗑️ Задача #{args.id} удалена!')

        elif args.command == "project":
            if args.project_command == 'list':
                projects = project_repo.get_all()
                display_projects(projects)
            elif args.project_command == 'add':
                project_repo.add(Project(name=args.name,
                                         description=args.description))
                print(f'✅ Проект {args.name} создан!')
            elif args.project_command == 'delete':
                project = project_repo.get_by_name(args.name)
                if project is None:
                    print(f"❌ Проект '{args.name}' не найден!")
                else:
                    project_repo.delete(project.id)
                    print(f"🗑️ Проект '{args.name}' удалён!")
            else:
                print("Используйте: project [list|add|delete]")
        else:
            parser.print_help()

    except ValueError as e:
        print(f"❌ Ошибка: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()