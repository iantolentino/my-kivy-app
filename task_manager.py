import os
import json
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
from excel_handler import save_tasks_to_excel, save_task_done_time

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")

class TaskManager:
    data = {"lists": []}

    @classmethod
    def load_data(cls):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                cls.data = json.load(f)
        else:
            cls.data = {"lists": []}

    @classmethod
    def save_data(cls):
        with open(DATA_FILE, "w") as f:
            json.dump(cls.data, f, indent=4)

    @classmethod
    def load_tasks(cls, screen):
        cls.load_data()
        layout = screen.ids.task_box
        layout.clear_widgets()
        app = App.get_running_app()
        text_color = app.get_text_color()

        for i, task_list in enumerate(cls.data["lists"]):
            # Header row with list name, expand/collapse button, and delete button
            header = BoxLayout(size_hint_y=None, height=40)
            label = Label(text=task_list["name"], bold=True, font_size=20)
            label.color = text_color

            toggle_btn = Button(text="-" if task_list.get("expanded", True) else "+", size_hint_x=None, width=40)
            def toggle_expansion(instance, index=i):
                cls.toggle_list_expanded(index)
                screen.on_enter()
            toggle_btn.bind(on_release=toggle_expansion)

            delete_btn = Button(text="Delete", size_hint_x=None, width=70, background_color=(1, 0, 0, 1))
            def delete_list(instance, index=i):
                cls.delete_list_by_index(index)
                screen.on_enter()
            delete_btn.bind(on_release=delete_list)

            header.add_widget(label)
            header.add_widget(toggle_btn)
            header.add_widget(delete_btn)
            layout.add_widget(header)

            # Tasks container (only if expanded)
            if task_list.get("expanded", True):
                for task in task_list["tasks"]:
                    row = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
                    checkbox = CheckBox(active=task.get("done", False))
                    def on_checkbox_active(cb, value, list_index=i, task_name=task["name"]):
                        cls.set_task_done(list_index, task_name, value)
                    checkbox.bind(active=on_checkbox_active)
                    label = Label(text=task["name"])
                    label.color = text_color
                    row.add_widget(checkbox)
                    row.add_widget(label)
                    layout.add_widget(row)

                # Input row to add new task to this list
                input_row = BoxLayout(size_hint_y=None, height=40)
                task_input = TextInput(hint_text=f"Add task to {task_list['name']}")
                add_button = Button(text="+", size_hint_x=None, width=40)
                def add_task(instance, list_index=i, inp=task_input):
                    cls.add_task_to_list_by_index(list_index, inp.text)
                    inp.text = ""
                    screen.on_enter()
                add_button.bind(on_release=add_task)
                input_row.add_widget(task_input)
                input_row.add_widget(add_button)
                layout.add_widget(input_row)

    @classmethod
    def toggle_list_expanded(cls, index):
        cls.data["lists"][index]["expanded"] = not cls.data["lists"][index].get("expanded", True)
        cls.save_data()

    @classmethod
    def add_new_list(cls, name, is_daily):
        if name and all(lst["name"] != name for lst in cls.data["lists"]):
            cls.data["lists"].append({
                "name": name,
                "daily": is_daily,
                "expanded": True,
                "tasks": []
            })
            cls.save_data()

    @classmethod
    def add_task_to_list_by_index(cls, list_index, task_name):
        if task_name.strip():
            cls.data["lists"][list_index]["tasks"].append({"name": task_name.strip(), "done": False})
            cls.save_data()

    @classmethod
    def set_task_done(cls, list_index, task_name, done):
        for task in cls.data["lists"][list_index]["tasks"]:
            if task["name"] == task_name:
                task["done"] = done
                cls.save_data()

                if done:
                    now = datetime.now()
                    save_task_done_time(cls.data["lists"][list_index]["name"], task_name, now)

                break

    @classmethod
    def save_daily_tasks(cls):
        today = datetime.now().strftime("%Y-%m-%d")
        for task_list in cls.data["lists"]:
            if task_list.get("daily"):
                tasks_to_save = [task["name"] for task in task_list["tasks"]]
                save_tasks_to_excel(task_list["name"], today, tasks_to_save)

    @classmethod
    def delete_list_by_index(cls, index):
        if 0 <= index < len(cls.data["lists"]):
            cls.data["lists"].pop(index)
            cls.save_data()
