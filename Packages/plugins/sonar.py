import sublime_plugin
import sublime
import utils
import re

def quitCurlyAlones(text):
    return re.sub("\)\s*\n\s*\{", "){", text)

def quitarImports(text):
    for linea in text.splitlines():
        if linea.startswith("import "):
            pass

class SonarCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("entro")
        window=sublime.active_window()
        view=window.active_view()
        text=utils.get_text()
        text=quitCurlyAlones(text)
        view.run_command("replace_all", {"text":text})



class SonarProjectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        lista=utils.get_files({"ignores":["target", "build", ".svn", ".git", "bin"], "ext":["java"]})
        for clase in lista:
            self.aplicarSonar(clase)

    def aplicarSonar(ruta):
        text=utils.file_read(ruta)
        text=quitCurlyAlones(text)
        utils.file_write(ruta, text)

                
                