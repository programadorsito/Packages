import sublime
import sublime_plugin

class InsertarCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		view=sublime.active_window().active_view()
		if args.get("text"):
			if args.get("point")!=None:
				view.insert(edit, args.get("point"), args.get("text"))
			else:
				for punto in view.sel():view.insert(edit, punto.b, args.get("text"))

