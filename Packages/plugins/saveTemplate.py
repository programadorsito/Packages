import os
import utils
import sublime
import sublime_plugin

TEMPLATES_PATH="d:/sublime3/data/templates/"

class SaveTemplateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.langs=os.listdir(TEMPLATES_PATH)
        window=sublime.active_window()
        window.show_quick_panel(self.langs,self.seleccionarLenguaje)

    def seleccionarLenguaje(self, index):
        if index==-1:return
        self.langFolder=self.langs[index]
        window=sublime.active_window()
        name=utils.get_filename()
        window.show_input_panel("name", name, self.guardar, None, None)

    def guardar(self, name):
        rutaTemplate=os.path.join(TEMPLATES_PATH,self.langFolder,name)
        utils.file_write(rutaTemplate, utils.get_text())

