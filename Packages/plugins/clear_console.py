import sublime_plugin
import sublime
import utils

class ClearConsoleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("\n"*100)
          