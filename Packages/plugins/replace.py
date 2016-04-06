import utils
import sublime_plugin
import sublime


class ReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        window=sublime.active_window()
        view=window.active_view()
        if args!=None:
            old=args["old"]
            new=args["new"]
            texto=view.substr(sublime.Region(0, view.size()))
            texto=texto.replace(old, new)
            view.replace(edit, sublime.Region(0, view.size()), texto)

class ReplaceAllCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        text=args.get("text")
        window=sublime.active_window()
        view=window.active_view()
        view.replace(edit, sublime.Region(0, view.size()), text)

class ReplaceFromCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        text=args.get("text")
        point=args.get("point")
        window=sublime.active_window()
        view=window.active_view()
        view.replace(edit, sublime.Region(punto, view.size()), text)

class ReplaceFromSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        text=args.get("text")
        window=sublime.active_window()
        view=window.active_view()
        punto=view.sel()[0].a
        view.replace(edit, sublime.Region(0, view.size()), text)

class ReemplazarRegionCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        print("entro")
        text=args["text"]
        print(text, args["region"])
        region=sublime.Region(args["region"][0],args["region"][1])
        print(region)
        window=sublime.active_window()
        view=window.active_view()
        view.replace(edit, region, text)
        print("salio")