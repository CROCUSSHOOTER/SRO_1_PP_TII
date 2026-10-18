"""
Модуль 1: models.py
Предметные сущности системы мониторинга учебных проектов.
Реализует принципы ООП: классы, инкапсуляцию, наследование, интерфейсы и композицию (Лекции 5, 6).
"""

from abc import ABC, abstractmethod
from typing import List


class Task:
    """Сущность 'Задача' с инкапсулированным состоянием."""
    def __init__(self, task_id: str, title: str, weight: int, completed: bool = False):
        self.__task_id = task_id
        self.__title = title
        self.__weight = weight
        self.__completed = completed

    @property
    def task_id(self) -> str:
        return self.__task_id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def weight(self) -> int:
        return self.__weight

    @property
    def completed(self) -> bool:
        return self.__completed

    def complete(self) -> None:
        """Изменение состояния задачи с защитой данных."""
        self.__completed = True

    def to_dict(self) -> dict:
        return {
            "task_id": self.__task_id,
            "title": self.__title,
            "weight": self.__weight,
            "completed": self.__completed
        }


class ProgressPolicy(ABC):
    """Общий интерфейс для вычисления прогресса проекта (Лекция 6)."""
    @abstractmethod
    def calculate(self, tasks: List[Task]) -> float:
        pass


class SimpleProgress(ProgressPolicy):
    """Простая политика: отношение выполненных задач к общему числу."""
    def calculate(self, tasks: List[Task]) -> float:
        if not tasks:
            return 0.0
        completed_count = sum(1 for t in tasks if t.completed)
        return round((completed_count / len(tasks)) * 100.0, 2)


class WeightedProgress(ProgressPolicy):
    """Взвешенная политика: учет веса (сложности) задач."""
    def calculate(self, tasks: List[Task]) -> float:
        if not tasks:
            return 0.0
        total_weight = sum(t.weight for t in tasks)
        if total_weight == 0:
            return 0.0
        completed_weight = sum(t.weight for t in tasks if t.completed)
        return round((completed_weight / total_weight) * 100.0, 2)


class Project:
    """Сущность 'Проект', использующая композицию политик расчёта."""
    def __init__(self, project_id: str, name: str, team_name: str, deadline_days_left: int, policy: ProgressPolicy = None):
        self.project_id = project_id
        self.name = name
        self.team_name = team_name
        self.deadline_days_left = deadline_days_left
        self.tasks: List[Task] = []
        self.policy: ProgressPolicy = policy if policy else SimpleProgress()

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def set_policy(self, policy: ProgressPolicy) -> None:
        self.policy = policy

    def get_progress(self) -> float:
        return self.policy.calculate(self.tasks)