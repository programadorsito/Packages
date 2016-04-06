import sublime_plugin
import sublime
import utils

class InvertLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        texto=""
        for linea in reversed(utils.get_text().splitlines())  :
            texto+=linea+"\n"
        utils.set_text(texto)