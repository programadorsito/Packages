import os
import shutil
import sublime_plugin
import sublime

class CopiarProyectoCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        self.source=args["source"]
        self.target=args["target"]
        self.source=os.path.normpath(self.source)
        self.target=os.path.normpath(self.target)
        self.archivos(self.source)

    def archivos(self, ruta):
        if os.path.isdir(ruta):
            for subruta in os.listdir(ruta):
                self.archivos(ruta+os.sep+subruta)
        else:
            self.crearArchivo(ruta, self.target+os.sep+ruta[len(self.source)+1:])

    def crearArchivo(self, sourceFile, targetFile):
        sourceFile=os.path.normpath(sourceFile)
        targetFile=os.path.normpath(targetFile)
        print("se va a copiar de  : "+sourceFile+" a "+targetFile)
        if os.path.exists(targetFile):return
        if not os.path.exists(os.path.dirname(targetFile)):
            os.makedirs(os.path.dirname(targetFile))
        shutil.copyfile(sourceFile, targetFile)
