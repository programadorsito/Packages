import re
import sublime
import sublime_plugin

class BuscarDefinicionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window=sublime.active_window()
		view=window.active_view()
		tipo=view.scope_name(0)
		if tipo.startswith("source.python ") or tipo.startswith("source.java "):
			punto=view.sel()[0].a
			if tipo.startswith("source.python " ):
				self.lineas=list(reversed(view.substr(sublime.Region(0, punto)).splitlines()))
				self.variable=view.substr(view.word(punto))
				linea=view.substr(view.line(punto))
				if linea.find(self.variable+"(")!=-1:
					window.run_command("show_overlay",{"overlay": "goto", "text": "@"+self.variable})
				else:
					self.buscarDefinicionPython()
			elif tipo.startswith("source.java "):
				linea=view.substr(view.line(punto))
				self.variable=view.substr(view.word(punto))
				print("buscando la variable "+self.variable)

	def buscarDefinicionPython(self):
		view=sublime.active_window().active_view()
		i=0
		encontrada=False
		aumento=0
		for l in self.lineas:
			if re.findall(self.variable+"\s*=", l) or l.strip().startswith("def ") and re.findall(self.variable+"\s*[,)]",l):
				aumento+=l.find(self.variable)+1
				encontrada=True
				break
			i+=1
		if not encontrada:return
		i=len(self.lineas)-i
		view.run_command("go", {"row":i, "column":aumento})
		
