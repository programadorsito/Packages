import sublime
import sublime_plugin
import utils
class OrderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        lineas=view.substr(sublime.Region(0, view.size())).splitlines()
        if utils.get_language()=="json":
            view.run_command("format_json")
            return
        filename=view.file_name()
        scopename=view.scope_name(0)
        if filename!=None and filename.endswith(".properties"):
            diccionario={}
            for linea in lineas:
                name=linea[:linea.find("=")]
                value=linea[linea.find("=")+1:]
                diccionario[name]=value
            keys=sorted(diccionario.keys())
            archivo=open(filename, "w")
            for key in keys:
                value=diccionario[key].strip()
                if value[0].islower():value=value[0].upper()+value[1:]
                archivo.write("%(key)s=%(value)s\n"%{"key":key, "value":value})
            archivo.close()
        elif scopename.startswith("text.") or scopename.find(".zul")!=-1:
            sublime.status_message("run format")
            view.run_command("format")