import utils
import re
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
import time
import threading
from subprocess import PIPE, Popen


class EjecutarComandoCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        Comando(args.get("comando"))

class EjecutarComandoSilenciosoCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
#        print("llego")
        ComandoSilencioso.ejecutarComandoSilencioso(args.get("comando"))

class EjecutarUltimoComandoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        if view.settings().has("ultimo_comando"):
            self.ejecutar(view.settings().get("ultimo_comando"))
        else:
            sublime.status_message("no hay un ultimo comando")

    def ejecutar(self, comando):
        if comando:
            comando=comando.strip()
            self.view.settings().set("ultimo_comando", comando)
            if comando.endswith(";"):
                comando=comando[:-1]
                self.view.run_command("ejecutar_comando_silencioso", {"comando":comando})
            else:
                self.view.run_command("ejecutar_comando", {"comando":comando})

class EjecutarComandoGlobalCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        Comando(args.get("comando"), comandoGlobal=True)

class EjecutarComandoDialogoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("llamado")
        window=sublime.active_window()
        self.view=window.active_view()
        recomendacion=""
        if self.view.settings().has("ultimo_comando"):recomendacion=self.view.settings().get("ultimo_comando")
        window.show_input_panel("command",recomendacion,self.ejecutar, None, None)
    
    def ejecutar(self, comando):
        if comando:
            comando=comando.strip()
            self.view.settings().set("ultimo_comando", comando)
            if comando.endswith(";"):
                comando=comando[:-1]
                self.view.run_command("ejecutar_comando_silencioso", {"comando":comando})
            else:
                self.view.run_command("ejecutar_comando", {"comando":comando})

class Comando:
    def __init__(self, comando, comandoGlobal=False):
        """Ejecuta comandos en la ruta de apertura del proyecto, se le puede pasar el comando con los siguientes parametros
        $filename = nombre del archivo
        $package = nombre del paquete
        $file = nombre del archivo con extension
        $filepath = ruta del archivo
        $dirpath = direcotrio donde se encuentra el archivo
        $dirname = nombre del direcotrio donde se encuentra el archivo
        """
        window=sublime.active_window()
        self.window=window
        self.comandoGlobal=comandoGlobal
        self.comando=comando
        self.parametros=re.findall("@[\w]+", self.comando)
        preferences=re.findall("#[\w.]+", self.comando)
        print("estas son las preferencias : ", preferences)
        for preference in preferences:
            preferenceValue=utils.get_preference(preference[1:])
            if(preferenceValue!=None):self.comando=self.comando.replace(preference, preferenceValue)
            else:sublime.status_message("hay preferencias no definidas")
        self.pedidos=[]
        self.i=0
        if self.parametros:
            self.pedirParametros()
        else:
            self.ejecutarComando()

    def pedirParametros(self,parametro=None):
        print(self.i)
        if self.i!=0:self.pedidos.append(parametro)
        if self.i==len(self.parametros):
            print(self.parametros)
            print(self.pedidos)
            for j in range(0, self.i):
                print(j)
                self.comando=self.comando.replace(self.parametros[j], self.pedidos[j])
            self.ejecutarComando()
            return
        pedir=self.parametros[self.i].replace("@", "")
        self.i+=1
        self.window.show_input_panel(pedir, pedir, self.pedirParametros, None, None)
        

    def ejecutarComando(self):
        comandoGlobal=self.comandoGlobal
        comando=self.comando.replace("~", "@")

        esLinux=False
        esMac=False
        window=sublime.active_window()
        view=window.active_view()

        if window.folders():
            dirpath=window.folders()[0]
            dirname=os.path.basename(dirpath)
            comando=comando.replace("$dirname", dirname).replace("$dirpath", dirpath)
            os.chdir(window.folders()[0])

        if view.file_name():
            ruta=view.file_name()
            filename=os.path.basename(ruta)
            archivo=filename[:filename.rfind(".")]
            dirpath=os.path.dirname(ruta)
            dirname=os.path.basename(dirpath)
            package=utils.get_package()
            if package==None:package=""
            comando=comando.replace("$package", package).replace("$filename",archivo).replace("$filepath", ruta).replace("$dirname", dirname).replace("$dirpath", dirpath).replace("$file", filename).replace("~", "@")
            os.chdir(dirpath)

        if comando.endswith("^"):
            comando=comando[:-1]
            os.chdir(utils.get_folder())

        comando=comando
        pausa=" && pause>nul"
        plataforma = platform.system().lower().strip() 
        
        if plataforma=="linux":
            esLinux=True
            pausa=' && read - p ""'
        
        elif plataforma == "darwin":
            esMac=True

        if comando.strip():
            if esLinux:
                comando="gnome-terminal -x bash -c '%s'"%(comando+pausa)
                os.system(comando)
            elif esMac:
                rutaArchivoRun=os.path.join(sublime.packages_path(), "run.command")
                utils.file_write(rutaArchivoRun, comando)
                comando='open "'+rutaArchivoRun+'"'
                os.system(comando)
            else:
                comando="@echo off && "+comando+pausa+" && exit"
                print(comando)
                archivo=open(sublime.packages_path()+os.sep+"start.cmd", "w")
                archivo.write(comando)
                archivo.close()
                os.system("start "+sublime.packages_path()+os.sep+"start.cmd") 

