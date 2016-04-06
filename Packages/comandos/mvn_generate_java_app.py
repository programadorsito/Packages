
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen

class MvnGenerateJavaAppCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("ejecutar_comando", {"comando":'mvn archetype:generate -DgroupId=@paquete -DartifactId=@AppName -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false ^'})
