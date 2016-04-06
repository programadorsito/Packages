import os
import utils
import sublime_plugin
import sublime

PROJECT_PATH="D:\\sublime3\\Data\\proyectos"

class NuevoProyectoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        folders=os.listdir(PROJECT_PATH)
        proyectos=[]
        for folder in folders:
            for proyecto in os.listdir(PROJECT_PATH+os.sep+folder):
                proyectos.append(folder+" : "+proyecto)
        self.proyectos=proyectos
        window=sublime.active_window()
        window.show_quick_panel(proyectos, self.seleccionarProyecto)

    def seleccionarProyecto(self, index):
        if index==-1:return
        proyecto=self.proyectos[index]
        if proyecto=="android:gradle":utils.set_preference("project.type", "android.gradle")
        proyecto=proyecto.replace(" : ",os.sep)
        rutaModelo=PROJECT_PATH+os.sep+proyecto
        rutaProyecto=utils.get_folder()
        print("la ruta modelo es : "+rutaModelo)
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("copiar_proyecto", {"source":os.path.normpath(rutaModelo), "target":os.path.normpath(rutaProyecto)})