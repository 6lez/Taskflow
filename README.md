# 📋 TaskFlow

**Консольный менеджер задач и проектов с приоритетами, дедлайнами, тегами и статистикой**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

---

## 🌟 Особенности

- ✅ **Управление задачами** — создание, просмотр, завершение и удаление
- 📁 **Проекты** — группировка задач по проектам
- 🎯 **Приоритеты** — low, medium, high, critical
- 📅 **Дедлайны** — отслеживание сроков выполнения
- 🏷️ **Теги** — гибкая категоризация задач
- 📊 **Статистика** — подробный анализ продуктивности
- 📤 **Экспорт** — JSON, CSV, Markdown
- 💾 **SQLite база данных** — надёжное хранение данных
- 🎨 **Красивый консольный интерфейс** — эмодзи и таблицы
---

## 🚀 Быстрый старт

### Требования

- Python 3.8 или выше
- SQLite3 (встроен в Python)

### Установка

```bash
# Клонировать репозиторий
git clone https://github.com/6lez/taskflow.git
cd taskflow

# (Опционально) Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Если есть зависимости
pip install -r requirements.txt
```

### Первое использование
```bash
# Добавить первую задачу
python app.py add "Изучить Python" --priority high --deadline 2024-12-31

# Посмотреть список задач
python app.py list

# Отметить задачу выполненной
python app.py done 1

# Посмотреть справку
python app.py --help
```
## 📖 Документация
### 📌 Управление задачами
#### Создать задачу
```bash
python app.py add "Название задачи" [опции]
```
Опции:
* --priority, -p — Приоритет: low, medium, high, critical (по умолчанию: medium)
* --deadline, -d — Дедлайн в формате YYYY-MM-DD
* --project — Название проекта
* --description — Описание задачи

