import time
import sublime_plugin
import sublime
class GoCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		window=sublime.active_window()
		view=window.active_view()
		if args.get("line")!=None:
			print("the line es : ")
			print(args.get("line"))
			view.run_command("goto_line", {"line":args["line"]})
			return
		elif args.get("point")!=None:
			del view.sel()[0]
			view.sel().add(sublime.Region(args["point"], args["point"]))
		elif args.get("row")!=None:
			view.run_command("goto_line", {"line":args["row"]})
			punto=view.sel()[0].a+args["column"]
			del view.sel()[0]
			view.sel().add(sublime.Region(punto, punto))

class GoAndCheckCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		if not args.get("lines"):return
		window=sublime.active_window()
		view=window.active_view()
		lineas=view.lines(sublime.Region(0, view.size()))
		lines=args.get("lines")
		
		for line in lines:
			del view.sel()[0]
			view.sel().add(lineas[int(line)-1])
			view.run_command("toggle_bookmark")

class GoAndCheckLineCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		if not args.get("line"):return
		window=sublime.active_window()
		view=window.active_view()
		lineas=view.lines(sublime.Region(0, view.size()))
		line=args.get("line")
		del view.sel()[0]
		view.sel().add(lineas[int(line)-1])
		view.run_command("toggle_bookmark")
