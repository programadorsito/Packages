import utils
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen

class mvnExecJavaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        f=utils.File()
        name=f.package()+"."+f.clase()
        view.run_command("ejecutar_comando", {"comando":'mvn exec:java -Dexec.mainClass="'+name+'"^'})
