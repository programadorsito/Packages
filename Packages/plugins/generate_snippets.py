import sublime_plugin
import sublime
import utils
import os

RUTA_COMANDOS="D:/sublime3/Data/comandos/"

class GenerateSnippetsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        paquete_snippets=sublime.packages_path()+os.sep+"snippets"
        lista=[]
        for archivo in utils.get_files({"folder":paquete_snippets, "ext":"json"}):
            snip=utils.load_json(archivo)
            lista=lista + list(snip.keys())
        lista=list(set(lista))
        for snippet in lista:
            snippet=snippet.lower().replace("-", "_").replace(" ", "").replace("?", "_")
            utils.file_write(RUTA_COMANDOS+"code_"+snippet+".bat", "echo code_"+snippet+" > d:/sublime3/comando.txt")
            print(snippet)


          