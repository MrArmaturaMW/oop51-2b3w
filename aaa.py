import tkinter as tk
import sqlite3
from datetime import datetime

# Подключение к базе данных SQLite
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Создание таблицы, если ее нет
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    completed INTEGER DEFAULT 0)''')
conn.commit()


def add_task():
    """Добавление задачи с датой и временем"""
    task_text = task_entry.get().strip()
    if task_text:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO tasks (text, created_at) VALUES (?, ?)", (task_text, created_at))
        conn.commit()
        task_entry.delete(0, tk.END)
        display_tasks()


def toggle_task(task_id):
    """Переключение статуса выполнения задачи"""
    cursor.execute("UPDATE tasks SET completed = NOT completed WHERE id = ?", (task_id,))
    conn.commit()
    display_tasks()


def delete_task(task_id):
    """Удаление задачи"""
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    display_tasks()


def display_tasks(order_by="created_at DESC"):
    """Отображение списка задач"""
    for widget in task_frame.winfo_children():
        widget.destroy()

    cursor.execute(f"SELECT * FROM tasks ORDER BY {order_by}")
    tasks = cursor.fetchall()

    for task in tasks:
        task_id, text, created_at, completed = task
        color = "green" if completed else "black"

        task_label = tk.Label(task_frame, text=f"{text} ({created_at})", fg=color, font=("Arial", 12))
        task_label.pack(anchor="w", padx=5, pady=2)

        toggle_button = tk.Button(task_frame, text="✅" if completed else "⬜",
                                  command=lambda tid=task_id: toggle_task(tid))
        toggle_button.pack(anchor="e", padx=5, pady=2)

        delete_button = tk.Button(task_frame, text="🗑", command=lambda tid=task_id: delete_task(tid))
        delete_button.pack(anchor="e", padx=5, pady=2)


def sort_by_date():
    display_tasks(order_by="created_at DESC")


def sort_by_status():
    display_tasks(order_by="completed ASC, created_at DESC")


# Создание основного окна
root = tk.Tk()
root.title("Task Manager")
root.geometry("500x400")

task_entry = tk.Entry(root, font=("Arial", 12))
task_entry.pack(pady=5)

add_button = tk.Button(root, text="Добавить задачу", command=add_task)
add_button.pack(pady=5)

sort_date_button = tk.Button(root, text="📅 Сортировать по дате", command=sort_by_date)
sort_date_button.pack(pady=5)

sort_status_button = tk.Button(root, text="✅ Сортировать по статусу", command=sort_by_status)
sort_status_button.pack(pady=5)

task_frame = tk.Frame(root)
task_frame.pack(pady=10)

display_tasks()

root.mainloop()
conn.close()
