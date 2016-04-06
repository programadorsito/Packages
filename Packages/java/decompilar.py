import os.path
import re
import os
import sublime
import sublime_plugin
import threading
from subprocess import Popen, PIPE, call

class DecompileClassesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        HiloDecompileClasses().start()

class HiloDecompileClasses(threading.Thread):
    def run(self):
        sublime.status_message("comando descompilar clases")
        window=sublime.active_window()
        self.lista=[]
        if window.folders()!=None and len(window.folders())>=1:
            carpeta=window.folders()[0]
            self.decompilar(carpeta)
            total=len(self.lista)
            totalDecompilados=0
            for ruta in self.lista:
                comando="java -jar d:/decompiler.jar %s"%(ruta)
                proceso=Popen(comando, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
                salida=proceso.communicate()[0].decode("utf-8")
                pathJava=ruta[:-5]+"java"
                f=open(pathJava, "w")
                f.write("""/**
* Clase descompilada
*/
""")
                salida=re.sub(r"\bfinal\b", "", salida)
                salida=re.sub("\(Throwable\)", "", salida)
                f.write(salida)
                f.close()
                totalDecompilados+=1
                sublime.status_message("%.2f"%((totalDecompilados/total)*100)+"%")
            sublime.status_message("finalizado!!")

    def decompilar(self, carpeta):
        for ruta in os.listdir(carpeta):
            ruta=os.path.join(carpeta, ruta)
            if not os.path.isfile(ruta):
                self.decompilar(ruta)
            elif ruta.endswith(".class"):
                self.lista.append(ruta)