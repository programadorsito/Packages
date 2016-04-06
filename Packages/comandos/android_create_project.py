import utils
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen

class AndroidCreateProjectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        utils.set_preference("project.type", "android")
        view.run_command("ejecutar_comando", {"comando":"android create project --target @target --name @AppName --path $dirpath --activity @MainActivity --package @package"})
