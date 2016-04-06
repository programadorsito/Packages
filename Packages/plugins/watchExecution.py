import winsound
import time
import sublime_plugin
import subprocess
import threading
import re
import os
import sublime
import utils
#view.run_command("watch_execution", {"comando":"standalone", "expresion":"hptu", "funcion":None})

errores={}
causaErrores={}
archivos={}
tiempo={}
erroresPorArchivo={}

server_run_file={
    "jboss":os.path.join(os.environ["JBOSS_AS_HOME"], "bin", "standalone.bat"),
    "widfly":os.path.join(os.environ["WIDFLY_HOME"], "bin", "standalone.bat"),
    "weblogic":os.path.join(os.environ["WEBLOGIC_HOME"], "bin", "startWebLogic.cmd"),
    "tomcat":os.path.join(os.environ["TOMCAT_HOME"], "bin", "startup.bat"),
    "tomee":os.path.join(os.environ["TOMEE_HOME"], "bin", "startup.bat"),
    "glassfish":os.path.join(os.environ["GLASSFISH_DOMAIN"], "..", "..", "bin", "startserv.bat"),
    "glassfish_web":os.path.join(os.environ["GLASSFISH_WEB_DOMAIN"], "..", "..", "bin", "startserv.bat"),
    "jetty":os.path.join(os.environ["JETTY_HOME"], "bin", "startJetty.bat"),
    "resin":os.path.join(os.environ["RESIN_HOME"], "bin", "start.bat")
}

class WatchExecutionCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        threading.Thread(target=WatchExecutionCommand.watch, kwargs={"comando":args.get("comando"), "funcion":args.get("funcion"), "expresion":args.get("expresion")}).start()

    def watch(**args):
        global archivos
        archivos_java=utils.get_files_project(["java", "xhtml"])
        for archivo_java in archivos_java:
            archivos[os.path.basename(archivo_java)]=archivo_java
        infinito=False
        comando=args["comando"]
        expresion=args["expresion"]
        funcion=None
        final=None
        if comando=="standalone":
            infinito=True
            WatchJbossCommand.tiempo=time.time()
            funcion=WatchJbossCommand.watch

        elif comando=="startWebLogic":
            infinito=True
            WatchWeblogicCommand.tiempo=time.time()
            funcion=WatchWeblogicCommand.watch

        elif comando.startswith("mvn "):
            global errores
            global causaErrores
            errores={}
            causaErrores={}
            print("activo maven")
            funcion=WatchMavenCommand.watch
            final=WatchMavenCommand.terminar
            window=sublime.active_window()
            os.chdir(window.folders()[0])

        elif comando=="gradle build":
            WatchAndroidGradleCommand.errores={}
            WatchAndroidGradleCommand.causaErrores={}
            funcion=WatchAndroidGradleCommand.watch
            final=WatchAndroidGradleCommand.terminar
            window=sublime.active_window()
            os.chdir(window.folders()[0])

        elif comando=="npm install":
            funcion=WatchNodeCommand.watch
            final=WatchNodeCommand.terminar
            window=sublime.active_window()
            os.chdir(window.folders()[0])

        elif utils.get_preference("server"):
            funcion=WatchJavaServerCommand.watch
            final=WatchJavaServerCommand.terminar



        final_comando=None
        command_end={
            "gradle build":"Total\\s+time:\\s+\\d+",
            "mvn package":"",
            "npm install":""
        }

        if command_end.get(comando)!=None:final_comando=command_end[comando]
        print("comando : "+comando)
        proc = subprocess.Popen(comando,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        while True:
            proc_read = proc.stdout.readline()
            try:proc_read = proc_read.decode("utf-8")
            except:pass
            if proc_read:
                proc_read=proc_read.strip()
                try:
                    if proc_read==None or proc_read.startswith("[ERROR]   mvn <goals>") or proc_read.startswith("[INFO] BUILD SUCCESS") or proc_read.startswith("[INFO] BUILD FAILURE") and not infinito:
                        print("end here")
                        final()
                        break
                    elif re.findall(expresion, proc_read, re.IGNORECASE):
                        funcion(proc_read)
                except:pass
            else:
                if comando in ["npm install"]:final()
#                final()
                break

class WatchJavaServerCommand(sublime_plugin.TextCommand):
    server=None
    def run(self, edit, **args):
        print("va a hacer el despliegue en un servidor de java")
        server=args["server"]
        WatchJavaServerCommand.server=server
        print("el servidor ess : "+server)
        if not server:sublime.status_message("servidor no definido")
        window=sublime.active_window()
        view=window.active_view()
        if server in ["jboss","weblogic"]:view.run_command("watch_"+server)
        else:
            return
            archivo_ejecucion=server_run_file[server]
            print(archivo_ejecucion)
            carpeta_ejecucion=os.path.dirname(archivo_ejecucion)
            os.chdir(carpeta_ejecucion)
            comando=os.path.basename(archivo_ejecucion)
            view.run_command("watch_execution", {"comando":comando, "expresion":".*"})

    def watch(str):
        print(WatchJavaServerCommand.server+"> "+str)

    def terminar():
        print("ha terminado la ejecucion del servidor")


class WatchJbossCommand(sublime_plugin.TextCommand):
    tiempo=time.time()

    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("watch_execution", {"comando":"standalone", "expresion":".*"})
    
    def watch(str):
        str=str.strip()
        print("Jboss> "+str)
        
        if str.find("test ^_^")!=-1:pass
#            print("Jboss > "+str)

        if str.find("Caused by:")!=-1:
            print("cause by  : "+str)
#print("Jboss > "+str)

#            listaErrores=re.findall("[\w]+Exception:", str)
            listaErrores=[]
            if listaErrores:str=listaErrores[0]
            else:
                str=str[str.find("Caused by:")+10:]
                str=str[str.find(":")+1:]
                str=re.sub("[\w]+[.]+[\w]+", "", str)
                str=re.sub("[\w]+[/]+", "", str)
                str=re.sub("[\w]+[\d]+", "", str)
                str=str.replace(":", "")
            
            window=sublime.active_window()
            view=window.active_view()
            view.run_command("tts", {"msg":str})
            
        if re.findall('Deployed "[^"]*"|Replaced deployment "[^"]*"', str):
#            print("Jboss > "+str)
            window=sublime.active_window()
            view=window.active_view()
            view.run_command("tts",{"msg":"The Application was Deployed"})

#        elif str.startswith("Caused by: javax.el.ELException: ")!=-1:
#            archivos={}
#            lista=re.findall("([\w_]+.xhtml) @([\d]+)", str)
#            vista=lista[0][0]
#            linea=lista[0][1]
#            msg=str[str.rfind(":")+1:]
            print("Error en el archivo "+vista+" en la linea : "+linea)
#            archivo=archivos[vista]
#            window=sublime.active_window()
#            view=window.open_file(archivo)
#            time.sleep(2)
#            view.run_command("go_and_check", {"lines":[linea]})
#            view.run_command("tts", {"msg":msg})

        elif str.find("at com.co.hptu")!=-1 or re.findall("[\w_]+\.xhtml @[\d]+,[\d]+", str):
#            print("Jboss > "+str)
#            print("Error encontrado ^_^")
            lista=[]
            errorVista=False
            if str.find("at com.co.hptu")!=-1:
                lista=re.findall("([\w]+)\(([\w]+\.java):([\d]+)\)", str)
            else:
                lista=re.findall("([\w_]+.xhtml) @([\d]+)", str)
                errorVista=True

            if lista:
#                metodo=lista[0][0]
                diff=1 if errorVista else 0
                clase=lista[0][1-diff]
                linea=lista[0][2-diff]       
                if clase in ["EncodingFilter.java", "LoginManagedBean.java", "LdapUserDetailsMapper.java", "PropertiesLoader.java"]:return
#                window=sublime.active_window()
#                view=window.active_view()
#                view.run_command("tts",{"msg":"Error found"})
                global archivos
                global erroresPorArchivo
                if not erroresPorArchivo.get(clase):
                    erroresPorArchivo[clase]=[]

                if linea in erroresPorArchivo[clase]:return
                erroresPorArchivo[clase].append(linea)
                archivo=archivos[clase]
                window=sublime.active_window()
                view=window.open_file(archivo)
                time.sleep(2)
                view.run_command("go_and_check", {"lines":[linea]})

    def terminar():
        print("Servidor finalizado")

class WatchWeblogicCommand(sublime_plugin.TextCommand):
    tiempo=time.time()

    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("watch_execution", {"comando":"startWebLogic", "expresion":".*"})
    
    def watch(str):
        str=str.strip()
        print("Weblogic > "+str)

        if str.find("Caused by:")!=-1:
#            print("cause by  : "+str)

#            listaErrores=re.findall("[\w]+Exception:", str)
            listaErrores=[]
            if listaErrores:str=listaErrores[0]
            else:
                str=str[str.find("Caused by:")+10:]
                str=str[str.find(":")+1:]
                str=re.sub("[\w]+[.]+[\w]+", "", str)
                str=re.sub("[\w]+[/]+", "", str)
                str=re.sub("[\w]+[\d]+", "", str)
                str=str.replace(":", "")
            
            window=sublime.active_window()
            view=window.active_view()
            view.run_command("tts", {"msg":str})
            
        if str.find('INFO: Running on PrimeFaces')!=-1:
            window=sublime.active_window()
            view=window.active_view()
            view.run_command("tts",{"msg":"The Application is Running on Primerfaces"})

#        elif str.startswith("Caused by: javax.el.ELException: ")!=-1:
#            archivos={}
#            lista=re.findall("([\w_]+.xhtml) @([\d]+)", str)
#            vista=lista[0][0]
#            linea=lista[0][1]
#            msg=str[str.rfind(":")+1:]
#            print("Error en el archivo "+vista+" en la linea : "+linea)
#            archivo=archivos[vista]
#            window=sublime.active_window()
#            view=window.open_file(archivo)
#            time.sleep(2)
#            view.run_command("go_and_check", {"lines":[linea]})
#            view.run_command("tts", {"msg":msg})

        elif str.find("at com.co.hptu")!=-1 or re.findall("[\w_]+\.xhtml @[\d]+,[\d]+", str):
            print("Error encontrado ^_^")
            lista=[]
            errorVista=False
            if str.find("at com.co.hptu")!=-1:
                lista=re.findall("([\w]+)\(([\w]+\.java):([\d]+)\)", str)
            else:
                lista=re.findall("([\w_]+.xhtml) @([\d]+)", str)
                errorVista=True

            if lista:
#                metodo=lista[0][0]
                diff=1 if errorVista else 0
                clase=lista[0][1-diff]
                linea=lista[0][2-diff]       
                if clase in ["EncodingFilter.java", "LoginManagedBean.java", "LdapUserDetailsMapper.java", "PropertiesLoader.java"]:return
#                window=sublime.active_window()
#                view=window.active_view()
#                view.run_command("tts",{"msg":"Error found"})
                global archivos
                global erroresPorArchivo
                if not erroresPorArchivo.get(clase):
                    erroresPorArchivo[clase]=[]

                if linea in erroresPorArchivo[clase]:return
                erroresPorArchivo[clase].append(linea)
                archivo=archivos[clase]
                window=sublime.active_window()
                view=window.open_file(archivo)
                time.sleep(2)
                view.run_command("go_and_check", {"lines":[linea]})

    def terminar():
        print("Servidor finalizado")

class WatchNodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("watch_execution", {"comando":"npm install", "expresion":".*"})

    def watch(str):
        print(str)

    def terminar():
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("tts", {"msg":"all dependencies installed"})
        sublime.status_message("OK")
        view.run_command("deploy")
        
class WatchMavenCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print("watch maven")
        self.list=[]
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("watch_execution", {"comando":"mvn package", "expresion":"\[ERROR\] [^.]+\\.java:\\[\\d+,\\d+\\]"})

    def watch(str):
        str=str.strip()
        str=str.replace("[ERROR] /", "")
        str=str.replace("[ERROR] ", "")
        print(str)

        window=sublime.active_window()
        separador="/"
        if str.count("\\")>str.count("/"):separador="\\"

        archivo=str[:str.find(":[")]
        if archivo.startswith("\\") or archivo.startswith("/"):archivo=window.folders()[0][0]+":"+archivo
        linea=str[str.rfind("[")+1:str.rfind("]")].split(",")[0]
        if not linea.strip():return
        causa=str[str.rfind("]")+1:]
        print("causa : "+causa)
        view=window.active_view()
        print(archivo[archivo.rfind(separador)+1:]+":"+linea+":"+causa)
        global errores
        global causaErrores
        if not errores.get(archivo):errores[archivo]=[]
        if not causaErrores.get(archivo):causaErrores[archivo]={}
        causaErrores[archivo][linea]=causa
        errores[archivo].append(linea)

    def terminar():
        print("finalizando maven")
        global errores
        window=sublime.active_window()
        view=window.active_view()
        if not errores:
            view.run_command("tts", {"msg":"compilation successfull"})
            sublime.status_message("OK")
            view.run_command("deploy")
        else:
            view.run_command("tts", {"msg":"compilation with errors"})
        print("OK")
        for archivo in errores.keys():
            window=sublime.active_window()
            print("el archivo es : "+archivo)
            view=window.open_file(archivo)     
            view.run_command("clear_bookmarks")
            time.sleep(1)
            lineas=list(set(errores[archivo]))
            view.run_command("go_and_check", {"lines":lineas})


class GotoFileLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        filepath=args["filepath"]
        window=sublime.active_window()
        window.open_file(filepath)        
        view=window.active_view()
        view.run_command("goto_line", {"line":args["line"]})
        view.run_command("toggle_bookmark")

class ViewErrorCauseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        project_type=utils.get_project_type()
        window=sublime.active_window()
        view=window.active_view()
        linea=view.line(view.sel()[0])
        lines=view.lines(sublime.Region(0, view.size()))
        i=0
        for line in lines:
            i+=1
            if line==linea:
                if project_type=="maven":
                    if causaErrores.get(view.file_name().replace("\\", "/")):
                        msg=causaErrores[view.file_name().replace("\\", "/")][str(i)]
                        sublime.status_message(msg)
                        msg=re.sub("[\w]+\.[\w]+", "", msg)
                        view.run_command("tts", {"msg":msg})
                elif project_type=="android.gradle":
                    msg=WatchAndroidGradleCommand.causaErrores[view.file_name()][str(i)]
                    sublime.status_message(msg)
                    msg=re.sub("[\w]+\.[\w]+", "", msg)
                    view.run_command("tts", {"msg":msg})
    
    def viewAndroidGradleError(self, view, line):
        pass

class WatchAndroidGradleCommand(sublime_plugin.TextCommand):
    errores={}
    causaErrores={}

    def run(self, edit):
        print("watch gradle")
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("watch_execution", {"comando":"gradle build", "expresion":".+"})

    def watch(line):
        line=line.strip()
        print(line)
        if re.findall(": error:", line, re.IGNORECASE):
            line=line.replace(":compileDebugJava", "")
            line=line.strip()
            ruta=line[:line.find(".java:")+5]
            print("el archivo es : "+ruta)
            window=sublime.active_window()
            view=window.open_file(ruta)
            line=line.replace(ruta, "")
            print(line)
            line=line[1:]
            print(line)
            causa=line[line.find(": error:")+8:]
            line=line[:line.find(":")]
            print("la linea es : "+line)
            print("error en  : "+line)
            WatchAndroidGradleCommand.errores[line]=causa
            if not WatchAndroidGradleCommand.causaErrores.get(ruta):
                WatchAndroidGradleCommand.causaErrores[ruta]={}
            WatchAndroidGradleCommand.causaErrores[ruta][line]=causa
        elif line=="BUILD FAILED":
            window=sublime.active_window()
            view=window.active_view()
            view.run_command("tts", {"msg":line})
            WatchAndroidGradleCommand.terminar()
        elif line=="BUILD SUCCESSFUL":
            window=sublime.active_window()
            view=window.active_view()
            view.run_command("tts", {"msg":line})
            view.run_command("deploy")

    def terminar():
        print("va a temrinar")
        print("los errores son : ")
        print(WatchAndroidGradleCommand.errores)
        print("las causas de errores son : ")
        print(WatchAndroidGradleCommand.causaErrores)

        window=sublime.active_window()
        for key in WatchAndroidGradleCommand.causaErrores.keys():
            view=window.open_file(key)
            lines=WatchAndroidGradleCommand.causaErrores[key].keys()
            for line in lines:
                view.run_command("go_and_check_line", {"line":int(line.strip())})
        print("termino")

class CerrarYLimpiarListener(sublime_plugin.EventListener):
    def on_close(self, view):
        global erroresPorArchivo
        archivo=view.file_name()
        if archivo:
            erroresPorArchivo[os.path.basename(archivo)]=[]

                
class BuildCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        project_type=utils.get_project_type()
        print("el tipo de proyecto es : "+project_type)
        if project_type == "maven":view.run_command("watch_maven")
        elif project_type=="android.gradle":view.run_command("watch_android_gradle")
        elif project_type=="node":view.run_command("watch_node")