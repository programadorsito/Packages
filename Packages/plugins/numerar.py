import sublime_plugin
import sublime

class NumerarCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        sels=view.sel()
        i=len(sels)
        for sel in reversed(sels):
            view.run_command("insertar", {"point":sel.a, "text":str(i)})
            i-=1
                