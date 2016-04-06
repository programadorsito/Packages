import threading
import re
import sublime_plugin
import sublime
import os
import socket
import utils

server_path={
    "jboss":os.path.join(os.environ["JBOSS_AS_HOME"], "standalone", "deployments"),
    "widfly":os.path.join(os.environ["WIDFLY_HOME"], "standalone", "deployments"),
    "weblogic":os.path.join(os.environ["WEBLOGIC_HOME"], "autodeploy"),
    "tomcat":os.path.join(os.environ["TOMCAT_HOME"], "webapps"),
    "tomee":os.path.join(os.environ["TOMEE_HOME"], "webapps"),
    "glassfish":os.path.join(os.environ["GLASSFISH_DOMAIN"], "autodeploy"),
    "glassfish_web":os.path.join(os.environ["GLASSFISH_WEB_DOMAIN"], "autodeploy"),
    "jetty":os.path.join(os.environ["JETTY_HOME"], "webapps"),
    "resin":os.path.join(os.environ["RESIN_HOME"], "webapps")
}

server_command={
    "jboss":'rm -f %(serverpath)s.failed && rm -f %(serverpath)s && rm -f %(serverpath)s.deployed && rm -f %(serverpath)s.undeployed && cp %(filepath)s %(serverpath)s && exit',
    "weblogic":'rm -f "%(serverpath)s" && cp "%(filepath)s" "%(serverpath)s" && exit',
    "glassfish":'rm -f %(serverpath)s rm -f %(serverpath)s_deployed && cp %(filepath)s %(serverpath)s && exit',
    "widfly":'rm -f %(serverpath)s && rm -f %(serverpath)s.deployed && rm -f %(serverpath)s.undeployed && cp %(filepath)s %(serverpath)s && exit',
    "tomcat":'rm -f %(serverpath)s && cp %(filepath)s %(serverpath)s && exit',
    "tomee":'rm -f %(serverpath)s && cp %(filepath)s %(serverpath)s && exit',
    "glassfish_web":'rm -f %(serverpath)s rm -f %(serverpath)s_deployed && cp %(filepath)s %(serverpath)s && exit',
    "jetty":'rm -f %(serverpath)s && cp %(filepath)s %(serverpath)s && exit',
    "resin":'rm -f %(serverpath)s && cp %(filepath)s %(serverpath)s && exit'
}


server_config={
    "jboss":os.path.join(os.environ["JBOSS_AS_HOME"], "standalone", "configuration", "standalone.xml"),
    "widfly":os.path.join(os.environ["WIDFLY_HOME"], "standalone", "configuration", "standalone.xml"),
    "weblogic":os.path.join(os.environ["WEBLOGIC_HOME"], "config", "config.xml"),
    "tomcat":os.path.join(os.environ["TOMCAT_HOME"], "conf", "server.xml"),
    "tomee":os.path.join(os.environ["TOMEE_HOME"], "conf", "server.xml"),
    "glassfish":os.path.join(os.environ["GLASSFISH_DOMAIN"], "config", "domain.xml"),
    "glassfish_web":os.path.join(os.environ["GLASSFISH_WEB_DOMAIN"], "config", "domain.xml"),
    "jetty":os.path.join(os.environ["JETTY_HOME"], "start.ini"),
    "resin":os.path.join(os.environ["RESIN_HOME"], "conf", "resin.properties")
}

server_default_port={
    "jboss":8080,
    "widfly":8080,
    "weblogic":7001,
    "tomcat":8080,
    "tomee":8080,
    "glassfish":8080,
    "glassfish_web":8080,
    "jetty":8080,
    "resin":8080
}

server_regex_port={
    "jboss":'<socket-binding name="http" port="([\d]+)"/>',
    "widfly":'<socket-binding name="http" port="\\$\\{jboss.http.port:([\d]+)\\}"/>',
    "weblogic":'<listen-port>([\d]+)</listen-port>',
    "tomcat":'<Connector\s+port="([\d]+)"\s+protocol="HTTP/1.1"',
    "tomee":'<Connector\s+port="([\d]+)" protocol="HTTP/1.1"',
    "glassfish":'<network-listener port="([\d]+)" protocol="http-listener-1" transport="tcp" name="http-listener-1" thread-pool="http-thread-pool"></network-listener>',
    "glassfish_web":'<network-listener port="([\d]+)" protocol="http-listener-1" transport="tcp" name="http-listener-1" thread-pool="http-thread-pool"></network-listener>',
    "jetty":'jetty.http.port\s*=\s*([\d]+)',
    "resin":'app.http\s*:\s*([\d]+)'
}

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


class SeleccionarServidorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.servers=["jboss","widfly","weblogic","tomcat","tomee","glassfish","glassfish_web","jetty","resin"]
        window=sublime.active_window()
        window.show_quick_panel(self.servers,self.seleccionar)
    def seleccionar(self, index):
        if index==-1:return
        server=self.servers[index]
        utils.set_preference("server", server)
                

class ViewPortJavaServerCommand(sublime_plugin.TextCommand):
    def run(self, view):
        pass

class ChangePortJavaServerCommand(sublime_plugin.TextCommand):
    def run(self, view):
        pass

class DeployOnJavaServerCommand(sublime_plugin.TextCommand):
    def run(self, view):
        servidor=utils.get_preference("server")
        if not servidor:
            sublime.status_message("No se ha definido un servidor")
            return
        self.servidor=servidor
        comando=server_command[servidor]
        print("el servidor es : "+servidor)
        servidor=server_path[servidor]
        folder=sublime.active_window().folders()[0]
        self.archivos=[]
        self.explore(folder)
        ruta=""
        for archivo in self.archivos:
            if archivo.endswith(".ear"):
                ruta=archivo
                break
            if archivo.endswith(".war"):ruta=archivo
        if not ruta:
            sublime.status_message("no hay nada pa desplegar")
            return
        filename=os.path.basename(ruta)
        os.chdir(folder)
        d={"filepath":ruta, "serverpath":os.path.join(servidor, filename)}
#        comando='mvn -q package -DskipTests && rm -f "%(weblogicpath)s" && cp "%(filepath)s" "%(weblogicpath)s" && exit'%d
        comando=comando%d
        print(comando)
        archivo=open(sublime.packages_path()+os.sep+"start.cmd", "w")
        archivo.write(comando)
        archivo.close()
        os.system("start /min "+sublime.packages_path()+os.sep+"start.cmd")
        threading.Thread(target=self.run_server).start()

    def run_server(self):
        print("va a correr el servidor")
        port=int(self.get_port())
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result=sock.connect_ex(("127.0.0.1", port))
        print("http://localhost:"+str(port))
        if result != 0:
            window=sublime.active_window()
            view=window.active_view()
            view.run_command("watch_java_server", {"server":self.servidor})
        else:sublime.status_message("Servidor en ejecucion o puerto ocupado")

    def explore(self, ruta):
        for subruta in os.listdir(ruta):
            newpath=os.path.join(ruta, subruta)
            if os.path.isdir(newpath):self.explore(newpath)
            elif os.path.isfile(newpath) and (subruta.endswith(".ear") or subruta.endswith(".war")):self.archivos.append(newpath)
    
    def get_port(self):
        string=open(server_config[self.servidor]).read()
        port=re.findall(server_regex_port[self.servidor], string)
        if not port:port=server_default_port[self.servidor]
        else:port=port[0]
        print("^_^ el puerto es : ")
        print(port)
        self.port=port
        return self.port
#        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        result=sock.connect_ex(("127.0.0.1", 8080))
#        if result != 0:
#            window=sublime.active_window()
#            view=window.active_view()
#            view.run_command("ejecutar_comando", {"comando":"standalone"})

#        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        result=sock.connect_ex(("127.0.0.1", 8888))
#
#        if result != 0:
#            window=sublime.active_window()
#            view=window.active_view()
#            print("va a ejcauar")
#            os.system("start /min startserv") 


class TomcatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result=sock.connect_ex(("127.0.0.1", 9000))
        adicional='echo "good"'
        if result == 0:
            window=sublime.active_window()
            view=window.active_view()
            print("va a ejcauar")
            adicional="start /min shutdown_tomcat"

        folder=sublime.active_window().folders()[0]
        self.archivos=[]
        self.explore(folder)
        ruta=""
        for archivo in self.archivos:
            if archivo.endswith(".ear"):
                ruta=archivo
                break
            if archivo.endswith(".war"):ruta=archivo
        if not ruta:
            sublime.status_message("no hay nada pa desplegar")
            return
        filename=os.path.basename(ruta)
        os.chdir(folder)
        d={"filepath":ruta, "serverPath":os.path.join(TOMCAT_HOME_DEPLOYMENT, filename), "folderpath":os.path.join(TOMCAT_HOME_DEPLOYMENT, filename.replace(".war", ""))}
        comando='mvn -q package -DskipTests && '+adicional+' && timeout /t 3 && rm -f -r %(folderpath)s && rm -f %(serverPath)s && cp %(filepath)s %(serverPath)s && startup && exit'%d
        print(comando)
        archivo=open(sublime.packages_path()+os.sep+"start.cmd", "w")
        archivo.write(comando)
        archivo.close()
        os.system("start /min "+sublime.packages_path()+os.sep+"start.cmd") 

    def explore(self, ruta):
        for subruta in os.listdir(ruta):
            newpath=os.path.join(ruta, subruta)
            if os.path.isdir(newpath):self.explore(newpath)
            elif os.path.isfile(newpath) and (subruta.endswith(".ear") or subruta.endswith(".war")):self.archivos.append(newpath)


class TomeeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        folder=sublime.active_window().folders()[0]
        self.archivos=[]
        self.explore(folder)
        ruta=""
        for archivo in self.archivos:
            if archivo.endswith(".ear"):
                ruta=archivo
                break
            if archivo.endswith(".war"):ruta=archivo
        if not ruta:
            sublime.status_message("no hay nada pa desplegar")
            return
        filename=os.path.basename(ruta)
        os.chdir(folder)
        d={"filepath":ruta, "serverPath":os.path.join(TOMEE_HOME_DEPLOYMENT, filename)}
        comando='mvn -q package -DskipTests && cp %(filepath)s %(serverPath)s && exit'%d
        print(comando)
        archivo=open(sublime.packages_path()+os.sep+"start.cmd", "w")
        archivo.write(comando)
        archivo.close()
        os.system("start /min "+sublime.packages_path()+os.sep+"start.cmd") 

    def explore(self, ruta):
        for subruta in os.listdir(ruta):
            newpath=os.path.join(ruta, subruta)
            if os.path.isdir(newpath):self.explore(newpath)
            elif os.path.isfile(newpath) and (subruta.endswith(".ear") or subruta.endswith(".war")):self.archivos.append(newpath)

class JettyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result=sock.connect_ex(("127.0.0.1", 7777))

        if result != 0:
            window=sublime.active_window()
            view=window.active_view()
            print("va a ejcauar")
            os.system("start /min startJetty") 

        folder=sublime.active_window().folders()[0]
        self.archivos=[]
        self.explore(folder)
        ruta=""
        for archivo in self.archivos:
            if archivo.endswith(".ear"):
                ruta=archivo
                break
            if archivo.endswith(".war"):ruta=archivo
        if not ruta:
            sublime.status_message("no hay nada pa desplegar")
            return
        filename=os.path.basename(ruta)
        os.chdir(folder)
        d={"filepath":ruta, "serverPath":os.path.join(JETTY_HOME_DEPLOYMENT, filename)}
        comando='mvn -q package -DskipTests && rm -f %(serverPath)s && timeout /T 2 && cp %(filepath)s %(serverPath)s && exit'%d
        print(comando)
        archivo=open(sublime.packages_path()+os.sep+"start.cmd", "w")
        archivo.write(comando)
        archivo.close()
        os.system("start /min "+sublime.packages_path()+os.sep+"start.cmd") 

    def explore(self, ruta):
        for subruta in os.listdir(ruta):
            newpath=os.path.join(ruta, subruta)
            if os.path.isdir(newpath):self.explore(newpath)
            elif os.path.isfile(newpath) and (subruta.endswith(".ear") or subruta.endswith(".war")):self.archivos.append(newpath)

    
