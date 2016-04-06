
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen

class CurlNoposCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("ejecutar_comando", {"comando":'curl -H "Authorization: Bearer #token" http://172.20.28.141:8282/accreditation/gestion/GesNoPos -d "nHoras=@nHoras" > $filepath '})
