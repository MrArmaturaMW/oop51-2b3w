import tkinter as tk
from datetime import datetime

def get_greeting_and_color(name):
    """Функция возвращает приветствие и соответствующий цвет в зависимости от времени суток."""
    current_hour = datetime.now().hour

    if 6 <= current_hour < 12:
        greeting = "Доброе утро"
        color = "yellow"
    elif 12 <= current_hour < 18:
        greeting = "Добрый день"
        color = "orange"
    elif 18 <= current_hour < 24:
        greeting = "Добрый вечер"
        color = "red"
    else:
        greeting = "Доброй ночи"
        color = "blue"

    return f"{greeting}, {name}!", color

def update_greeting():
    """Функция обновляет приветствие, цвет текста и время."""
    name = name_entry.get().strip()
    if name:
        greeting_text, color = get_greeting_and_color(name)
        greeting_label.config(text=greeting_text, fg=color)  # Меняем текст и цвет
        history_label.config(text=f"История приветствий:\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — {name}")

# Создаем окно приложения
root = tk.Tk()
root.title("Моё первое приложение")
root.geometry("400x300")

# Виджеты интерфейса
greeting_label = tk.Label(root, text="Введите ваше имя", font=("Arial", 14))
greeting_label.pack(pady=10)

name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.pack(pady=5)

greet_button = tk.Button(root, text="Поздороваться снова", command=update_greeting)
greet_button.pack(pady=10)

history_label = tk.Label(root, text="История приветствий:", font=("Arial", 12))
history_label.pack(pady=10)

# Запуск приложения
root.mainloop()
