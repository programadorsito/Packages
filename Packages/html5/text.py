import sublime_plugin
import sublime
import utils

class TestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        for x in view.find_all("\d+"):
            print(view.substr(x))
            
          