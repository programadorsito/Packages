import os
import sublime_plugin
import sublime
import json

class RutasPhp:
	def root():
		return sublime.packages_path()+os.sep+"php"+os.sep
	def clase(clase):
		return RutasPhp.root()+"clases"+os.sep+clase+".json"
	def funciones():
		return RutasPhp.root()+"funciones.json"
	def clases():
		return RutasPhp.root()+"clases.json"

class ArchivoPhp:
	def listaClases():
		return ArchivoPhp.leerJson(RutasPhp.clases())
	
	def listaFunciones():
		return ArchivoPhp.leerJson(RutasPhp.funciones())
	
	def listaMetodos(clase):
		return ArchivoPhp.leerJson(RutasPhp.clase(clase))

	def leer(ruta):
		archivo=open(ruta)
		texto=archivo.read()
		archivo.close()
		return texto

	def escribir(ruta, texto):
		archivo=open(ruta, "w")
		archivo.write(texto)
		archivo.close()

	def leerJson(ruta):
		return json.loads(ArchivoPhp.leer(ruta))

	def escribirJson(ruta, objeto):
		json.dumps(objeto, encoding='utf-8')

class phpListener(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if not view.scope_name(view.sel()[0].a).startswith("text.html.basic source.php"):return
		punto=view.sel()[0].a
		lista=[]
		linea=view.substr(sublime.Region(view.line(punto).a, punto))
		listaClases=ArchivoPhp.listaClases()
		if linea.endswith("."):
			palabra=view.substr(view.word(punto-1))
			if palabra in listaClases:
				lista=ArchivoPhp.listaMetodos(palabra)
		else:
			listaFunciones=ArchivoPhp.listaFunciones()
			lista=listaFunciones+listaClases
				
		if lista:
			return [(f.strip()+"\t•", self.cursores(f.strip().replace("$", ""))) for f in lista]
	def cursores(self, funcion):
		funcion=funcion.replace(",", "},${~:").replace("(", "(${~:").replace(")", "})")
		text=""
		i=1
		for c in funcion:
			if c=="~":
				text+=str(i)
				continue
			text+=c
		return text



