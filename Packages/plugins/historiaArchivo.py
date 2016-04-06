import time
import utils
import sublime_plugin
import sublime
import os

HISTORIA_PATH=os.path.join("D:\\sublime3\\Data\\Packages", "..", "historia")

def cargarRutaArchivo():
    rutaArchivo=utils.get_filepath().replace(":", "")
    rutaArchivo=HISTORIA_PATH+os.sep+rutaArchivo+".json"
    carpeta=os.path.dirname(rutaArchivo)
    utils.create_json_if_not_exist(rutaArchivo)
    return rutaArchivo

def cargarHistoriaArchivo():
    rutaArchivo=cargarRutaArchivo()
    historia=utils.load_json(rutaArchivo)
    if historia==None:historia={}
    return historia

class GuardarHistoriaArchivoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        window.show_input_panel("nombre", "", self.guardar, None, None)

    def guardar(self, nombre):
        self.historia=cargarHistoriaArchivo()
        self.historia[nombre+" ("+time.strftime("%d-%m-%Y")+")"]=utils.get_text()
        utils.save_json(cargarRutaArchivo(), self.historia)

class CargarHistoriaArchivoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.historia=cargarHistoriaArchivo()
        self.tiempos=list(self.historia.keys())
        window=sublime.active_window()
        window.show_quick_panel(self.tiempos,self.seleccionar)

    def seleccionar(self, index):
        if index==-1:return
        tiempo=self.tiempos[index]
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("replace_all", {"text":self.historia[tiempo]})