class ComandoSilencioso:
    def ejecutarComandoSilencioso(comando, comandoGlobal=False):
#        print("ejecutando el callado")
        """Ejecuta comandos en la ruta de apertura del proyecto, se le puede pasar el comando con los siguientes parametros
        $filename = nombre del archivo
        $file = nombre del archivo con extension
        $filepath = ruta del archivo
        $dirpath = direcotrio donde se encuentra el archivo
        $dirname = nombre del direcotrio donde se encuentra el archivo
        """
        window=sublime.active_window()
        view=window.active_view()

        if comandoGlobal and (window.folders()):
            dirpath=window.folders()[0]
            dirname=os.path.basename(folder)
            comando=comando.replace("$dirname", dirname).replace("$dirpath", dirpath)
            os.chdir(window.folders()[0])

        if view.file_name():
            ruta=view.file_name()
            filename=os.path.basename(ruta)
            archivo=filename[:filename.rfind(".")]
            dirpath=os.path.dirname(ruta)
            dirname=os.path.basename(dirpath)
            comando=comando.replace("$filename",archivo).replace("$filepath", ruta).replace("$dirname", dirname).replace("$dirpath", dirpath).replace("$file", filename)
            if not comandoGlobal:os.chdir(dirpath)
        
#        print("llego aqui")
        if comando.strip():
#            print("llego")
            ComandoSilencioso.ejecutarComando(comando)

    def ejecutar(**strComando):
        """Execute the GIT command"""
        time.sleep(1)
        strComando=strComando["comando"]
        proceso=subprocess.Popen(ComandoSilencioso.comando(strComando), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if proceso.communicate()[1]:
            error=proceso.communicate()[1].decode("utf-8")
            sublime.status_message("MAL "+error)
            print(error)
        else:
            salida=proceso.communicate()[0].decode("utf-8")
            print(salida)
            sublime.active_window().run_command("refresh_folder_list")
            sublime.status_message("-----OK-----")
            return salida

    def comando(comando):
        """Open the terminal according to the system"""
        return comando if sublime.platform()=="windows" else "gnome-terminal -x bash -c '%s'"%(comando)

    def ejecutarComando(comando):
        strComando=comando
#        print("comando:")
        print(comando)
        threading.Thread(target=ComandoSilencioso.ejecutar, kwargs={"comando":comando}).start()
        sublime.active_window().run_command("refresh_folder_list")
        sublime.status_message("Success : "+comando)