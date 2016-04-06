import sublime_plugin
import sublime
import utils
import os

class NextFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        carpeta=utils.get_filedir()
        archivo=utils.get_filename()
        archivos=sorted(os.listdir(carpeta))
        i=0
        for arc in archivos:
            if arc == archivo:
                i+=1
                break
            i+=1
        nuevo_archivo=archivos[i]
        window=sublime.active_window()
        window.open_file(carpeta+os.sep+nuevo_archivo)

class BackFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        carpeta=utils.get_filedir()
        archivo=utils.get_filename()
        archivos=sorted(os.listdir(carpeta))
        i=0
        for arc in archivos:
            if arc == archivo:
                i-=1
                break
            i+=1
        nuevo_archivo=archivos[i]
        window=sublime.active_window()
        window.open_file(carpeta+os.sep+nuevo_archivo)
