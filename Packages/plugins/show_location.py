import sublime_plugin
import sublime
import utils
import os

class ShowLocationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        os.system("start "+utils.get_filedir())
          