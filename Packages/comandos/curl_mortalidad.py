
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen

class CurlMortalidadCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("ejecutar_comando", {"comando":'curl -H "Authorization: Bearer #token" http://172.20.28.141:8484/accreditationProced/mortality/findDeceasedPatient -d "hclinica=@Historia&typeId=''&id=''&fechaIni=''&fechaFin=''" > $filepath '})
