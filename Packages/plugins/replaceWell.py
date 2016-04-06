import utils
import sublime_plugin
import sublime

class ReplaceWellCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        window.show_input_panel("new word", "", self.reemplazar, None, None)
    
    def reemplazar(self, word):
         window=sublime.active_window()
         view=window.active_view()
         sels=view.sel()
         i=len(sels)-1
         while i>=0:
            region=sels[i]
            text=view.substr(region)
            region=[region.a, region.b]
            new=word
            if text.isupper():new=new.upper()
            elif text.islower():new=new.lower()
            elif text[0].isupper():new=new[0].upper()+new[1:]
            view.run_command("reemplazar_region", {"text":new, "region":region})
            i-=1