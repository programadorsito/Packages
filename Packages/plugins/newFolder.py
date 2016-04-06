import os
import sublime
import sublime_plugin
class NewFolderCommand(sublime_plugin.TextCommand):
	def run(self, edit, args={}):
		if args.get("folder"):
			self.crearDirectorio(args["folder"])
			return
		window=sublime.active_window()
		view=window.active_view()
		self.raiz=""
		if view.file_name():
			self.raiz=os.path.dirname(view.file_name())
		elif window.folders():
			self.raiz=os.path.dirname(window.folders()[0])
		window.show_input_panel("nombre carpeta","", self.crearDirectorio, None, None)

	def crearDirectorio(self, nombre=None):
		if nombre!=None:
			os.mkdir(os.path.join(self.raiz,nombre))