
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen

class GitPushSublimePackagesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("ejecutar_comando", {"comando":'git push https://programadorsito:alejandromagno1~github.com/programadorsito/Packages^'})
