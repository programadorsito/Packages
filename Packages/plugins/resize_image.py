import re, os
import utils
import sublime_plugin
import sublime

class ResizeImageCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        images=utils.get_files({"ext":"png", "ignores":["target"]})
        self.items=[[os.path.basename(i),i] for i in images]
        window.show_quick_panel(self.items, self.seleccionar_imagen)
        
    def seleccionar_imagen(self, index):
        if index==-1:return
        self.source=self.items[index][1]
        window=sublime.active_window()
        window.show_input_panel("size", "", self.resize, None, None)

    def resize(self, size):
        window=sublime.active_window()
        view=window.active_view()
        source=self.source
        sourcedir=os.path.dirname(source)
        sourcename=os.path.basename(source)
        sourcebasename=sourcename[:sourcename.rfind(".")]
        sourceext=sourcename[sourcename.rfind(".")+1:]
        targetname=re.sub("_[\d]+", "", sourcebasename)+"_"+size+"."+sourceext
        targetpath=sourcedir+os.sep+targetname
        params={"size":size, "source":source, "target":targetpath}
        view.run_command("ejecutar_comando", {"comando":'python D:/sublime3/Data/python/resize_image.py %(size)s "%(source)s" "%(target)s"'%params})

class InverseImageCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        images=utils.get_files({"ext":"png", "ignores":["target"]})
        self.items=[[os.path.basename(i),i] for i in images]
        window.show_quick_panel(self.items, self.seleccionar_imagen)
        
    def seleccionar_imagen(self, index):
        if index==-1:return
        self.source=self.items[index][1]
        window=sublime.active_window()
        view=window.active_view()
        source=self.source
        sourcedir=os.path.dirname(source)
        sourcename=os.path.basename(source)
        sourcebasename=sourcename[:sourcename.rfind(".")]
        sourceext=sourcename[sourcename.rfind(".")+1:]
        targetname=re.sub("_[\d]+", "", sourcebasename)+"_inverse."+sourceext
        targetpath=sourcedir+os.sep+targetname
        params={"source":source, "target":targetpath}
        view.run_command("ejecutar_comando", {"comando":'python D:/sublime3/Data/python/inverse_image.py "%(source)s" "%(target)s"'%params})