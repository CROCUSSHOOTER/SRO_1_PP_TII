import sqlite3

# 1. Инициализация базы данных и сидирование полного списка студентов из ведомости
def init_database():
    conn = sqlite3.connect("student_projects.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects_monitoring (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            project_title TEXT NOT NULL,
            tasks_total INTEGER NOT NULL,
            tasks_completed INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)
    
    # Проверяем, есть ли уже данные
    cursor.execute("SELECT COUNT(*) FROM projects_monitoring")
    if cursor.fetchone()[0] == 0:
        students_data = [
            # Из первого скриншота
            (1, "Абдрашитов Мухамед Абдимежитович", "AI Student Analytics", 5, 5, "Готов"),
            (2, "Амираджанов Ислам Амираджанович", "Smart Attendance Bot", 4, 2, "В процессе"),
            (3, "Ансарбоева Гульбану Абдигани кизи", "Library E-Catalog", 6, 6, "Готов"),
            (4, "Батырбеков Диас Дидарович", "Scholarship Calculator", 4, 1, "Задержан"),
            (5, "Досжан Әлижан Еркінұлы", "Lab Booking System", 5, 4, "В процессе"),
            (6, "Жусупов Айболат Шандиевич", "Система мониторинга учебных проектов", 5, 5, "Готов"),
            (7, "Керимбаева Карина Эдуардовна", "Support HelpDesk", 4, 3, "В процессе"),
            (8, "Корганбаева Хуснора Алишеровна", "Dorm Allocation", 5, 5, "Готов"),
            (9, "Мұхамеджан Бекзат Мадиярұлы", "Internship Tracker", 4, 2, "В процессе"),
            (10, "Пак Дамир Игоревич", "Exam Ticket Generator", 6, 6, "Готов"),
            (11, "Петров Сергей Викторович", "Portfolio Analyzer", 4, 1, "Задержан"),
            # Из второго скриншота
            (12, "Рәсілбек Данайя Мұратқызы", "Academic Mobility Portal", 5, 4, "В процессе"),
            (13, "Сабиржанов Муратжан Баходирович", "Course Prerequisite Checker", 4, 4, "Готов"),
            (14, "Сагаталиев Ильяс Маратович", "Course Quality Survey", 5, 2, "В процессе"),
            (15, "Сайтұлы Диас", "University Notification System", 4, 4, "Готов"),
            (16, "Серік Алишер Айбекұлы", "Equipment Inventory System", 6, 3, "Задержан"),
            (17, "Слободзян Святослав Константинович", "Teacher Consultation Platform", 5, 5, "Готов"),
            (18, "Утепов Тимур Ермекович", "Achievement Portfolio Analyzer", 4, 2, "В процессе"),
            (19, "Хаким Алишер Аркенович", "Risk Analytics Dashboard", 5, 5, "Готов"),
            (20, "Хе Валерий Андреевич", "AI Credit Scoring Monitor", 4, 4, "Готов"),
            (21, "Храменков Спиридон Дмитриевич", "Smart Timetable Scheduler", 5, 3, "В процессе"),
            (22, "Черепивский Эрик Александрович", "Student Support Chatbot", 4, 1, "Задержан")
        ]
        cursor.executemany("INSERT INTO projects_monitoring (id, student_name, project_title, tasks_total, tasks_completed, status) VALUES (?, ?, ?, ?, ?, ?)", students_data)
        
    conn.commit()
    conn.close()

# 2. ООП: Класс для описания студенческого проекта (Лекция 5)
class StudentProjectRecord:
    def __init__(self, record_id, student_name, project_title, tasks_total, tasks_completed, status):
        self._id = record_id
        self._student_name = student_name
        self._project_title = project_title
        self._tasks_total = tasks_total
        self._tasks_completed = tasks_completed
        self._status = status

    @property
    def id(self):
        return self._id

    @property
    def student_name(self):
        return self._student_name

    @property
    def project_title(self):
        return self._project_title

    @property
    def progress_percentage(self):
        if self._tasks_total == 0:
            return 0.0
        return round((self._tasks_completed / self._tasks_total) * 100.0, 2)

    @property
    def status(self):
        return self._status


# 3. Чистые функции для аналитики (Лекция 3, 7)
def calculate_average_group_progress(records):
    if not records:
        return 0.0
    total = sum(r.progress_percentage for r in records)
    return round(total / len(records), 2)

def filter_ready_projects(records):
    return [r for r in records.values() if r.status == "Готов"]


# 4. Главная точка входа (Лекция 4)
if __name__ == "__main__":
    init_database()
    
    conn = sqlite3.connect("student_projects.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects_monitoring")
    rows = cursor.fetchall()
    conn.close()
    
    # Создаем словарь объектов по ID
    records_dict = {}
    for r in rows:
        rec = StudentProjectRecord(r[0], r[1], r[2], r[3], r[4], r[5])
        records_dict[r[0]] = rec
        
    avg_prog = calculate_average_group_progress(list(records_dict.values()))
    
    print("==================================================================")
    print("          СИСТЕМА МОНИТОРИНГА УЧЕБНЫХ ПРОЕКТОВ ГРУППЫ             ")
    print("==================================================================")
    
    for r_id, rec in records_dict.items():
        icon = "✅" if rec.status == "Готов" else ("⏳" if rec.status == "В процессе" else "⚠️")
        print(f"ID: {r_id:2d} | Студент: {rec.student_name}")
        print(f"        | Проект: {rec.project_title}")
        print(f"        | Прогресс: {rec.progress_percentage}% ({rec.status}) {icon}")
        print("-" * 66)
        
    print(f"\nОбщий средний показатель готовности группы: {avg_prog}%")
    print(f"Количество завершенных проектов: {len(filter_ready_projects(records_dict))} из {len(records_dict)}")