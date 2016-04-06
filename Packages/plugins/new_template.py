import sublime_plugin
import sublime
import utils

TEMPLATES_PATH="D:/sublime3/Data/plantillas/"
class NewTemplateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        window.show_input_panel("Nombre", "", self.guardar, None, None)

    def guardar(self, nombre):
        if not nombre:return
        ext=utils.get_fileext()
        if not ext:ext=utils.get_ext()
        nombre=nombre.replace(" ", "_")
        text=utils.get_text()
        text=text.replace("$", "\$");
        utils.file_write(TEMPLATES_PATH+nombre+"."+ext, text)