Примеры:
```bash
# Простая задача
python app.py add "Написать отчёт"

# С приоритетом и дедлайном
python app.py add "Написать отчёт" -p high -d 2024-06-15

# С проектом и описанием
python app.py add "Код-ревью" --project "WebApp" --description "Проверить PR #42"

# Полный набор параметров
python app.py add "Релиз версии 2.0" -p critical -d 2024-07-01 --project "MainApp" --description "Финальное тестирование перед релизом"
```
#### Список задач
```bash
python app.py list [фильтры]
```
Фильтры:
* --status, -s — Фильтр по статусу: todo, in_progress, done, cancelled
* --priority, -p — Фильтр по приоритету: low, medium, high, critical
* --tag, -t — Фильтр по тегу
Примеры:
```bash
# Все задачи
python app.py list

# Только невыполненные
python app.py list --status todo

# Только высокоприоритетные
python app.py list --priority high

# Комбинация фильтров
python app.py list --status todo --priority critical

# По тегу
python app.py list --tag urgent
```
#### Завершить задачу
```bash
python app.py done <ID>
```
Пример:
```bash
python app.py done 5
```
Удалить задачу
```bash
python app.py delete <ID>
```
Пример:
```bash
python app.py delete 3
```
### 📁 Управление проектами
#### Список проектов
```bash
python app.py project list
```
#### Создать проект
```bash
python app.py project add "Название проекта" [--description "Описание"]
```
Примеры:
```bash
python app.py project add "WebApp"
python app.py project add "Учёба" --description "Образовательные задачи"
```
#### Удалить проект
```bash
python app.py project delete "Название проекта"
```
Пример:
```bash
python app.py project delete "OldProject"
```
### 🏷️ Управление тегами
#### Добавить тег к задаче
```bash
python app.py tag <ID задачи> <название тега>
```
Примеры:
```bash
python app.py tag 1 urgent
python app.py tag 2 backend
python app.py tag 2 python
```
Убрать тег с задачи
```bash
python app.py untag <ID задачи> <название тега>
```
#### Список всех тегов
```bash
python app.py tags
```
Вывод:
```bash
🏷️ Все теги (4):

 1 | • urgent
 2 | • backend
 3 | • python
 4 | • personal
```
### 📊 Статистика
```bash
python app.py stats
```
Показывает:
* 📊 Общую статистику — всего задач, выполнено, процент завершения, просроченные
* 📈 Статистику по приоритетам — распределение по critical, high, medium, low
* 📁 Статистику по проектам — количество и процент завершения в каждом проекте
* ⚡ Продуктивность — задачи за последние 7 дней
Пример вывода:
```bash
📊 Общая статистика:

  Всего задач: 15
  ✅ Выполнено: 8 (53.33%)
  🔄 В работе: 3
  📌 К выполнению: 4
  ❌ Отменено: 0
  ⏰ Просрочено: 2

📈 По приоритетам:

  🔴 Critical: 2
  🟠 High: 5
  🟡 Medium: 6
  🟢 Low: 2

📁 По проектам:

  WebApp: 8 задач (75% завершено)
  Учёба: 5 задач (40% завершено)
  Без проекта: 2 задачи (50% завершено)

⚡ Продуктивность (последние 7 дней):

  Создано: 5
  Завершено: 8
  В среднем в день: 1.14
```
### 📤 Экспорт данных
```bash
python app.py export <формат> [--output файл]
```
Форматы:
* json — Экспорт в JSON
* csv — Экспорт в CSV (совместим с Excel)
* md — Экспорт в Markdown
Примеры:
```bash
# Экспорт в JSON (по умолчанию tasks_export.json)
python app.py export json

# Экспорт в CSV с пользовательским именем
python app.py export csv --output my_tasks.csv

# Экспорт в Markdown
python app.py export md -o weekly_report.md
```
### 💡 Примеры использования
#### Сценарий 1: Управление учебными задачами
```bash
# Создать проект
python app.py project add "Учёба Python" --description "Курс по Python разработке"

# Добавить задачи
python app.py add "Пройти модуль 1" --project "Учёба Python" -p high -d 2024-06-20
python app.py add "Решить практические задачи" --project "Учёба Python" -p medium -d 2024-06-22
python app.py add "Написать финальный проект" --project "Учёба Python" -p critical -d 2024-06-30

# Добавить теги
python app.py tag 1 python
python app.py tag 1 learning
python app.py tag 2 practice
python app.py tag 3 project

# Посмотреть задачи проекта
python app.py list

# Завершить первую задачу
python app.py done 1

# Посмотреть статистику
python app.py stats
```
#### Сценарий 2: Рабочие задачи с приоритетами
```bash
# Создать проект
python app.py project add "Работа" --description "Рабочие задачи"

# Добавить срочные задачи
python app.py add "Исправить критический баг" --project "Работа" -p critical -d 2024-06-10
python app.py add "Провести код-ревью" --project "Работа" -p high -d 2024-06-12

# Добавить теги
python app.py tag 1 urgent
python app.py tag 1 bugfix
python app.py tag 2 review

# Посмотреть только критические задачи
python app.py list --priority critical

# Экспортировать отчёт для менеджера
python app.py export md -o weekly_report.md
```
#### Сценарий 3: Личные дела
```bash
# Добавить задачи без проекта
python app.py add "Купить продукты" -p low
python app.py add "Записаться к врачу" -p medium -d 2024-06-15
python app.py add "Оплатить счета" -p high -d 2024-06-11

# Добавить теги
python app.py tag 1 shopping
python app.py tag 2 health
python app.py tag 3 finance

# Посмотреть задачи по тегу
python app.py list --tag health

# Завершить задачу
python app.py done 1
```
### 📂 Структура проекта
```bash
TaskFlow/
├── data/
│   └── taskflow.db              # База данных SQLite (создаётся автоматически)
├── taskflow/
│   ├── repositories/            # Слой работы с базой данных
│   │   ├── __init__.py
│   │   ├── task_repo.py         # CRUD для задач
│   │   ├── project_repo.py      # CRUD для проектов
│   │   └── tag_repo.py          # CRUD для тегов
│   ├── services/                # Бизнес-логика
│   │   ├── task_service.py      # Сервис управления задачами
│   │   ├── stats_service.py     # Сервис статистики
│   │   └── export_service.py    # Сервис экспорта
│   ├── utils/                   # Утилиты (если понадобятся)
│   ├── __init__.py
│   ├── database.py              # Управление подключением к БД
│   └── models.py                # Модели данных (Task, Project, Tag)
├── tests/                       # Тесты (для будущего развития)
├── app.py                       # Главный файл приложения
├── requirements.txt             # Зависимости Python (если есть)
├── .gitignore
├── LICENSE
└── README.md
```
## 🛠️ Технологии
* Python 3.8+ — основной язык
* SQLite3 — встроенная база данных
* argparse — парсинг аргументов командной строки
* dataclasses — удобные модели данных
* csv, json — экспорт данных
* datetime — работа с датами
## 🧪 Тестирование
```bash
# Запустить тесты (когда будут реализованы)
python -m pytest tests/
```
## 📄 Лицензия
Этот проект распространяется под лицензией MIT. См. файл LICENSE для подробностей.
## 👤 Автор
Глеб Ефимов  
GitHub: @6lez  
Email: efimo.egi@gmail.com  