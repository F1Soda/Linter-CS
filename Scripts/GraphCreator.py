import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import networkx as nx
from tkinter import messagebox
import math

import numpy as np


def is_inside_circle(x, y, center, radius):
    distance = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
    return distance <= radius


class PopupWindow:
    def __init__(self, master, message, timeout=3000):  # timeout указывается в миллисекундах
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.title("Уведомление")

        self.label = tk.Label(self.top, text=message)
        self.label.pack(padx=20, pady=10)

        # Устанавливаем таймер для закрытия окна через timeout миллисекунд
        self.top.after(timeout, self.close_window)

    def close_window(self):
        self.top.destroy()


class GraphEditor:
    def __init__(self, master):
        self.name_entry_var = None
        self.name_label = None
        self.inspector_frame = None
        self.start_node_id = None
        self.pos_mouse = (0, 0)
        self.scale_factor = 1.0
        self.master = master
        self._id_abs = 0
        self.node_id_to_copy = None
        self.should_draw_edge_to_mouse = False
        self.data_same_with_name = True
        self.master.title("Графовый редактор")

        self.selected_node_id = None
        self.selected_edge = None
        self.drag_data = {"x": 0, "y": 0}

        self.graph = nx.DiGraph(directed=True)

        self.canvas = tk.Canvas(self.master, width=800, height=800)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.add_node)

        self.canvas.bind("<Motion>", self.draw_temporary_line)

        self.header_label = tk.Label(self.inspector_frame, text="Графовый Редактор", font=("Arial", 22), pady=10)
        self.header_label.pack()

        self.export_button = tk.Button(self.master, text="Экспорт", command=self.export_graph)
        self.export_button.pack()

        self.export_button = tk.Button(self.master, text="Импорт", command=self.import_graph)
        self.export_button.pack()

        self.export_button = tk.Button(self.master, text="Создать", command=self.create_new_graph)
        self.export_button.pack()

        self.canvas.bind("<Button-3>", self.on_node_right_click)

        self.canvas.bind("<B1-Motion>", self.on_node_drag)

        self.canvas.bind("<Delete>", self._del)

        self.canvas.bind("<Control-c>", self.copy)
        self.canvas.bind("<Control-v>", self.paste)

        self.canvas.focus_set()
        self.selected_node = None
        self.right_parent_frame = tk.Frame(self.master)
        self.right_parent_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_inspector()

        self.last_opened_files = []
        with open("data/GraphCreatorData", "r") as f:
            self.current_file = f.readline()
            for line in f.readline():
                self.last_opened_files.append(line)
        if self.current_file != "":
            self.import_graph_by_path(self.current_file)
        self.create_History()
        self.master.protocol("WM_DELETE_WINDOW", self.confirm_exit)

    def confirm_exit(self):
        if self.current_file != "":
            nx.write_gml(self.graph, self.current_file)
            self.master.destroy()
            return

        response = messagebox.askyesnocancel("Предупреждение", "Хотите ли вы сохранить данные перед выходом?")
        if response is None:
            return  # Нажата кнопка "Отмена"
        elif response:
            self.save_data()  # Нажата кнопка "Да", сохраняем данные

        self.master.destroy()

    def create_new_graph(self):
        self.save_data()
        self.graph = nx.DiGraph(directed=True)
        self.current_file = ""
        self.draw_graph()

    def save_data(self):
        if self.current_file != "":
            nx.write_gml(self.graph, self.current_file)
            PopupWindow(root, f"Данные были сохранены в файл {self.current_file}", timeout=2000)
        else:
            response = messagebox.askyesnocancel("Предупреждение", "Хотите ли вы сохранить данные?")
            if response is None:
                return  # Нажата кнопка "Отмена"
            elif response:
                self.export_graph()

    def change_focus(self, event):
        if event.widget == self.canvas:
            self.canvas.focus_set()  # Установить фокус на frame2
        elif event.widget == self.inspector_frame:
            self.inspector_frame.focus_set()  # Установить фокус на frame1

    def display_mouse_position(self):
        x, y = root.winfo_pointerxy()  # Получаем координаты мыши на экране
        x = int(x - root.winfo_rootx() / 2 - self.canvas.winfo_rootx() / 2)  # Переводим в координаты холста
        y = int(y - root.winfo_rooty() / 2 - self.canvas.winfo_rooty() / 2)

        # Очищаем старый текст на холсте
        self.canvas.delete("text")

        # Отображаем текущие координаты мыши
        self.canvas.create_text(x, y + 30, text=f"({x}, {y})", tag="text", fill="black", font="Arial 10")

    def update_mouse_position(self):
        self.display_mouse_position()
        root.after(10, self.update_mouse_position)

    def _del(self, event):
        if self.selected_node_id:
            self.delete_node(self.selected_node_id)
            self.update_inspector()

    def copy(self, event):
        if self.selected_node_id:
            self.node_id_to_copy = self.selected_node_id

    def paste(self, event):
        if self.node_id_to_copy:
            node_id = len(self.graph.nodes) + 1
            node = self.graph.nodes[self.selected_node_id]
            name = node["name"] + str(node_id)
            pos = node["pos"]
            should_check = node[" should_check_offset"]
            self.graph.add_node(node_id, pos=(pos[0] + 40, pos[1] + 40), name=name, data=name,
                                should_check_offset=should_check)

            self.selected_node_id = node_id
            self.update_inspector()

            self.draw_graph()

    def create_inspector(self):
        self.inspector_frame = tk.Frame(self.right_parent_frame, width=200, height=200)
        self.inspector_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.header_label = tk.Label(self.inspector_frame, text="Инспектор", font=("Arial", 18), pady=10)
        self.header_label.pack()

        self.header_label = tk.Label(self.inspector_frame, text="Вершина", font=("Arial", 13), pady=2)
        self.header_label.pack()

        self.name_label = tk.Label(self.inspector_frame, text="Имя вершины:")
        self.name_label.pack()

        self.name_entry_var = tk.StringVar()
        self.name_entry = tk.Entry(self.inspector_frame, textvariable=self.name_entry_var)
        self.name_entry.pack()
        self.name_entry.bind("<KeyRelease>", self.on_change_in_inspector_field_name)

        self.token_value_label = tk.Label(self.inspector_frame, text="Значение токена")
        self.token_value_label.pack()

        self.token_value_entry_var = tk.StringVar()
        self.token_value_entry = tk.Entry(self.inspector_frame, textvariable=self.token_value_entry_var)
        self.token_value_entry.bind("<KeyRelease>", self.on_change_in_inspector_field_data)
        self.token_value_entry.pack()

        self.should_check_offset_label = tk.Label(self.inspector_frame, text="проводить проверку отступов?")
        self.should_check_offset_label.pack()

        options = options = ["default", "true", "false"]
        self.should_check_offset_combo = ttk.Combobox(self.inspector_frame, values=options)
        self.should_check_offset_combo.pack()

        def on_select_should_check_offset_combo(event):
            selected_option = self.should_check_offset_combo.get()
            self.graph.nodes[self.selected_node_id]["should_check_offset"] = selected_option

        # Привязка функции к событию выбора из списка
        self.should_check_offset_combo.bind("<<ComboboxSelected>>", on_select_should_check_offset_combo)

        tk.Label(self.inspector_frame, text="id:").pack()

        self.id_field = tk.Entry(self.inspector_frame)
        self.id_field.pack()

        self.id_field.config(state="readonly")

        self.inspector_frame.bind("<Button-1>", self.change_focus)

        self.header_label = tk.Label(self.inspector_frame, text="Ребро", font=("Arial", 13), pady=2)
        self.header_label.pack()

        self.info_edge_label = tk.Label(self.inspector_frame, text="'' → ''")
        self.info_edge_label.pack()

        self.conditional_combo = ttk.Combobox(self.inspector_frame, values=["default", "True", "False"])
        self.conditional_combo.pack()

        def on_select_conditional_combo(event):
            selected_option = self.conditional_combo.get()
            self.graph.add_edge(self.selected_edge[0], self.selected_edge[1], condition=selected_option)

        # Привязка функции к событию выбора из списка
        self.conditional_combo.bind("<<ComboboxSelected>>", on_select_conditional_combo)

    def create_History(self):
        self.history_frame = tk.Frame(self.right_parent_frame, width=200, height=200)
        self.history_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.name_label = tk.Label(self.history_frame, text="Последние графы")
        self.name_label.pack()

        listbox = tk.Listbox(self.history_frame)
        listbox.pack()
        listbox.insert(tk.END, self.current_file)
        for graph in self.last_opened_files:
            listbox.insert(tk.END, graph)

    def on_change_in_inspector_field_name(self, event):
        if self.data_same_with_name:
            value = self.name_entry_var.get()  # Получаем значение из первого поля
            self.token_value_entry_var.set(value)  # Устанавливаем значение во втором поле
        self.apply_changes()

    def on_change_in_inspector_field_data(self, event):
        self.apply_changes()

    def add_node(self, event):
        self.change_focus(event)
        x, y = event.x, event.y

        if self.should_draw_edge_to_mouse:
            found = self.find_node(event)
            if found:
                self.create_edge(found)

        for node in self.graph.nodes.items():
            pos_node = node[1]["pos"]
            if is_inside_circle(x, y, pos_node, 10):
                self.selected_node_id = node[0]
                self.selected_edge = None
                self.on_node_press(event)
                self.draw_graph()
                return

        u, v = self.find_edge(event)
        if u is not None:
            self.selected_edge = (u, v)
            self.update_inspector(edge=self.selected_edge)
            self.selected_node_id = None
            self.draw_graph()
            return

        self._id_abs += 1
        node_id = self._id_abs
        name = "Новая вершина_" + str(node_id)
        self.graph.add_node(node_id, pos=(x, y), name=name, data=name, should_check_offset="default")
        self.selected_node_id = node_id
        self.update_inspector(self.selected_node_id)

        self.draw_graph()

    def apply_changes(self):
        if self.selected_node_id:
            name = self.name_entry.get()
            data = self.token_value_entry.get()
            should_check_offset = self.should_check_offset_combo.get()

            self.graph.nodes[self.selected_node_id]["data"] = data
            self.graph.nodes[self.selected_node_id]["name"] = name
            self.graph.nodes[self.selected_node_id]["should_check_offset"] = should_check_offset
            self.draw_graph()  # Убедитесь, что вызывается перерисовка графа после изменений

    def draw_graph(self):
        self.canvas.delete("all")
        for node_id, info in self.graph.nodes.items():
            x, y = info['pos']
            radius = 10
            color = "blue"
            if node_id == self.selected_node_id:
                color = "red"
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
            self.canvas.create_text(x, y - 15, text=info['name'])  # Отображение текста с данными
        for u, v in self.graph.edges:
            color = "black"
            width = 1
            if (u, v) == self.selected_edge:
                color = "red"
                width = 2
            self.canvas.create_line(self.graph.nodes[u]['pos'][0], self.graph.nodes[u]['pos'][1],
                                    self.graph.nodes[v]['pos'][0], self.graph.nodes[v]['pos'][1], fill=color,
                                    width=width)
            to_point = self.graph.nodes[v]['pos']
            size_cube = 5
            self.canvas.create_rectangle(to_point[0] - size_cube, to_point[1] - size_cube, to_point[0] + size_cube,
                                         to_point[1] + size_cube, fill="green")
        if self.selected_node_id in self.graph.nodes:
            self.update_inspector(self.selected_node_id)

    def draw_temporary_line(self, event):
        if self.should_draw_edge_to_mouse:
            self.canvas.delete("arrow")
            self.canvas.create_line(self.graph.nodes[self.selected_node_id]['pos'][0],
                                    self.graph.nodes[self.selected_node_id]['pos'][1],
                                    event.x, event.y, fill="black", tags="arrow")

    def export_graph(self):
        filename = filedialog.asksaveasfilename(defaultextension=".gml", filetypes=[("GML files", "*.gml")])
        nx.write_gml(self.graph, filename)

    def import_graph(self):
        self.save_data()
        filename = filedialog.askopenfilename(defaultextension=".gml", filetypes=[("GML files", "*.gml")])
        self.import_graph_by_path(filename)

    def import_graph_by_path(self, filename):
        self.graph = nx.convert_node_labels_to_integers(nx.read_gml(filename))  # type: nx.DiGraph

        self._id_abs = len(self.graph.nodes) + 100
        self.current_file = filename
        self.draw_graph()

    def on_mousewheel(self, event):
        # Узнаем направление прокрутки колеса
        if event.delta > 0:
            self.scale_factor *= 1.1  # Увеличиваем масштаб
        else:
            self.scale_factor /= 1.1  # Уменьшаем масштаб

        # Устанавливаем новый масштаб канваса
        self.canvas.scale("all", 0, 0, self.scale_factor, self.scale_factor)

    def on_node_press(self, event):
        node_id = self.find_node(event)
        if node_id:
            self.selected_node_id = node_id
            self.drag_data["x"] = event.x - self.graph.nodes[node_id]["pos"][0]
            self.drag_data["y"] = event.y - self.graph.nodes[node_id]["pos"][1]
            self.update_inspector(node_id)

    def update_inspector(self, node_id=None, edge=None):
        self.name_entry.delete(0, tk.END)
        self.id_field.config(state="normal")
        self.id_field.delete(0, tk.END)
        self.id_field.config(state="readonly")
        self.token_value_entry.delete(0, tk.END)
        self.should_check_offset_combo.set("")
        self.conditional_combo.set("")
        self.info_edge_label.config(text="'' → ''")
        if node_id is not None:
            self.name_entry.insert(0, self.graph.nodes[node_id]["name"])
            self.token_value_entry.insert(0, self.graph.nodes[node_id]["data"])
            try:
                self.should_check_offset_combo.insert(0, self.graph.nodes[node_id]["should_check_offset"])
            except Exception:
                response = messagebox.askyesnocancel("Предупреждение",
                                                     f"Возможно в графе не установлены некоторые параметры(should_check_offset). Установить их к стандартному значению?")
                if response is None:
                    pass
                elif response:
                    for index in range(len(self.graph.nodes)):
                        self.graph.nodes[index]["should_check_offset"] = "default"
            self.id_field.config(state="normal")
            self.id_field.delete(0, tk.END)
            self.id_field.insert(0, str(node_id))
            self.id_field.config(state="readonly")
        elif edge:
            try:
                condition = self.graph[edge[0]][edge[1]]['condition']
                self.conditional_combo.insert(0, condition)
                self.info_edge_label.config(text=f"'{self.graph.nodes[edge[0]]['name']}' → '{self.graph.nodes[edge[1]]['name']}'")

            except Exception:
                response = messagebox.askyesnocancel("Предупреждение",
                                                     f"Возможно в графе не установлены некоторые параметры(condition). Установить их к стандартному значению?")
                if response is None:
                    pass
                elif response:
                    for source, target in self.graph.edges:
                        self.graph[source][target]['condition'] = 'default'

    def on_node_drag(self, event):
        if self.selected_node_id:
            x = event.x - self.drag_data["x"]
            y = event.y - self.drag_data["y"]
            self.graph.nodes[self.selected_node_id]["pos"] = (x, y)
            self.draw_graph()

    def on_node_release(self, event):
        self.selected_node_id = None

    def find_node(self, event):
        for node_id, info in self.graph.nodes.items():
            x, y = info["pos"]
            if is_inside_circle(event.x, event.y, (x, y), 25):
                return node_id
        return None

    def on_node_right_click(self, event):
        node_id = self.find_node(event)
        if node_id:
            # Показать контекстное меню
            self.show_context_menu_node(event, node_id)
        u, v = self.find_edge(event)
        if u:
            self.show_context_menu_edge(event, u, v)

    def find_edge(self, event):
        x, y = event.x, event.y
        for u, v in self.graph.edges:
            x1, y1 = self.graph.nodes[u]['pos'][0], self.graph.nodes[u]['pos'][1]
            x2, y2 = self.graph.nodes[v]['pos'][0], self.graph.nodes[v]['pos'][1]
            a = np.array([x1 - x2, y1 - y2])
            a = a / np.linalg.norm(a)
            n = np.array([a[1], -a[0]])
            m = np.array([a, n])
            m = np.transpose(m)
            xy1_ = m @ np.array([x1, y1])
            xy2_ = m @ np.array([x2, y2])
            pos_mouse = m @ np.array([x, y])
            threshold = 10
            if min(float(xy1_[0]), float(xy2_[0])) <= pos_mouse[0] <= max(float(xy1_[0]), float(xy2_[0])) and abs(
                    pos_mouse[1] - xy1_[1]) <= threshold:
                return u, v
        return None, None

    def show_context_menu_node(self, event, node_id):
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Удалить вершину", command=lambda: self.delete_node(node_id))
        # Добавьте другие действия, которые могут быть выполнены с вершиной
        menu.add_command(label="Создать ребро", command=lambda: self.start_creating_edge())
        menu.post(event.x_root, event.y_root)

    def show_context_menu_edge(self, event, u, v):
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Удалить ребро", command=lambda: self.delete_edge(u, v))
        menu.post(event.x_root, event.y_root)

    def start_creating_edge(self):
        self.should_draw_edge_to_mouse = True
        self.start_node_id = self.selected_node_id

    def create_edge(self, target_node_id):
        self.graph.add_edge(self.selected_node_id, target_node_id, condition="default")
        self.draw_graph()
        self.should_draw_edge_to_mouse = False

    def delete_edge(self, u, v):
        self.graph.remove_edge(u, v)
        self.draw_graph()

    def delete_node(self, node_id):
        # Удалите вершину из графа и из отображения на холсте
        self.graph.remove_node(node_id)
        self.selected_node_id = None
        self.draw_graph()


root = tk.Tk()
app = GraphEditor(root)
app.update_mouse_position()
root.mainloop()

with open("data/GraphCreatorData", "w") as file:
    file.writelines([app.current_file] + app.last_opened_files)
