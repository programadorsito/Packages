import sublime_plugin
import sublime
import utils

class CloseAllFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view.run_command("close_others_by_index",  {"group": 0, "index": 0})
        view.run_command("close_by_index",  {"group": 0, "index": 0})