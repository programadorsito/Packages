import sublime_plugin
import sublime
import utils

class TtsCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        msg=args["msg"]
        comando="echo \"%s\" > d:/ptts.txt && d:/ptts.vbs -v 100 -r -3 -u d:/ptts.txt"%(msg)
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("ejecutar_comando_silencioso", {"comando":comando})

