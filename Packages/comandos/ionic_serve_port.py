
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen

class IonicServePortCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("ejecutar_comando", {"comando":'ionic serve -p @port'})
