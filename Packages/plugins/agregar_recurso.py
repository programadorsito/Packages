import utils
import sublime_plugin
import sublime
import shutil
import os


class AgregarRecursoCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):    
        if not args.get("folder"):return
        self.folder=args.get("folder")
        self.resources_folder=os.path.normpath(sublime.packages_path()+os.sep+".."+os.sep+"recursos")
        self.files=utils.get_files({"folder":self.resources_folder})
        self.nombres=[[os.path.basename(x), os.path.basename(os.path.dirname(x))] for x in self.files]
        window=sublime.active_window()
        window.show_quick_panel(self.nombres,self.utilizar)
        print(self.nombres)

    def utilizar(self, index):
        if index==-1:return
        shutil.copyfile(self.files[index], self.folder+os.sep+os.path.basename(self.files[index]))

class AgregarRecursoEnLocalCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        folder=os.path.dirname(view.file_name())
        view.run_command("agregar_recurso", {"folder":folder})
