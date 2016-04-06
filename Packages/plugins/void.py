import sublime_plugin
import sublime
import utils

class VoidCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        metodo="""public void ${1:name}(){
    try{
        ${3:}
    }catch(Exception e){
        lerror(LOG, "Error al ${2:}", e);
    }
}
"""
        view.run_command('insert_snippet', {"contents":metodo})

class StringMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        metodo="""public String ${1:name}(){
    try{
        ${3:}
    }catch(Exception e){
        lerror(LOG, "Error al ${2:}", e);
    }
}
"""
        view.run_command("insert_snippet", {"contents":metodo})

class BooleanMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        metodo="""public String ${1:name}(){
    try{
        ${3:}
    }catch(Exception e){
        lerror(LOG, "Error al ${2:}", e);
    }
}
"""
        view.run_command("insert_snippet", {"contents":metodo})