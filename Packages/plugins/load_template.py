import threading
import sublime_plugin
import sublime
import utils
import os
import time

TEMPLATES_PATH="D:/sublime3/Data/plantillas"

class cargarPlantillaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.lista=os.listdir(TEMPLATES_PATH)
        window=sublime.active_window()
        window.show_quick_panel(self.lista,self.seleccionarPlantilla)
    
    def seleccionarPlantilla(self, index):
        if index==-1:return
        window=sublime.active_window()
        view=window.active_view()
        plantilla=self.lista[index]
        plantilla=plantilla[:plantilla.find(".")]
        view.run_command("load_template", {"nombre":plantilla})
        pass

class LoadTemplateCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        if not args.get("nombre"):return
        nombre=args.get("nombre")
        for c in os.listdir(TEMPLATES_PATH):
#            print(c)
            if nombre.lower()==c.lower()[:c.rfind(".")]:
                texto=utils.file_read(TEMPLATES_PATH+"/"+c)
                self.texto=texto
                if not utils.get_text().strip():
                    self.insertar()
                else:
#                    print("no tiene texto")
                    self.texto=texto
                    window=sublime.active_window()
                    window.show_input_panel("", c[c.rfind("."):], self.crear_archivo, None, None)


    def crear_archivo(self, nombre):
        archivo=utils.get_filedir()+os.sep+nombre
        utils.file_write(archivo, "")
        window=sublime.active_window()
        window.open_file(archivo)
        view=window.active_view()
        threading.Thread(target=self.insertar).start()

    def insertar(self):
        window=sublime.active_window()
        view=window.active_view()
        self.texto=self.procesar(self.texto)
#        print("va a insertar : "+self.texto)
        view.run_command('insert_snippet', {"contents":utils.agregarCursores(self.texto)})

    def procesar(self, texto):
        window=sublime.active_window()
        view=window.active_view()
        puntero="@"
        if texto.find("~")!=-1:puntero="~"
        d={
            "package":utils.get_file_package({"filepath":utils.get_filedir({"filepath":view.file_name()})}),
            "currentDate":time.strftime("%d/%m/%Y"),
            "filename":utils.get_filebasename()
        }
        for key in d.keys():
            if d.get(key):
                texto=texto.replace("%s%s"%(puntero, key), d[key])
        return texto
