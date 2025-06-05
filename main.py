from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ListProperty
from task_manager import TaskManager

Builder.load_file("ui.kv")

class TaskScreen(Screen):
    def on_enter(self):
        self.ids.task_box.clear_widgets()
        app = App.get_running_app()
        app.task_manager.load_tasks(self)

class TaskApp(App):
    light_theme = BooleanProperty(True)
    text_color = ListProperty([0, 0, 0, 1])  # Default to black

    def build(self):
        self.title = "Task List App"
        self.task_manager = TaskManager()

        # Start in light mode with background #EAE4D5
        self.light_theme = True
        Window.clearcolor = (0.916, 0.894, 0.835, 1)  # Light beige background
        self.text_color = [0, 0, 0, 1]                # Black text

        sm = ScreenManager()
        sm.add_widget(TaskScreen(name="tasks"))
        return sm

    def toggle_theme(self, state):
        if state == "down":  # Dark mode
            self.light_theme = False
            Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background
            self.text_color = [1, 1, 1, 1]           # White text
        else:  # Light mode
            self.light_theme = True
            Window.clearcolor = (0.916, 0.894, 0.835, 1)  # Light beige background
            self.text_color = [0, 0, 0, 1]                 # Black text

        # Refresh current screen to update colors
        if self.root and self.root.current_screen:
            self.root.current_screen.on_enter()

    def get_text_color(self):
        return (0, 0, 0, 1) if self.light_theme else (1, 1, 1, 1)

if __name__ == "__main__":
    TaskApp().run()
