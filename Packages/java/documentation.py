import os.path
import os
import sublime
import sublime_plugin
import threading
import re

class CopyAllDocumentationCommand(sublime_plugin.TextCommand):
    """Toma toda la documentacion de un proyecto y la implanta en otro proyecto con las mismas clases"""
    def run(self, edit):
        CopyAllDocumentationThread().start()

class CopyAllDocumentationThread(threading.Thread):
    def run(self):
        windows=sublime.windows()
        if len(windows)==1:
            sublime.status_message("No hay otro proyecto al cual dirigir la documentacion")
            return 
        window=sublime.active_window()
        windows.remove(window)
        self.folder=window.folders()[0]
        windowsForCopy=[]
        self.projects=[]
        for win in windows:
            if len(win.folders())==0:continue
            self.projects.append(win.folders()[0])
        window.show_quick_panel(self.projects, self.seleccionar)

    def seleccionar(self, opcion):
        if opcion==-1:return
        self.to=self.projects[opcion]
        self.madeCopy()

    def madeCopy(self):
        """Made the copy of documentation from one path to another"""
#        print("la carpeta de origen es : "+self.folder)
#        print("la carpeta de llegada es : "+self.to)
        listaClasesDocumentadas=self.getAllJavaClasses(self.folder)
        listaClasesNoDocumentadas=self.getAllJavaClasses(self.to)
#        print(listaClasesDocumentadas)
        self.listaClases={}
        for clase in listaClasesDocumentadas:
            for clasePorDocumentar in listaClasesNoDocumentadas:
                if self.equals(clase, clasePorDocumentar):
                    self.listaClases[clase]=clasePorDocumentar
#        print(self.listaClases)
        for item in self.listaClases.items():
            self.copyDocClass(item[0], item[1])
        sublime.status_message("Proyecto documentado!!")


    def getAllJavaClasses(self, path):
        """Get all java classes tha exists in the path"""
        self.listaClases=[]
        self.getJavaClasses(path)
        return self.listaClases

    def getJavaClasses(self, path):
        """if path is a dir then try to get all java classes from this path or if path is a java class then add to the lsit"""
        if os.path.isfile(path):
            if path.endswith(".java"):
                self.listaClases.append(path)
        else:
            for pathFile in os.listdir(path):
                self.getJavaClasses(os.path.join(path, pathFile))

    def equals(self, path1, path2):
        """Compare if two classes are in the same package in differents paths"""
        return os.path.basename(os.path.dirname(path1))+os.sep+os.path.basename(path1) == os.path.basename(os.path.dirname(path2))+os.sep+os.path.basename(path2)

    def copyDocClass(self, path1, path2):
        """Copy all documentation from one file to another"""
        comentario=""
        comentarioLargo=False
        metodos={}
        for linea in open(path1).readlines():
            line=linea.strip()
            if comentarioLargo:
                if line.endswith("*/"):comentarioLargo=False
                comentario+=linea
            elif line.startswith("/*") and line.endswith("*/"):
                comentario=linea
            elif line.startswith("/*"):
                comentario=linea
                comentarioLargo=True
            elif line.startswith("//"):
                comentario=linea
            else:
                if not comentario or not line:continue
                if len(line.replace(" ", ""))<2:continue
                metodos[line.replace(" ", "")]=comentario
                comentario=""
        archivo=open(path2)
        contentFile=""
        for linea in archivo.readlines():
            line=linea.strip().replace(" ", "")
            if line in metodos.keys():
                contentFile+="\n"+metodos[line]
            contentFile+=linea
        archivo.close()
        archivo=open(path2, "w")
        archivo.write(contentFile)
#        print(contentFile)
        archivo.close()