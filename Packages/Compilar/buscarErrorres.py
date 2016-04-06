import sublime
import os
import sublime_plugin

class BuscarErroresCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		f=open(sublime.packages_path()+os.sep+"errores.txt")
		lineas=f.readlines()
		f.close()
		if not lineas:
			sublime.status_message("no hay errores")
			return
		linea=lineas[0]
		f=open(sublime.packages_path()+os.sep+"errores.txt", "w")
		for l in lineas:
			if l==linea:continue
			f.write(l)
		f.write(linea)
		justificacion=linea[linea.find(":")+1:]
		linea=linea[:linea.find(":")]
		sublime.status_message("Error: line "+linea)
		
		sublime.active_window().active_view().run_command("goto_line", {"line": linea} )
		sublime.status_message(justificacion)
			
