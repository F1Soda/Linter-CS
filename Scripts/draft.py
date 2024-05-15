import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Раскрывающийся список")

# Список с вариантами выбора
options = ["default", "true", "false"]

# Функция для обработки выбора из списка
def on_select(event):
    selected_option = combo.get()
    print(selected_option)

# Создание и размещение Combobox на окне
combo = ttk.Combobox(root, values=options)
combo.pack()

# Привязка функции к событию выбора из списка
combo.bind("<<ComboboxSelected>>", on_select)

root.mainloop()
