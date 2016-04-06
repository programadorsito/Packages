
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen

class MysqldumpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("ejecutar_comando", {"comando":'mysqldump --bind-address=#mysql.host --port=#mysql.port --user=#mysql.user --password=#mysql.pass #mysql.db > @filepath'})
