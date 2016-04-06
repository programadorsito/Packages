import sublime_plugin
import sublime

class HelpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        recomendacion=""
        if view.sel()[0].a!=view.sel()[0].b:
            recomendacion=view.substr(view.sel()[0])
        self.view=view
        tipo=view.settings().get("syntax")
        if tipo.find("/"):tipo=tipo[tipo.rfind("/")+1:]
        if tipo.find("."):tipo=tipo[:tipo.rfind(".")]
        if tipo.find(" "):tipo=tipo.replace(" ", "_")
        self.tipo=tipo.lower()
        if self.tipo=="nodejs":self.tipo="node.js"
        elif self.tipo=="python":self.tipo="python 2"
        elif self.tipo=="shell-unix-generic":self.tipo="bash"
        window.show_input_panel("help", recomendacion, self.ejecutar, None, None)

    def ejecutar(self, palabra):
        if not palabra:
            sublime.status_message("no se ha ingresado nada para buscar")
            return
        self.view.run_command("ejecutar_comando_silencioso", {"comando":"zeal \""+self.tipo+":"+palabra+'"'})