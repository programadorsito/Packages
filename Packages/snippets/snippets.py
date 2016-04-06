import utils
import re
import sublime
import os
import os.path
import sublime_plugin

def get_path_snippets():
	return os.path.join(sublime.packages_path(), "snippets")

class SnippetsListener(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		#if view.substr(view.line(view.sel()[0].a)).strip():return
		#si es completacion por punto entonces no haga nada
		if view.substr(sublime.Region(view.sel()[0].a-1, view.sel()[0].a))==".":return
		snippets=Snippets.cargarSnippets()
		if not snippets:return
		lista=[]
		for snippet in snippets:
			lista.append((snippet+"\t(Snippet)•", self.agregarCursores(snippets[snippet])))
		return lista

	def agregarCursores(self, texto):
		simbolo="@" if texto.find("~")==-1 else "~"
		excepciones = [int(posicion) for posicion in re.findall("%s(?P<cantidad>\d+)"%simbolo, texto)]
		completion=""
		i=1
		recogiendo=False
		cursor=False
		numero=""

		for c in texto:

			if cursor and c.isdigit():
				numero+=c
				continue

			if cursor:
				if not numero:
					while i in excepciones:
						i+=1
					completion+="${"+str(i)+":"	
					i+=1
				else:
					completion+="${"+numero+":"
				cursor=False
				

			if c==simbolo:
				cursor=True
				numero=""
				recogiendo=True
				continue

			if recogiendo and not c.isalpha():
				completion+="}"
				recogiendo=False
			completion+=c
		return completion

class AgregarSnippetCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window=sublime.active_window()
		view=window.active_view()
		self.snippets=Snippets.cargarSnippets()
		self.texto=view.substr(view.sel()[0])
		window.show_input_panel("Ingrese nombre", "", self.agregar, None, None)

	def agregar(self, nombre):
		self.texto=self.texto.replace("$", "\$")
		self.snippets[nombre]=self.texto
		Snippets.guardarSnippets(self.snippets)

class Snippets:
	def ruta():
		window=sublime.active_window()
		view=window.active_view()
		tipo=utils.get_language()
		#print("el tipo para los snippets es : "+tipo)
#		return sublime.packages_path()+os.sep+"snippets"+os.sep+tipo+".json"
		return get_path_snippets()+"/"+tipo+".json"
	
	def cargarSnippets():
		ruta=Snippets.ruta()
		if not os.path.exists(ruta):return {}
		snippets=sublime.decode_value(open(ruta).read())
		return snippets


	def guardarSnippets(snippets):
		ruta=Snippets.ruta()
		archivo=open(ruta, "w")
		archivo.write(sublime.encode_value(snippets))
		archivo.close()
