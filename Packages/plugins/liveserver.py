import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen


class LiveServerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        comando="live-server --port=4444"
        view.run_command("ejecutar_comando_global", {"comando":comando})