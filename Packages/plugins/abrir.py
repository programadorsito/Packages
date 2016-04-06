import sublime_plugin
import sublime
import os
import os.path

class configurarConexionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        scope=view.scope_name(0)
        scope=scope[:scope.find(" ")]
        self.lenguaje=scope[scope.find(".")+1:]
        self.cadenasConexion={}
        self.cadenasConexion["plsql"]="user/pass@ip:1521/orcl"
        window.show_input_panel("url connection", self.cadenasConexion[self.lenguaje], self.configurarCadena, None, None)


    def configurarCadena(self, cadena):
        comando={}
        if self.lenguaje=="plsql":
            comando["cmd"]=["sqlplus", cadena, "@", "$file"]
            comando["selector"]="source.plsql"
        comando=sublime.encode_value(comando, True)
        ruta=os.path.join(sublime.packages_path(), "user", self.lenguaje+".sublime-build")
        archivo=open(ruta, "w")
        archivo.write(comando)
        archivo.close()

class AbrirCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        scope=view.scope_name(0)
        scope=scope[:scope.find(" ")]
        lenguaje=scope[scope.find(".")+1:]
        print("el lenguaje es : "+lenguaje)
        ruta=os.path.join(sublime.packages_path(), "user", lenguaje+".sublime-build")
        if not os.path.exists(ruta):
            sublime.status_message("no existe un build definido")
            return
        window.run_command("set_build_system", {"file": "Packages/User/%s.sublime-build"%(lenguaje)})
        print("se definio el nuevo")
        window.run_command("build")