import os
import sublime
import sublime_plugin
import codecs

class ReemplazarCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        ruta=window.folders()[0]
        window.show_input_panel("find:", "", self.buscar,None, None)

    def buscar(self, texto):
        window=sublime.active_window()
        window.show_input_panel("replace by:", texto, self.reemplazar, None, None)

    def reemplazar(self):
        pass
        window=sublime.active_window()
        for archivo in self.l:
            if codecs.open(archivo, mode='r', encoding="utf-8").read().find(texto):
                window.open_file(archivo)

    def get_files_base(self, ruta):
        if os.path.isdir(ruta):
            for subruta in os.listdir(ruta):
                self.get_files_base(os.path.join(ruta, subruta))
        else:
            if os.path.getsize(ruta)/1000<800:
                self.l.append(ruta)
                print(ruta)

    def get_files(self, args=None):
        window=sublime.active_window()
        folder=None
        window=sublime.active_window()
        folder=window.folders()[0]
        self.l=[]
        if folder==None:return self.l
        self.get_files_base(folder)
        return self.l