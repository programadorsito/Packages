import re
import os
import sublime_plugin
import sublime
import utils

RUTA_COMANDOS="D:/sublime3/Data/comandos/"
RUTA_PLANTILLAS="D:/sublime3/Data/plantillas"


class PrepareCommandsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        paquete_snippets=sublime.packages_path()+os.sep+"snippets"
        lista=[]
        comandos=[]
        for archivo in utils.get_files({"folder":paquete_snippets, "ext":"json"}):
            snip=utils.load_json(archivo)
            lista=lista + list(snip.keys())
        lista=list(set(lista))
        for snippet in lista:
            snippet=snippet.lower().replace("-", "_").replace("(", "").replace(")", "").replace(" ", "").replace("?", "").replace(":", "")
            utils.file_write(RUTA_COMANDOS+"code_"+snippet+".bat", "echo code_"+snippet+" > d:/sublime3/comando.txt")
            comandos.append("code_"+snippet)
        archivos_plantillas=utils.get_files({"folder":RUTA_PLANTILLAS})
        for plantilla in archivos_plantillas:
            plantilla=os.path.basename(plantilla)
            if plantilla.rfind(".")!=-1:plantilla=plantilla[:plantilla.rfind(".")]
            plantilla=plantilla.replace(" ", "_").lower()
            utils.file_write(RUTA_COMANDOS+"make_"+plantilla+".bat", "echo make_"+plantilla+" > d:/sublime3/comando.txt")
            comandos.append("make_"+plantilla)
        archivos_python=utils.get_files({"folder":sublime.packages_path(), "ext":".py"})
        for programa in archivos_python:
            rutaPrograma=programa
            try:programa=utils.file_read(programa)
            except:
                print("saco error al leer : "+rutaPrograma)
                continue
            comandosPython=re.findall("class ([\w]+)\(sublime_plugin.TextCommand\)",programa, re.IGNORECASE)
            for comandoPython in comandosPython:
                comandoPython=comandoPython[0].lower()+comandoPython[1:]
                cp=""
                for c in comandoPython:
                    if c.isupper():cp+="_"
                    cp+=c.lower()
                if cp.endswith("_command"):cp=cp.replace("_command", "")
                comandos.append(cp)
        comandosInternos=utils.file_read("D:/sublime3/Data/Packages/User/Default (Windows).sublime-keymap")
        comandosInternos=re.findall('"command": *"(\w+)" *\}', comandosInternos, re.IGNORECASE)
        for comandoInterno in comandosInternos:comandos.append(comandoInterno)
        comandos=sorted(list(set(comandos)))
        strComandos=""
        for comando in comandos:strComandos+=comando+"\n"

        window=sublime.active_window()
        view=window.active_view()
        utils.file_write("d:/sublime3/comandos.txt", strComandos)
        view.run_command("ejecutar_comando", {"comando":"taskkill /f /im CustomizeableJarvis.exe\njarvis\nexit"})
        