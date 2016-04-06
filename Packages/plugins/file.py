import os.path
import os
import sublime
import sublime_plugin



class File:
	def __init__(self):
		self.window=sublime.active_window()
		self.view=self.window.active_view()
		self.ruta=view.file_name()
		if self.ruta:
			self.directorio=os.path.dirname(self.ruta)
			self.nombreArchivo=os.path.basename(self.ruta)
		
	def delete(self):
		if self.ruta:
			os.remove(self.ruta)
			sublime.status_message("Eliminado con exito")

class findICommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window=sublime.active_window()
		self.view=window.active_view()
		window.show_input_panel("regex", "", self.buscar, None, None)
		del self.view.sel()[0]

	def buscar(self, regex):
		regions=self.view.find_all(regex, sublime.IGNORECASE)
		for region in regions:
			self.view.sel().add(region)



class findCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window=sublime.active_window()
		self.view=window.active_view()
		window.show_input_panel("regex", "", self.buscar, None, None)
		del self.view.sel()[0]

	def buscar(self, regex):
		regions=self.view.find_all(regex)
		for region in regions:
			self.view.sel().add(region)
