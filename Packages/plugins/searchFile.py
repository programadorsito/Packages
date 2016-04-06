import utils
import sublime_plugin
import os
import sublime

class SearchFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        if not window.folders():return
        folder=window.folders()[0]
        view=window.active_view()
        self.lista=[]
        self.lista=utils.get_files({"ignores":["target", "build", ".svn", ".git", "bin"]})
        self.Clista=[[os.path.basename(l), l] for l in self.lista]
        window.show_quick_panel(self.Clista, self.abrir)

    def abrir(self, index):
        if index==-1:return
        window=sublime.active_window()
        view=window.open_file(self.lista[index])