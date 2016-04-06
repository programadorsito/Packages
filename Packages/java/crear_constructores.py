import sublime_plugin
import sublime
import utils
import re

class CreateConstructorsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text=utils.get_text()
        atributos=re.findall("private ([\w]+) ([\w]+)\s*;|private ([\w]+) ([\w]+)\s*=", text, flags=re.IGNORECASE)
        nombreClase=re.findall("public class ([\w]+)", text, flags=re.IGNORECASE)
        if not nombreClase or not atributos:return

        nombreClase=nombreClase[0]
        listAtributos=[]
        strAtributos=""
        strCabecera=""
        strConstructor="""\tpublic %(nombreClase)s(%(cabeceraConstructor)s){
%(atributos)s
    }"""
        for atributo in atributos:
            strCabecera+=atributo[0]+" "+atributo[1]+","
            strAtributos+="\t\tthis."+atributo[1]+"="+atributo[1]+";\n"
        if strCabecera:strCabecera=strCabecera[:-1]
        if strAtributos:strAtributos=strAtributos[:-1]

        dConstructor={"atributos":strAtributos, "nombreClase":nombreClase, "cabeceraConstructor":strCabecera}
        strConstructorMaxivo=strConstructor%dConstructor
        window=sublime.active_window()
        view=window.active_view()
        view.insert(edit, view.line(view.sel()[0]).a, """\tpublic %(nombreClase)s(%(cabeceraConstructor)s){
        this.%(atributo)s=%(atributo)s;
    }\n\n"""%{"nombreClase":nombreClase, "atributo":atributos[0][1], "cabeceraConstructor":atributos[0][0]+" "+atributos[0][1]})
        view.insert(edit, view.line(view.sel()[0]).a, strConstructorMaxivo)




                