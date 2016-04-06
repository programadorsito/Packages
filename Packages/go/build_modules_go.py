import sublime_plugin
import sublime
import utils
import re

GO_MODULES="D:/sublime3/Data/go/completion/"
GO_MAIN_MODULE="D:/sublime3/Data/go/go.json"
GO_API_FILE="D:/programacion/programacion/go/api/go1.txt"
REGEX_FUNCION="pkg\s+([\w/]+)\s*,\s+func\s+([\w]+\([^)]*\))"

class BuildModulesGoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        d={}
        modulos=utils.file_read(GO_API_FILE)
        lineas=modulos.splitlines()
        for linea in lineas:
            if linea:
                ocurrencias=re.findall(REGEX_FUNCION, linea, re.IGNORECASE)
                if ocurrencias:
                    paquete=ocurrencias[0][0]
                    if paquete.find("/")!=-1:paquete=paquete[paquete.find("/")+1:]
                    funcion=ocurrencias[0][1]
                    if not d.get(paquete):d[paquete]=[]
                    d[paquete].append(funcion)

        utils.save_json(GO_MAIN_MODULE, d)
        for key in d.keys():
            utils.save_json(GO_MODULES+key+".json", d[key])
