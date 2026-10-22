import sqlite3

# 1. Функция для создания базы данных и добавления проектов студентов
def init_database():
    conn = sqlite3.connect("project.db")
    cursor = conn.cursor()
    
    # Создаем таблицу студентов и проектов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            project_title TEXT,
            completed INTEGER
        )
    """)
    
    # Если таблица пустая, добавляем данные студентов
    cursor.execute("SELECT COUNT(*) FROM student_projects")
    if cursor.fetchone()[0] == 0:
        student_data = [
            ("Хе Валерий", "Аналитическая система успеваемости", 1),      # 1 - готово
            ("Пак Дамир", "Система контроля посещаемости", 0),           # 0 - не готово
            ("Жусупов Айболат", "Система мониторинга учебных проектов", 1), # 1 - готово
            ("Черепивский Эрик", "Электронная библиотека университета", 0) # 0 - не готово
        ]
        cursor.executemany("INSERT INTO student_projects (student_name, project_title, completed) VALUES (?, ?, ?)", student_data)
        
    conn.commit()
    conn.close()

# 2. ООП: Класс для описания проекта студента (Лекция 5)
class StudentProject:
    def __init__(self, student_name, project_title, completed):
        self.student_name = student_name
        self.project_title = project_title
        self.completed = completed

# 3. Чистая функция для подсчета процента готовых проектов (Лекция 3, 7)
def calculate_group_progress(projects):
    if not projects:
        return 0.0
    completed_count = sum(1 for p in projects if p.completed == 1)
    progress = (completed_count / len(projects)) * 100
    return round(progress, 2)

# 4. Главная точка входа (Лекция 4)
if __name__ == "__main__":
    # Шаг 1: Инициализируем базу данных
    init_database()
    
    # Шаг 2: Загружаем данные из базы
    conn = sqlite3.connect("project.db")
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, project_title, completed FROM student_projects")
    rows = cursor.fetchall()
    conn.close()
    
    # Шаг 3: Превращаем строки из базы в объекты класса StudentProject
    projects_list = [StudentProject(row[0], row[1], row[2]) for row in rows]
    
    # Шаг 4: Считаем общий прогресс группы
    group_progress = calculate_group_progress(projects_list)
    
    # Шаг 5: Выводим результаты в консоль
    print("==================================================")
    print("   МОНИТОРИНГ УЧЕБНЫХ ПРОЕКТОВ СТУДЕНТОВ (АТО)     ")
    print("==================================================")
    for p in projects_list:
        status_text = "✅ Готов" if p.completed == 1 else "⏳ Не готов"
        print(f"Студент: {p.student_name}")
        print(f"  -> Проект: {p.project_title}")
        print(f"  -> Статус: {status_text}\n")
        
    print("==================================================")
    print(f"Общий процент готовности проектов группы: {group_progress}%")