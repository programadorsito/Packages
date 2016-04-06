import sublime
import sublime_plugin

class JavaCleanCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("clean_compare_files")