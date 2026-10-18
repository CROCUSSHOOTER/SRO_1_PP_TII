"""
Модуль 2: logic.py
Бизнес-логика, процедурный подход, чистые функции и функциональные конвейеры (Лекции 2, 3, 7, 8).
"""

from typing import List, Callable
from models import Project, Task


# Лекция 2: Императивный прототип поиска рисков с циклами и условиями
def imperative_find_risks(projects: List[Project], threshold_days: int) -> List[str]:
    risky_teams = []
    for proj in projects:
        if proj.deadline_days_left < threshold_days and proj.get_progress() < 70.0:
            risky_teams.append(proj.team_name)
    return risky_teams


# Лекция 3: Процедурная декомпозиция (6+ функций с явными параметрами и результатами)
def create_project_record(proj_id: str, name: str, team: str, days: int) -> dict:
    return {"id": proj_id, "name": name, "team": team, "days": days, "tasks": []}


def add_task_to_record(record: dict, task_id: str, title: str, weight: int) -> dict:
    record["tasks"].append({"id": task_id, "title": title, "weight": weight, "completed": False})
    return record


def mark_task_completed_in_record(record: dict, task_id: str) -> dict:
    for task in record["tasks"]:
        if task["id"] == task_id:
            task["completed"] = True
    return record


def calculate_record_progress(record: dict) -> float:
    tasks = record["tasks"]
    if not tasks:
        return 0.0
    completed = sum(1 for t in tasks if t["completed"])
    return round((completed / len(tasks)) * 100.0, 2)


def filter_delayed_records(records: List[dict], min_days: int) -> List[dict]:
    return [r for r in records if r["days"] < min_days]


def generate_group_rating_report(records: List[dict]) -> List[tuple]:
    sorted_recs = sorted(records, key=lambda r: calculate_record_progress(r), reverse=True)
    return [(r["team"], r["name"], calculate_record_progress(r)) for r in sorted_recs]


# Лекция 7: Чистые функции (не изменяющие входные коллекции) и рекурсия
def pure_filter_high_progress(projects: List[Project], min_progress: float) -> List[Project]:
    """Чистая функция: возвращает новый список проектов без мутации исходного."""
    return [p for p in projects if p.get_progress() >= min_progress]


def recursive_factorial_weight_sum(tasks: List[Task]) -> int:
    """Рекурсивный обход задач для вычисления условного суммарного веса с коэффициентами."""
    def _helper(lst: List[Task], index: int) -> int:
        if index >= len(lst):
            return 0
        return lst[index].weight + _helper(lst, index + 1)
    return _helper(tasks, 0)


# Лекция 8: Конвейерная обработка (map, filter, reduce) и замыкания
from functools import reduce

def make_risk_filter_closure(max_days: int, min_progress: float) -> Callable[[Project], bool]:
    """Замыкание, создающее функцию фильтрации по динамическим критериям риска."""
    def filter_func(project: Project) -> bool:
        return project.deadline_days_left <= max_days and project.get_progress() < min_progress
    return filter_func


def functional_pipeline_analysis(projects: List[Project], max_days: int, min_progress: float) -> List[str]:
    """Конвейер на базе filter, map для анализа проектов."""
    risk_predicate = make_risk_filter_closure(max_days, min_progress)
    
    # filter с использованием замыкания
    filtered_projects = filter(risk_predicate, projects)
    
    # map для извлечения названий команд
    team_names = map(lambda p: f"Команда: {p.team_name} (Проект: {p.name}, Прогресс: {p.get_progress()}%)", filtered_projects)
    
    return list(team_names)


def functional_calculate_total_budget_or_weight(projects: List[Project]) -> int:
    """Использование reduce для агрегации суммарного веса задач всех проектов."""
    all_weights = [t.weight for p in projects for t in p.tasks]
    return reduce(lambda acc, w: acc + w, all_weights, 0)