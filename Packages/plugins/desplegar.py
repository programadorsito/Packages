import re
import os
import utils
import sublime_plugin
import sublime
import socket



class DeployCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        
#        project_type=utils.get_preference("project.type")
        project_type=utils.get_project_type()
        if project_type:print("entro y el tipo de proyecto es : "+project_type)
        window=sublime.active_window()
        view=window.active_view()
        if project_type=="android":view.run_command("deploy_android")
        elif project_type=="android.gradle":view.run_command("deploy_android_gradle")
        elif project_type=="node":view.run_command("deploy_node")
        else:
            server=utils.get_preference("server")
            if server:view.run_command("deploy_on_java_server")

class DeployNodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result=sock.connect_ex(("127.0.0.1", 3333))
        if result == 0:
            sublime.status_message("Servidor en ejecucion o puerto ocupado")
            return

        print("va a correr el servidor")
        window=sublime.active_window()
        pathExecutable=os.path.join(window.folders()[0], "app.js")
        comando='nodemon %s'%(pathExecutable)
        archivo=open(sublime.packages_path()+os.sep+"start.cmd", "w")
        archivo.write("@echo off\n")
        archivo.write(comando)
        archivo.close()
        os.system("start /min "+sublime.packages_path()+os.sep+"start.cmd") 

class DeployAndroidCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("Va a desplegar para android")
        folder=utils.get_folder()
        self.archivos=[]
        self.explore(folder)
        ruta=""
        for archivo in self.archivos:
            if archivo.endswith(".apk"):
                ruta=archivo
                break
        if not ruta:
            sublime.status_message("no hay nada pa desplegar")
            return
        filename=os.path.basename(ruta)
        os.chdir(folder)
        d={"filepath":ruta}
        comando='ant debug && adb install -r %(filepath)s && exit'%d
        print(comando)
        archivo=open(sublime.packages_path()+os.sep+"start.cmd", "w")
        archivo.write(comando)
        archivo.close()
        os.system("start /min "+sublime.packages_path()+os.sep+"start.cmd") 

    def explore(self, ruta):
        for subruta in os.listdir(ruta):
            newpath=os.path.join(ruta, subruta)
            if os.path.isdir(newpath):self.explore(newpath)
            elif os.path.isfile(newpath) and subruta.endswith(".apk"):self.archivos.append(newpath)

class DeployAndroidGradleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        folder=utils.get_folder()
        self.archivos=[]
        self.explore(folder)
        ruta=""
        for archivo in self.archivos:
            if archivo.endswith(".apk"):
                ruta=archivo
                break
        if not ruta:
            sublime.status_message("no hay nada para desplegar")
            os.chdir(folder)    
            comando='gradle build && exit'
            print(comando)
            archivo=open(sublime.packages_path()+os.sep+"start.cmd", "w")
            archivo.write(comando)
            archivo.close()
            os.system("start /min "+sublime.packages_path()+os.sep+"start.cmd") 
            return
        filename=os.path.basename(ruta)
        os.chdir(folder)
        d={"filepath":ruta}
        d["package"]=package=utils.get_package()
        d["classname"]=utils.get_filebasename()

#        if d["package"]:comando='gradle build && adb install -r %(filepath)s && adb shell am start -n %(package)s/%(package)s.%(classname)s && exit'%d
#        else:comando='gradle build && adb install -r %(filepath)s && exit'%d
        
        if d["package"]:comando='adb install -r %(filepath)s && adb shell am start -n %(package)s/%(package)s.%(classname)s && exit'%d
        else:comando='adb install -r %(filepath)s && exit'%d

        print(comando)
        archivo=open(sublime.packages_path()+os.sep+"start.cmd", "w")
        archivo.write(comando)
        archivo.close()
        os.system("start /min "+sublime.packages_path()+os.sep+"start.cmd") 

    def explore(self, ruta):
        for subruta in os.listdir(ruta):
            newpath=os.path.join(ruta, subruta)
            if os.path.isdir(newpath):self.explore(newpath)
            elif os.path.isfile(newpath) and subruta.endswith(".apk"):self.archivos.append(newpath)

    
class EjecutarJarCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        folder=window.folders()[0]
        archivos=utils.get_files({"folder":folder, "ext":"jar"})
        ejecutables=[]
        for archivo in archivos:
            if archivo.find("with-dependencies")!=-1:
                ejecutables.append(archivo)

        if len(ejecutables)==1:
            view.run_command("ejecutar_comando", {"comando":"java -jar "+ejecutables[0]})
        else:
            self.ejecutables=ejecutables
            window.show_quick_panel(ejecutables, self.elegirEjecutable)
        print(ejecutables)

    def elegirEjecutable(self,index):
        if index==-1:return
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("ejecutar_comando", {"comando":"java -jar "+self.ejecutables[index]})