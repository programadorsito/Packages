import sublime_plugin
import sublime
import utils

class EliminarLineasRepetidasCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text=utils.get_text()
        lineas=text.splitlines()
        lineas=list(set(lineas))
        text=""
        for linea in lineas:text+=linea+"\n"
        utils.set_text(text)

                