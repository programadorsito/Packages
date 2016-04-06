
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen

class CurlOauthTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("ejecutar_comando", {"comando":'curl -H "Authorization: Basic Y2xpZW50YXBwOjEyMzQ1Ng==" http://172.20.28.141:8282/accreditation/oauth/token -d "grant_type=client_credentials" > $filepath '})
