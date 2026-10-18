"""
Модуль 3: main.py
Точка входа в приложение, консольное меню и демонстрация работы системы (Лекция 4).
"""

from models import Project, Task, SimpleProgress, WeightedProgress
from logic import (
    imperative_find_risks,
    pure_filter_high_progress,
    functional_pipeline_analysis,
    functional_calculate_total_budget_or_weight
)


def seed_initial_data() -> List[Project]:
    """Генерация не менее 20 содержательных записей для демонстрации."""
    projects = []
    teams_data = [
        ("П-01", "Анализатор трафика", "Альфа", 5),
        ("П-02", "Система Умный дом", "Бета", 15),
        ("П-03", "Чат-бот вуза", "Гамма", 2),
        ("П-04", "Финтех Скорринг", "Дельта", 10),
        ("П-05", "Медицинский агрегатор", "Омега", 25),
    ]
    
    for idx, (pid, name, team, days) in enumerate(teams_data):
        # Чередуем политики для демонстрации полиморфизма
        policy = WeightedProgress() if idx % 2 == 0 else SimpleProgress()
        proj = Project(pid, name, team, days, policy)
        
        # Добавляем задачи
        t1 = Task(f"{pid}-T1", "Проектирование архитектуры", 3, completed=True)
        t2 = Task(f"{pid}-T2", "Разработка модуля БД", 5, completed=(idx % 2 == 0))
        t3 = Task(f"{pid}-T3", "Тестирование и деплой", 2, completed=False)
        
        proj.add_task(t1)
        proj.add_task(t2)
        proj.add_task(t3)
        projects.append(proj)
        
    return projects


def main():
    print("==================================================")
    print(" СИСТЕМА МОНИТОРИНГА УЧЕБНЫХ ПРОЕКТОВ (СРО Тема №9)")
    print(" Студент: Жусупов Айболат | Группа: ТИИ-25-21")
    print("==================================================")
    
    projects = seed_initial_data()
    
    while True:
        print("\n--- ГЛАВНОЕ МЕНЮ ---")
        print("1. Показать список всех проектов и прогресс")
        print("2. Императивный поиск рисков (Лекция 2)")
        print("3. Демонстрация чистых функций и рекурсии (Лекция 7)")
        print("4. Функциональный конвейер и замыкания (Лекция 8)")
        print("5. Сравнение парадигм (Императивная vs Объектно-ориентированная)")
        print("6. Выход")
        
        choice = input("Выберите пункт меню (1-6): ").strip()
        
        if choice == "1":
            print("\n[Список проектов]")
            for p in projects:
                print(f"- [{p.project_id}] {p.name} | Команда: {p.team_name} | Срок: {p.deadline_days_left} дн. | Прогресс: {p.get_progress()}% | Политика: {type(p.policy).__name__}")
        
        elif choice == "2":
            print("\n[Императивный поиск рисков (дедлайн < 10 дней, прогресс < 70%)]")
            risks = imperative_find_risks(projects, threshold_days=10)
            print( команды в зоне риска: {risks}")
        
        elif choice == "3":
            print("\n[Чистые функции и рекурсия]")
            high_prog = pure_filter_high_progress(projects, min_progress=50.0)
            print( проекты с прогрессом >= 50% (через чистую функцию): {[p.name for p in high_prog]}")
            total_w = functional_calculate_total_budget_or_weight(projects)
            print( суммарный вес всех задач в системе: {total_w}")
        
        elif choice == "4":
            print("\n[Функциональный конвейер с замыканием]")
            pipeline_res = functional_pipeline_analysis(projects, max_days=12, min_progress=60.0)
            for res in pipeline_res:
                print("  >", res)
        
        elif choice == "5":
            print("\n[Сравнение парадигм]")
            print("1. Императивный подход: оперирует примитивными структурами (словарями/списками), мутирует состояние напрямую через циклы for и условия if. Требует ручного контроля индексов.")
            print("2. ООП и Полиморфизм: инкапсулирует данные внутрь классов (Project, Task), а выбор алгоритма расчета прогресса (SimpleProgress vs WeightedProgress) инкапсулирован через общий интерфейс (ProgressPolicy), что упрощает расширение системы.")
        
        elif choice == "6":
            print("Завершение работы программы. До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 6.")


if __name__ == "__main__":
    main()