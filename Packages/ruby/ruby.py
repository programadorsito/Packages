import re
import os
import os.path
import sublime_plugin
import sublime

class RutasRuby:
	def root():
		return os.path.join(sublime.packages_path(), "ruby")
	def librerias():
		return os.path.join(RutasRuby.root(), "librerias.json")
	def libreria(libreria):
		return os.path.join(RutasRuby.root(), "librerias", libreria+".json")

class ArchivoRuby:
	def cargarLibrerias():
		return ArchivoRuby.leerArchivoJson(RutasRuby.librerias())

	def guardarLibrerias(librerias):
		ArchivoRuby.guardarArchivoJson(RutasRuby.librerias(), librerias)

	def cargarLibreria(libreria):
		return ArchivoRuby.leerArchivoJson(RutasRuby.libreria(libreria))

	def guardarLibreria(nombre, libreria):
		ArchivoRuby.guardarArchivoJson(RutasRuby.libreria(nombre), libreria)

	def leerArchivoJson(path):
		archivo=open(path)
		texto=archivo.read()
		archivo.close()
		return sublime.decode_value(texto)

	def guardarArchivoJson(path, objetos):
		archivo=open(path, "w")
		archivo.write(sublime.encode_value(objetos))
		archivo.close()

	def getTextoCompleto(todo=True):
		window=sublime.active_window()
		view=window.active_view()
		puntoFinal=view.size()
		if not todo:puntoFinal=view.sel()[0].a
		return view.substr(sublime.Region(0, puntoFinal))

	def limpiarTexto(texto):
		texto=re.sub('=\s*"[^"]*"','=String.new' , texto)
		texto=re.sub("=\s*'[^']*'","=String.new" , texto)
		texto=re.sub("=\s*[\d]+\.\.\.?[\d]+","=Range.new" , texto)
		texto=re.sub("=\s*[\d]+\.[\d]+", "=Float.new", texto)
		texto=re.sub("=\s*[\d]+", "=Fixnum.new", texto)
		texto=re.sub("=\s*\[[^\]]*\]", "=Array.new", texto)
		texto=re.sub("=\s*\{[^}]*\}", "=Hash.new", texto)
		texto=re.sub("=\s*true\s*", "=TrueClass.new", texto)
		texto=re.sub("=\s*false\s*", "=TrueClass.new", texto)
		texto=re.sub(":", "=Hash.new", texto)
		return texto

	def getTextoCompletoLimpio():
		return ArchivoRuby.limpiarTexto(ArchivoRuby.getTextoCompleto())

	def getMetodos(variable):
		texto=ArchivoRuby.getTextoCompletoLimpio()
		declaracionVariable=re.findall("%s\s*=\s*([\w]+)\.new"%variable, texto)
		if declaracionVariable:
			return ArchivoRuby.cargarLibreria(declaracionVariable[0])["objeto"]
		else:
			return ArchivoRuby.cargarLibreria(variable)["clase"]

class RubyListener(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if view.scope_name(0).startswith("source.ruby "):
			punto=view.sel()[0].a
			linea=view.substr(sublime.Region(view.line(punto).a,punto))
			lista=[]
			if linea.endswith("."):
				libreria=re.findall("([\w:$@]+)\.$", linea)[0]
				if libreria.startswith(":"):libreria="Symbol"
				libreria=view.substr(view.word(punto-1))
				lista=ArchivoRuby.getMetodos(libreria)
			else:
				lista=ArchivoRuby.cargarLibrerias()
			return [(e+"\t•", e) for e in lista]

	def on_pre_save(self, view):
		pass