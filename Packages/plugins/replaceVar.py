import sublime_plugin
import sublime

class ReplaceVarCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        window.show_input_panel("new word", "", self.pedirNueva, None, None)

    def pedirNueva(self, nueva):
        if not nueva:return
        window=sublime.active_window()
        view=window.active_view()
        texto=view.substr(sublime.Region(0, view.size()))
        
        palabra=view.substr(view.word(view.sel()[0].a))
        palabraVariable=palabra[0].lower()+palabra[1:]
        palabraConstante=self.constante(palabraVariable)
        getPalabra=palabraVariable+".get"+palabra[:3]
        setPalabra=palabraVariable+".set"+palabra[:3]

        nuevaVariable=nueva[0].lower()+nueva[1:]
        nuevaConstante=self.constante(nuevaVariable)
        getNueva=nuevaVariable+".get"+nueva[:3]
        setNueva=nuevaVariable+".set"+nueva[:3]

        texto=texto.replace(getPalabra, getNueva).replace(setPalabra, setNueva).replace(palabra, nueva).replace(palabraVariable, nuevaVariable).replace(palabraConstante, nuevaConstante)

        view.run_command("replace_all", {"text":texto})

    def constante(self, variable):
        constante=""
        for c in variable:
            if c.isupper():
                constante+="_"
            constante+=c.upper()
        return constante

