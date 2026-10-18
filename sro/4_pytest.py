"""
Модуль 4: test_project.py
Набор автоматических тестов (не менее 12 тестов: нормальные, граничные и ошибочные сценарии).
Запуск через pytest.
"""

import pytest
from models import Task, Project, SimpleProgress, WeightedProgress
from logic import (
    imperative_find_risks,
    create_project_record,
    add_task_to_record,
    mark_task_completed_in_record,
    calculate_record_progress,
    filter_delayed_records,
    pure_filter_high_progress,
    recursive_factorial_weight_sum,
    make_risk_filter_closure
)


def test_task_creation():
    """Тест 1: Создание задачи и проверка свойств."""
    task = TestTask = Task("T1", "Тест", 5, completed=False)
    assert task.task_id == "T1"
    assert task.title == "Тест"
    assert task.weight == 5
    assert task.completed is False


def test_task_completion():
    """Тест 2: Изменение статуса задачи."""
    task = Task("T1", "Тест", 5)
    task.complete()
    assert task.completed is True


def test_simple_progress_policy():
    """Тест 3: Расчет простого прогресса."""
    tasks = [
        Task("1", "А", 1, True),
        Task("2", "Б", 1, False)
    ]
    policy = SimpleProgress()
    assert policy.calculate(tasks) == 50.0


def test_weighted_progress_policy():
    """Тест 4: Расчет взвешенного прогресса."""
    tasks = [
        Task("1", "А", 3, True),   # вес 3 выполнен
        Task("2", "Б", 7, False)   # вес 7 не выполнен
    ]
    policy = WeightedProgress()
    assert policy.calculate(tasks) == 30.0


def test_project_empty_tasks():
    """Тест 5 (Граничный): Проект без задач возвращает 0 прогресс."""
    proj = Project("P1", "Пустой", "Команда А", 10)
    assert proj.get_progress() == 0.0


def test_imperative_find_risks():
    """Тест 6: Императивный поиск рисков."""
    proj1 = Project("P1", "Проект 1", "Alpha", 3) # дедлайн 3 (<10), прогресс 0 (<70)
    proj2 = Project("P2", "Проект 2", "Beta", 20)
    risks = imperative_find_risks([proj1, proj2], threshold_days=10)
    assert "Alpha" in risks
    assert "Beta" not in risks


def test_procedural_record_workflow():
    """Тест 7: Процедурный цикл работы с записями (Лекция 3)."""
    rec = create_project_record("R1", "Рекорд", "Гамма", 5)
    rec = add_task_to_record(rec, "T1", "Задача 1", 4)
    rec = mark_task_completed_in_record(rec, "T1")
    assert calculate_record_progress(rec) == 100.0


def test_filter_delayed_records():
    """Тест 8: Фильтрация записей по сроку."""
    recs = [
        {"team": "T1", "days": 3},
        {"team": "T2", "days": 15}
    ]
    filtered = filter_delayed_records(recs, min_days=10)
    assert len(filtered) == 1
    assert filtered[0]["team"] == "T1"


def test_pure_filter_high_progress():
    """Тест 9: Чистая функция фильтрации проектов."""
    p1 = Project("1", "П1", "К1", 5)
    p1.add_task(Task("t1", "д", 10, True)) # 100%
    p2 = Project("2", "П2", "К2", 5) # 0%
    
    filtered = pure_filter_high_progress([p1, p2], min_progress=50.0)
    assert len(filtered) == 1
    assert filtered[0].project_id == "1"


def test_recursive_weight_sum():
    """Тест 10: Рекурсивное вычисление суммы весов."""
    tasks = [
        Task("1", "А", 2),
        Task("2", "Б", 3),
        Task("3", "В", 5)
    ]
    assert recursive_factorial_weight_sum(tasks) == 10


def test_risk_filter_closure():
    """Тест 11: Замыкание для фильтрации рисков."""
    risk_checker = make_risk_filter_closure(max_days=5, min_progress=50.0)
    proj = Project("1", "Тест", "К", 3)
    # Прогресс 0 (<50), дедлайн 3 (<=5) -> Риск True
    assert risk_checker(proj) is True


def test_error_zero_total_weight():
    """Тест 12 (Ошибочный / Граничный): Нулевой общий вес задач во взвешенной политике."""
    tasks = [
        Task("1", "А", 0),
        Task("2", "Б", 0)
    ]
    policy = WeightedProgress()
    assert policy.calculate(tasks) == 0.0