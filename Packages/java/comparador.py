import codecs
import re
import utils
import os
import sublime
import sublime_plugin

class CompareFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        self.file=view.file_name()
        self.lista=[]
        for window in sublime.windows():
            for view in window.views():
                filename=view.file_name()
                if filename:
                    self.lista.append(filename)
        self.lista.remove(view.file_name())

        if len(self.lista)==1:
            self.diff(self.lista[0])
        elif len(self.lista)>1:
            window.show_quick_panel(self.lista, self.seleccionar)


    def seleccionar(self, opcion):
        if opcion==-1:return
        archivo=self.lista[opcion]
        self.diff(archivo)
    
    def diff(self, archivo):    
        lines=self.view.lines(sublime.Region(0, self.view.size()))
        lineas=open(archivo, "").readlines()
        self.lista=[]
        puntos=[]
        i=0
        for line in lines:
            i+=1
            linea=self.view.substr(line)
            if linea.strip()=="}":continue
            if not linea+"\n" in lineas:
                self.lista.append(line)
                puntos.append(i)

        self.view.add_regions("diferentes", self.lista, "comment", "bookmark", sublime.DRAW_OUTLINED)
        sublime.status_message("Diff : "+str(len(self.lista)))
        f=open(sublime.packages_path()+os.sep+"errores.txt", "w")
        for punto in puntos:
            f.write(str(punto)+"\n")
        f.close()
        view.run_command("buscar_errores")

class CompareFilesIgnoreCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        self.file=view.file_name()
        self.lista=[]
        for window in sublime.windows():
            for view in window.views():
                filename=view.file_name()
                if filename:
                    self.lista.append(filename)
        self.lista.remove(view.file_name())

        if len(self.lista)==1:
            self.diff(self.lista[0])
        elif len(self.lista)>1:
            window.show_quick_panel(self.lista, self.seleccionar)


    def seleccionar(self, opcion):
        if opcion==-1:return
        archivo=self.lista[opcion]
        self.diff(archivo)
    
    def diff(self, archivo):    
        lines=self.view.lines(sublime.Region(0, self.view.size()))
        lineas=codecs.open(archivo,'r',encoding='utf8').readlines()
        self.lista=[]
        comentarioLargo=False
        puntos=[]
        i=0
        for line in lines:
            i+=1
            lineaOriginal=self.view.substr(line)
            linea=lineaOriginal.strip()
            if linea=="}":continue
            if comentarioLargo:
                if linea.endswith("*/"):comentarioLargo=False
                continue
            elif linea.startswith("/*") and linea.endswith("*/"):
                continue
            elif linea.startswith("/*"):
                comentarioLargo=True
                continue
            elif linea.startswith("//"):
                continue
            linea=lineaOriginal
            if not linea.strip():continue
            if not linea+"\n" in lineas:
                puntos.append(i)
                self.lista.append(line)
        self.view.add_regions("diferentes", self.lista, "comment", "bookmark", sublime.DRAW_OUTLINED)
        sublime.status_message("Diff : "+str(len(self.lista)))
        f=open(sublime.packages_path()+os.sep+"errores.txt", "w")
        for punto in puntos:
            f.write(str(punto)+"\n")
        f.close()
        view.run_command("buscar_errores")


class CleanCompareFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.erase_regions("diferentes")


class CompareScriptsDatabase(sublime_plugin.TextCommand):
    def run(self, edit):

        window=sublime.active_window()
        view=window.active_view()
        self.file=view.file_name()
        self.lista=[]
        for view in window.views():
            filename=view.file_name()
            if filename:
                self.lista.append(filename)
        self.lista.remove(view.file_name())

        if len(self.lista)==1:
            self.diff(self.lista[0])
        elif len(self.lista)>1:
            window.show_quick_panel(self.lista, self.seleccionar)


    def seleccionar(self, opcion):
        if opcion==-1:return
        archivo=self.lista[opcion]
        self.diff(archivo)
    
    def diff(self, archivo):    
        lines=utils.get_text().splitlines()
        lineas=open(archivo).readlines()
        tablas1=self.obtenerTablas(lines)
        tablas2=self.obtenerTablas(lineas)
        print("va a hacer el diff")
        print("Analizando la Base de datos actual")
        for key in tablas1.keys():
            print("\tAnalisis de Tabla "+key)
            if not tablas2.get(key):
                print("\t\tNo esta en la BD vieja")
            else:
                for campo in tablas1[key]:
                    if not campo in tablas2[key]:
                        print("\t\tFalta el campo {"+campo+"} en la BD Vieja")
        
        print("Analizando la Base de datos Vieja")
        for key in tablas2.keys():
            print("\tAnalisis de Tabla "+key)
            if not tablas1.get(key):
                print("\t\tNo esta en la BD Nueva")
            else:
                for campo in tablas2[key]:
                    if not campo in tablas1[key]:
                        print("\t\tFalta el campo {"+campo+"} en la BD Nueva")
        

    def obtenerTablas(self, lines):
        tablas={}
        tomandoCampos=False
        nombreTabla=""
        for line in lines:
            line=line.strip().lower();
            if line.startswith("--"):continue
            if tomandoCampos and line==");":tomandoCampos=False
            if line.startswith("create table"):
                nombreTabla=line.replace("create table", "").strip()
                tablas[nombreTabla]=[]
                tomandoCampos=True
            elif tomandoCampos:
                line=re.sub("\) +;", ");", line)
                if line.endswith(");"):
                    line=line.replace(");", "")
                    tomandoCampos=False
                if line.strip()=="(":continue
                if line.strip():
                    tablas[nombreTabla].append(line.replace(",", ""))
        return tablas


        