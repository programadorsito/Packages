import sublime_plugin
import sublime
import os

class CrearComandoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        window.show_input_panel("command, name", "", self.crearComando, None, None)

    def crearComando(self, strComando):
        if not strComando:
            sublime.status_message("No ingreso ningun comando")
            return
        self.silencioso=False
        strComando=strComando.strip()
        if strComando.endswith(";"):
            self.silencioso=True
            strComando=strComando[:-1]
        puntoCorte=strComando.find(";")
        comando=strComando[:puntoCorte]
        nombre=strComando[puntoCorte+1:]
        os.chdir(sublime.packages_path()+os.sep+"comandos")
        self.agregarNombreComando(nombre)
        self.agregarArchivoComandos(nombre, comando)
    
    def agregarNombreComando(self, nombre):
        nombreComando=self.nombreComando(nombre)
        nombre=nombreComando
        nombre=nombre[:nombre.find("_")]+": "+nombre[nombre.find("_")+1:]
        print("el nombre del comando es : "+nombreComando)
        textCommand="""
[{"caption":"%(caption)s", "command":"%(comando)s"}]
"""%{"caption":nombre.replace("_", " "), "comando":nombreComando}
        archivo=open(sublime.packages_path()+os.sep+"comandos"+os.sep+nombreComando+".sublime-commands", "w")
        archivo.write(textCommand)
        archivo.close()

    def agregarArchivoComandos(self,nombre, comando):
        nombreComando=self.nombreComando(nombre)
        silencioso=""
        if self.silencioso:silencioso="_silencioso"
        textCommand="""
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
from subprocess import PIPE, Popen

class %(nombreComando)sCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("ejecutar_comando%(silencioso)s", {"comando":'%(comando)s'})
"""%{"nombreComando":nombre, "comando":comando, "silencioso":silencioso}
        archivo=open(sublime.packages_path()+os.sep+"comandos"+os.sep+nombreComando+".py", "w")
        archivo.write(textCommand)
        archivo.close()

    def nombreComando(self, nombre):
        i = 0
        commandName=nombre[i].lower()
        i+=1
        while i<len(nombre):
            c=nombre[i]
            if c.isupper():
                commandName+="_"
            commandName+=c.lower()
            i+=1
        return commandName