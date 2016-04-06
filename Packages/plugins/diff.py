import difflib
import shutil
import filecmp
import threading
import sublime_plugin
import sublime
import utils
import time
import re
import os

DIFF_PATH="/Users/Mac/aplicaciones/diff"
DIFF_JSON="/Users/Mac/aplicaciones/diff/diff.json"

def diff(texto1, texto2):
    pass

def get_folder(filename):
    carpeta=os.path.dirname(filename)
    nombre=os.path.basename(filename)
    rutaCarpeta=DIFF_PATH+os.sep+carpeta.replace(":", "")+os.sep+nombre.replace(".", os.sep)
    return rutaCarpeta

def cambiar_version(cambio=1, mostrar=False):
    diff=utils.load_json(DIFF_JSON)
    window=sublime.active_window()
    view=window.active_view()
    filename=view.file_name()
    folder=get_folder(filename)
    actual=diff[view.file_name()]
    viejo=actual
    lista=os.listdir(folder)
    lista=sorted(lista)
    i=lista.index(actual)
    i+=cambio
    if i<0 or i==len(lista):return
    actual=lista[i]
    diff[filename]=actual
    utils.save_json(DIFF_JSON, diff)
    lines=view.lines(sublime.Region(0, view.size()))
    folder=get_folder(filename)
#    self.view.add_regions("diferentes", self.lista, "comment", "bookmark", sublime.DRAW_OUTLINED)
    if not mostrar:utils.set_text(open(get_folder(filename)+os.sep+actual).read())

    print("\n")
    with open(folder+os.sep+actual, 'r') as one:
        with open(folder+os.sep+viejo, 'r') as two:
            diff = difflib.unified_diff(one.readlines(),two.readlines())
            for line in diff:
                line=line.strip()
                if line.startswith("@@ -"):
#                    line=line[4, line.find(",")]
#                    print(line)
                    utils.go_line(int(line[4:line.find(",")])+3)
                if line.startswith("-") or line.startswith("+") or line.startswith("@@"):
                    print(line.strip()+":")
    print("\n")


class ViewAllVersionsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        diff=utils.load_json(DIFF_JSON)


class ViewPrevVersionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        cambiar_version(-1, False)

class ViewNextVersionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        cambiar_version(1, False)

class PrevVersionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        cambiar_version(-1, True)

class NextVersionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        cambiar_version(1, True)

class DiffListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        SaveFileThread().start()      

class SaveFileThread(threading.Thread):
    def run(self):
        jsonDiff=utils.load_json(DIFF_JSON)
        window=sublime.active_window()
        view=window.active_view()
        text=utils.get_text()
        filename=view.file_name()
        rutaCarpeta=get_folder(filename)
        utils.create_folder_if_not_exist(rutaCarpeta)
        nombreArchivo=time.strftime("%Y%m%d%H%M%S")
        lista=os.listdir(rutaCarpeta)
        escribir=True
        if lista:
            ultimo=max(lista)
            if filecmp.cmp(rutaCarpeta+os.sep+ultimo, filename):escribir=False
        if escribir:
            print("guardando version...")
            rutaArchivo=rutaCarpeta+os.sep+nombreArchivo
            shutil.copyfile(filename, rutaArchivo)
            jsonDiff[filename]=nombreArchivo
            utils.save_json(DIFF_JSON, jsonDiff)
