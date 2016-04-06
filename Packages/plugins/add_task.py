import sublime_plugin
import sublime
import utils

class AddTaskCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("task_list", {"agregar":True, "project":True})

class ShowTasksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("task_list", {"mostrar":True, "project":True})